from redis.asyncio import ConnectionPool, Redis

from ..core import settings


class RedisManager:
    """Manages async Redis connection pool."""

    def __init__(self) -> None:
        self._pool: ConnectionPool | None = None
        self._client: Redis | None = None

    def init(self) -> None:
        self._pool = ConnectionPool.from_url(
            settings.redis.dsn,
            max_connections=settings.postgres.pool_size, # Потом настроить отдельно для Redis
            decode_responses=True,
        )
        self._client = Redis(connection_pool=self._pool)

    @property
    def client(self) -> Redis:
        if self._client is None:
            raise RuntimeError("Redis client is not initialized. Call init() first.")
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
        if self._pool:
            await self._pool.aclose()
            self._pool = None


redis_manager = RedisManager()


# Ф-ция для FastAPI dependency
async def get_redis() -> Redis:
    """FastAPI dependency — returns the shared async Redis client."""
    return redis_manager.client