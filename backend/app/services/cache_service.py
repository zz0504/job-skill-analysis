import redis
import json
from typing import Optional, Any
from app.core.config import settings


class CacheService:
    def __init__(self):
        self.redis_client = None
        self.enabled = False
        
        try:
            if settings.REDIS_HOST:
                self.redis_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    password=settings.REDIS_PASSWORD,
                    db=settings.REDIS_DB,
                    decode_responses=True
                )
                self.redis_client.ping()
                self.enabled = True
        except Exception as e:
            print(f"Redis连接失败，缓存功能将禁用: {e}")
            self.enabled = False
    
    def get(self, key: str) -> Optional[Any]:
        if not self.enabled:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            print(f"缓存读取失败: {e}")
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        if not self.enabled:
            return False
        
        try:
            ttl = ttl or settings.CACHE_TTL
            serialized = json.dumps(value, ensure_ascii=False)
            self.redis_client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            print(f"缓存写入失败: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        if not self.enabled:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"缓存删除失败: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> bool:
        if not self.enabled:
            return False
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            print(f"缓存批量删除失败: {e}")
            return False


cache_service = CacheService()


def cache_key(prefix: str, **kwargs) -> str:
    parts = [prefix]
    for k, v in sorted(kwargs.items()):
        if v is not None:
            parts.append(f"{k}:{v}")
    return ":".join(parts)
