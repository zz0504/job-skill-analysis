from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class JobRawBase(BaseModel):
    job_title: str
    company: str
    publish_date: Optional[datetime] = None
    description: Optional[str] = None


class JobRawCreate(JobRawBase):
    batch_id: str
    source_file: Optional[str] = None


class JobRawResponse(JobRawBase):
    id: int
    batch_id: str
    source_file: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class JobCleanBase(BaseModel):
    job_title: str
    company: str
    publish_date: datetime
    description_clean: Optional[str] = None
    job_category: Optional[str] = None


class JobCleanCreate(JobCleanBase):
    batch_id: str


class JobCleanResponse(JobCleanBase):
    id: int
    batch_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class KeywordStatBase(BaseModel):
    keyword: str
    frequency: int
    job_category: Optional[str] = None
    time_period: Optional[str] = None
    time_dim: Optional[str] = None


class KeywordStatCreate(KeywordStatBase):
    batch_id: str


class KeywordStatResponse(KeywordStatBase):
    id: int
    batch_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class BatchRecordBase(BaseModel):
    batch_id: str
    file_name: Optional[str] = None
    total_count: int = 0
    clean_count: int = 0
    status: str = "pending"


class BatchRecordCreate(BatchRecordBase):
    pass


class BatchRecordResponse(BatchRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    batch_id: str
    message: str
    total_count: int


class CleanResponse(BaseModel):
    batch_id: str
    status: str
    clean_count: Optional[int] = None


class KeywordResponse(BaseModel):
    keywords: List[dict]
    total: int


class TrendResponse(BaseModel):
    data: List[dict]
    time_dim: str


class MatrixResponse(BaseModel):
    matrix: List[dict]
