from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.clean_service import clean_data, get_clean_status
from app.schemas.job import CleanResponse

router = APIRouter(prefix="/jobs", tags=["数据处理"])


@router.post("/clean/{batch_id}")
async def clean_batch(
    batch_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    def run_clean():
        clean_data(batch_id, db)
    
    background_tasks.add_task(run_clean)
    
    return {
        "batch_id": batch_id,
        "status": "processing"
    }


@router.get("/clean/status/{batch_id}")
async def get_status(
    batch_id: str,
    db: Session = Depends(get_db)
):
    return get_clean_status(batch_id, db)
