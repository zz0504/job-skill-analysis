from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.core.database import Base


class JobRaw(Base):
    __tablename__ = "jobs_raw"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(String(64), nullable=False, comment="批次ID")
    job_title = Column(String(255), nullable=False, comment="岗位名称")
    company = Column(String(255), nullable=False, comment="公司名称")
    publish_date = Column(DateTime, nullable=True, comment="发布日期")
    description = Column(Text, nullable=True, comment="技能描述")
    source_file = Column(String(255), nullable=True, comment="来源文件")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    __table_args__ = (
        Index('idx_batch', 'batch_id'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )


class JobClean(Base):
    __tablename__ = "jobs_clean"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(String(64), nullable=False, comment="批次ID")
    job_title = Column(String(255), nullable=False, comment="岗位名称")
    company = Column(String(255), nullable=False, comment="公司名称")
    publish_date = Column(DateTime, nullable=False, comment="发布日期")
    description_clean = Column(Text, nullable=True, comment="清洗后描述")
    job_category = Column(String(64), nullable=True, comment="岗位类别")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    __table_args__ = (
        Index('idx_batch_date', 'batch_id', 'publish_date'),
        Index('idx_category', 'job_category'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )


class KeywordStat(Base):
    __tablename__ = "keywords_stat"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(String(64), nullable=False, comment="批次ID")
    keyword = Column(String(128), nullable=False, comment="关键词")
    frequency = Column(Integer, nullable=False, default=0, comment="频次")
    job_category = Column(String(64), nullable=True, comment="岗位类别")
    time_period = Column(String(20), nullable=True, comment="时间段(月/季度)")
    time_dim = Column(String(10), nullable=True, comment="时间维度(month/quarter)")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    __table_args__ = (
        Index('uk_batch_skill_time', 'batch_id', 'keyword', 'job_category', 'time_period', unique=True),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )
