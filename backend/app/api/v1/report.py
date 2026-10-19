from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.report_service import generate_report_data
from app.services.keyword_service import get_keywords, get_trend_data
from app.services.matrix_service import get_job_skill_matrix
from app.models.user import BatchRecord

router = APIRouter(prefix="/report", tags=["分析报告"])


@router.get("/")
async def generate_report(
    batch_id: str = Query(...),
    db: Session = Depends(get_db)
):
    batch = db.query(BatchRecord).filter(BatchRecord.batch_id == batch_id).first()
    if not batch:
        return {"error": "批次不存在"}
    
    batch_info = {
        "batch_id": batch.batch_id,
        "file_name": batch.file_name,
        "total_count": batch.total_count,
        "clean_count": batch.clean_count,
        "status": batch.status
    }
    
    keywords = get_keywords(batch_id, top_n=50, db=db)
    
    top_keywords = [kw['name'] for kw in keywords[:5]]
    trend_data = get_trend_data(batch_id, top_keywords, 'month', db=db)
    
    matrix_data = get_job_skill_matrix(batch_id, top_n=10, db=db)
    
    report = generate_report_data(keywords, trend_data, matrix_data, batch_info)
    
    return JSONResponse(content=report)
