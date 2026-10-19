from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import BatchRecord

router = APIRouter(prefix="/batch", tags=["批次管理"])


@router.get("/latest")
async def get_latest_batch(db: Session = Depends(get_db)):
    batch = db.query(BatchRecord).filter(
        BatchRecord.status == 'completed'
    ).order_by(BatchRecord.created_at.desc()).first()
    
    if not batch:
        return {"batch_id": None, "message": "暂无可用数据"}
    
    return {
        "batch_id": batch.batch_id,
        "file_name": batch.file_name,
        "total_count": batch.total_count,
        "clean_count": batch.clean_count,
        "status": batch.status
    }
