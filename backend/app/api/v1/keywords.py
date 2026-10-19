from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.services.keyword_service import (
    calculate_keywords_stats,
    get_keywords,
    get_trend_data
)

router = APIRouter(prefix="/keywords", tags=["关键词分析"])


@router.post("/analyze/{batch_id}")
async def analyze_keywords(
    batch_id: str,
    background_tasks: BackgroundTasks,
    time_dim: str = Query('month', regex='^(month|quarter)$'),
    top_n: int = Query(50, ge=10, le=200),
    db: Session = Depends(get_db)
):
    def run_analysis():
        calculate_keywords_stats(batch_id, time_dim, top_n, db)
    
    background_tasks.add_task(run_analysis)
    
    return {
        "batch_id": batch_id,
        "status": "processing",
        "time_dim": time_dim
    }


@router.get("/")
async def get_keywords_list(
    batch_id: str = Query(...),
    top_n: int = Query(20, ge=1, le=100),
    job_category: Optional[str] = Query(None),
    time_period: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    keywords = get_keywords(batch_id, top_n, job_category, time_period, db)
    
    return {
        "keywords": keywords,
        "total": len(keywords)
    }


@router.get("/trend")
async def get_trend(
    batch_id: str = Query(...),
    keywords: Optional[str] = Query(None),
    time_dim: str = Query('month'),
    db: Session = Depends(get_db)
):
    keyword_list = keywords.split(',') if keywords else None
    
    trend_data = get_trend_data(batch_id, keyword_list, time_dim, db)
    
    return {
        "data": trend_data,
        "time_dim": time_dim
    }
