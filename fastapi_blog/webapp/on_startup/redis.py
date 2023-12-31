import redis.asyncio as aioredis
from redis.asyncio import Redis

# Глобальная переменная для хранения подключения к Redis
redis: Redis = None


async def get_redis_pool() -> Redis:
    """
    Создает и возвращает пул подключений к Redis.
    Вызывается при старте приложения.
    """
    global redis
    redis = aioredis.from_url('redis://redis', encoding='utf-8', decode_responses=True)
    return redis
