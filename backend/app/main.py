import os
from pathlib import Path
from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import engine
from app.core.logger import logger
from app.api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="招聘岗位技能关键词分析系统API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def read_root():
    index_file = frontend_dist / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Frontend not built. Please run 'npm run build' in frontend directory."}


@app.on_event("startup")
async def startup_event():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("数据库连接成功")
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        raise
    
    try:
        upload_dir = settings.UPLOAD_DIR
        os.makedirs(upload_dir, exist_ok=True)
        
        test_file = os.path.join(upload_dir, ".test")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        
        logger.info(f"上传目录准备就绪: {upload_dir}")
    except Exception as e:
        logger.error(f"上传目录检查失败: {str(e)}")
        raise
    
    try:
        from app.core.database import SessionLocal
        from app.services.init_test_data import init_test_data
        
        db = SessionLocal()
        try:
            init_success = init_test_data(db, num_records=100)
            if init_success:
                logger.info("测试数据初始化成功")
            else:
                logger.info("测试数据已存在")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"测试数据初始化失败: {str(e)}", exc_info=True)
    
    logger.info("应用启动完成")
