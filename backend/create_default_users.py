"""
创建默认用户脚本
运行此脚本创建默认管理员和测试账号
"""
import os

import bcrypt
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User


def hash_password(password: str) -> str:
    """生成密码hash"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_default_users():
    db: Session = SessionLocal()
    
    try:
        # 默认账号列表
        default_users = [
            {
                "username": "admin",
                "password": os.getenv("DEFAULT_ADMIN_PASSWORD", "CHANGE_ME_ADMIN_PWD"),
                "email": "admin@example.com",
                "is_active": 1
            },
            {
                "username": "test",
                "password": os.getenv("DEFAULT_TEST_PASSWORD", "CHANGE_ME_TEST_PWD"),
                "email": "test@example.com",
                "is_active": 1
            }
        ]
        
        for user_data in default_users:
            # 检查用户是否已存在
            existing_user = db.query(User).filter(
                User.username == user_data["username"]
            ).first()
            
            if existing_user:
                print(f"用户 {user_data['username']} 已存在，跳过创建")
                continue
            
            # 创建新用户
            hashed_password = hash_password(user_data["password"])
            new_user = User(
                username=user_data["username"],
                password=hashed_password,
                email=user_data["email"],
                is_active=user_data["is_active"]
            )
            
            db.add(new_user)
            print(f"✅ 创建用户: {user_data['username']}, 密码: {user_data['password']}")
        
        db.commit()
        print("\n默认用户创建完成！")
        
    except Exception as e:
        print(f"❌ 创建用户失败: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("创建默认用户账号")
    print("=" * 50)
    create_default_users()
