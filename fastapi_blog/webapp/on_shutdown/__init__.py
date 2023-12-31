from redis.asyncio import Redis

from webapp.db import kafka

redis: Redis = None


async def stop_producer() -> None:
    await kafka.producer.stop()


async def close_redis_pool():
    """
    Закрывает пул подключений к Redis.
    Вызывается при остановке приложения.
    """
    global redis
    if redis:
        await redis.close()
