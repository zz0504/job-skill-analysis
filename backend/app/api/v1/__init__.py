from fastapi import APIRouter
from app.api.v1.upload import router as upload_router
from app.api.v1.clean import router as clean_router
from app.api.v1.keywords import router as keywords_router
from app.api.v1.matrix import router as matrix_router
from app.api.v1.report import router as report_router
from app.api.v1.auth import router as auth_router
from app.api.v1.batch import router as batch_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(upload_router)
api_router.include_router(clean_router)
api_router.include_router(keywords_router)
api_router.include_router(matrix_router)
api_router.include_router(report_router)
api_router.include_router(batch_router)
