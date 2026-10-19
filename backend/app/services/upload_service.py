import os
import uuid
import pandas as pd
from datetime import datetime
from fastapi import UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.logger import logger
from app.models.job import JobRaw
from app.models.user import BatchRecord
from app.schemas.job import UploadResponse, JobRawResponse
from app.utils.parse_config import ParseConfig, ParseContext
from app.utils.csv_parser import EncodingDetector, SeparatorDetector
from app.utils.error_handler import ParseErrorHandler
from typing import List


def validate_file(file: UploadFile) -> str:
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式，仅支持 {settings.ALLOWED_EXTENSIONS}"
        )
    
    return ext


async def save_upload_file(file: UploadFile) -> tuple:
    batch_id = str(uuid.uuid4())
    filename = f"{batch_id}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    try:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        content = await file.read()
        
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"文件大小超过限制（最大 {settings.MAX_FILE_SIZE / 1024 / 1024}MB）"
            )
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        logger.info(f"文件保存成功: {file_path}")
        return batch_id, file_path, filename
        
    except PermissionError:
        logger.error(f"上传目录权限不足: {settings.UPLOAD_DIR}")
        raise HTTPException(
            status_code=500,
            detail="上传目录权限不足，请联系管理员"
        )
    except OSError as e:
        logger.error(f"文件保存失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"文件保存失败: {str(e)}"
        )


def parse_csv_excel(file_path: str, ext: str, batch_id: str = None) -> pd.DataFrame:
    context = ParseContext(
        file_path=file_path,
        file_name=os.path.basename(file_path),
        file_ext=ext,
        batch_id=batch_id or str(uuid.uuid4())
    )
    
    config = ParseConfig()
    
    try:
        if ext == '.csv':
            encoding_detector = EncodingDetector(config)
            encoding, df = encoding_detector.detect(file_path, context)
            
            logger.info(f"编码检测完成: {encoding}")
            logger.info(f"编码尝试记录: {context.encoding_attempts}")
            
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
            logger.info(f"Excel文件解析成功，共 {len(df)} 行")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式: {ext}"
            )
        
        field_mapping = config.field_mapping
        for source_field, target_field in field_mapping.items():
            if source_field in df.columns and target_field not in df.columns:
                df[target_field] = df[source_field]
                context.log_field_mapping(source_field, target_field)
                logger.info(f"字段映射: {source_field} -> {target_field}")
        
        if '发布时间' not in df.columns:
            df['发布时间'] = datetime.now().strftime('%Y-%m-%d')
            logger.info("添加默认发布时间字段")
        
        missing_fields = []
        for required_field in config.required_fields:
            if required_field not in df.columns:
                missing_fields.append(required_field)
        
        if missing_fields:
            raise KeyError(f"缺少必需字段: {', '.join(missing_fields)}")
        
        logger.info(f"字段映射记录: {context.field_mappings}")
        
        return df
        
    except HTTPException:
        raise
    except UnicodeDecodeError as e:
        raise ParseErrorHandler.handle_parse_error(e, {
            "encoding_attempts": context.encoding_attempts,
            "file_path": file_path
        })
    except pd.errors.ParserError as e:
        raise ParseErrorHandler.handle_parse_error(e, {
            "file_path": file_path,
            "detected_encoding": context.detected_encoding
        })
    except pd.errors.EmptyDataError as e:
        raise ParseErrorHandler.handle_parse_error(e, {
            "file_path": file_path
        })
    except KeyError as e:
        raise ParseErrorHandler.handle_parse_error(e, {
            "available_columns": list(df.columns) if 'df' in locals() else []
        })
    except Exception as e:
        logger.error(f"文件解析失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"文件解析失败: {str(e)}"
        )


def save_to_database(
    df: pd.DataFrame,
    batch_id: str,
    source_file: str,
    db: Session
) -> int:
    try:
        records = []
        
        for _, row in df.iterrows():
            publish_date = row.get('发布时间')
            if pd.isna(publish_date):
                publish_date = None
            elif isinstance(publish_date, str):
                try:
                    publish_date = datetime.strptime(publish_date, '%Y-%m-%d')
                except:
                    publish_date = datetime.now()
            
            record = JobRaw(
                batch_id=batch_id,
                job_title=str(row.get('岗位名称', '')),
                company=str(row.get('公司', '')),
                publish_date=publish_date,
                description=str(row.get('技能描述', row.get('岗位职责', ''))),
                source_file=source_file
            )
            records.append(record)
        
        db.bulk_save_objects(records)
        db.commit()
        
        logger.info(f"数据库写入成功: {len(records)} 条记录")
        return len(records)
        
    except Exception as e:
        db.rollback()
        logger.error(f"数据库写入失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="数据库写入失败，请联系管理员"
        )


def create_batch_record(
    batch_id: str,
    file_name: str,
    total_count: int,
    db: Session
) -> BatchRecord:
    batch = BatchRecord(
        batch_id=batch_id,
        file_name=file_name,
        total_count=total_count,
        status='uploaded'
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


async def load_test_data(db: Session) -> UploadResponse:
    try:
        logger.info("开始加载测试数据")
        
        test_file_path = os.path.join(settings.UPLOAD_DIR, "test_data.xlsx")
        
        if not os.path.exists(test_file_path):
            raise HTTPException(
                status_code=404,
                detail="测试数据文件不存在"
            )
        
        batch_id = str(uuid.uuid4())
        filename = f"{batch_id}_test_data.xlsx"
        
        df = parse_csv_excel(test_file_path, '.xlsx', batch_id)
        total_count = save_to_database(df, batch_id, filename, db)
        create_batch_record(batch_id, "招聘岗位技能数据集_500条.xlsx", total_count, db)
        
        logger.info(f"测试数据加载成功: batch_id={batch_id}, total_count={total_count}")
        
        return UploadResponse(
            batch_id=batch_id,
            message="测试数据加载成功",
            total_count=total_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"测试数据加载失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"测试数据加载失败: {str(e)}"
        )


async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> UploadResponse:
    try:
        logger.info(f"开始处理文件上传: {file.filename}")
        
        ext = validate_file(file)
        batch_id, file_path, filename = await save_upload_file(file)
        df = parse_csv_excel(file_path, ext, batch_id)
        total_count = save_to_database(df, batch_id, filename, db)
        create_batch_record(batch_id, file.filename, total_count, db)
        
        logger.info(f"文件上传成功: batch_id={batch_id}, total_count={total_count}")
        
        return UploadResponse(
            batch_id=batch_id,
            message="文件上传成功",
            total_count=total_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"文件处理失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="文件处理失败，请联系管理员"
        )


def get_jobs_preview(
    batch_id: str,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
) -> dict:
    offset = (page - 1) * page_size
    
    total = db.query(JobRaw).filter(JobRaw.batch_id == batch_id).count()
    
    jobs = db.query(JobRaw).filter(
        JobRaw.batch_id == batch_id
    ).offset(offset).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": [JobRawResponse.model_validate(job) for job in jobs]
    }
