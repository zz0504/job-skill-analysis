from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码哈希")
    email = Column(String(128), nullable=True, comment="邮箱")
    is_active = Column(Integer, default=1, comment="是否激活")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class BatchRecord(Base):
    __tablename__ = "batch_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(String(64), unique=True, nullable=False, comment="批次ID")
    file_name = Column(String(255), nullable=True, comment="文件名")
    total_count = Column(Integer, default=0, comment="总记录数")
    clean_count = Column(Integer, default=0, comment="清洗后记录数")
    status = Column(String(20), default="pending", comment="状态")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
