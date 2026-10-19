from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.matrix_service import get_job_skill_matrix, get_matrix_table

router = APIRouter(prefix="/matrix", tags=["岗位技能矩阵"])


@router.get("/")
async def get_matrix(
    batch_id: str = Query(...),
    top_n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    matrix = get_job_skill_matrix(batch_id, top_n, db)
    
    return {
        "matrix": matrix,
        "total": len(matrix)
    }


@router.get("/table")
async def get_table(
    batch_id: str = Query(...),
    top_n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return get_matrix_table(batch_id, top_n, db)
