import re
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.job import JobRaw, JobClean
from app.models.user import BatchRecord


JOB_CATEGORIES = {
    '开发': ['开发', '工程师', '程序员', '架构师', '开发工程师', '后端', '前端', '全栈'],
    '运维': ['运维', 'DevOps', 'SRE', '系统管理员', '网络工程师'],
    '测试': ['测试', 'QA', '测试工程师', '自动化测试'],
    '产品': ['产品', 'PM', '产品经理', '产品助理'],
    '设计': ['设计', 'UI', 'UX', '视觉设计', '交互设计'],
    '数据': ['数据', '数据分析', '数据挖掘', '算法', 'AI', '机器学习'],
    '运营': ['运营', '市场', '推广', '增长'],
    '管理': ['经理', '总监', '主管', '负责人', 'Lead']
}


def classify_job(job_title: str) -> str:
    if not job_title:
        return '其他'
    
    job_title_lower = job_title.lower()
    
    for category, keywords in JOB_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in job_title_lower:
                return category
    
    return '其他'


def clean_text(text: str) -> str:
    if not text:
        return ''
    
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def clean_data(batch_id: str, db: Session) -> dict:
    batch = db.query(BatchRecord).filter(BatchRecord.batch_id == batch_id).first()
    if not batch:
        return {"status": "error", "message": "批次不存在"}
    
    batch.status = 'processing'
    db.commit()
    
    raw_jobs = db.query(JobRaw).filter(JobRaw.batch_id == batch_id).all()
    
    seen = set()
    clean_records = []
    duplicate_count = 0
    
    for job in raw_jobs:
        key = (job.job_title, job.company, job.publish_date)
        
        if key in seen:
            duplicate_count += 1
            continue
        
        seen.add(key)
        
        publish_date = job.publish_date if job.publish_date else datetime.now()
        
        description_clean = clean_text(job.description)
        
        job_category = classify_job(job.job_title)
        
        clean_record = JobClean(
            batch_id=batch_id,
            job_title=job.job_title,
            company=job.company,
            publish_date=publish_date,
            description_clean=description_clean,
            job_category=job_category
        )
        clean_records.append(clean_record)
    
    db.bulk_save_objects(clean_records)
    
    batch.clean_count = len(clean_records)
    batch.status = 'completed'
    db.commit()
    
    return {
        "status": "success",
        "batch_id": batch_id,
        "total_count": len(raw_jobs),
        "clean_count": len(clean_records),
        "duplicate_count": duplicate_count
    }


def get_clean_status(batch_id: str, db: Session) -> dict:
    batch = db.query(BatchRecord).filter(BatchRecord.batch_id == batch_id).first()
    
    if not batch:
        return {"status": "not_found"}
    
    return {
        "status": batch.status,
        "batch_id": batch.batch_id,
        "total_count": batch.total_count,
        "clean_count": batch.clean_count,
        "file_name": batch.file_name
    }
