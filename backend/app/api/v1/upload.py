from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.upload_service import upload_file, get_jobs_preview, load_test_data

router = APIRouter(prefix="/upload", tags=["数据上传"])


@router.post("/test-data")
async def test_data(db: Session = Depends(get_db)):
    return await load_test_data(db)


@router.post("/")
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await upload_file(file, db)


@router.get("/preview/{batch_id}")
async def preview(
    batch_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_jobs_preview(batch_id, page, page_size, db)
