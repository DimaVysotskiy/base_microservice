from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from ..core import settings




class Base(DeclarativeBase):
    pass


class PostgresSessionManager:

    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    def init(self) -> None:
        pg = settings.postgres
        
        # Настраиваем аргументы подключения, включая схему (для драйвера asyncpg)
        connect_args = {}
        if pg.schema_:
            connect_args["server_settings"] = {"search_path": pg.schema_}

        self.engine = create_async_engine(
            pg.dsn,
            pool_size=pg.pool_size,
            max_overflow=pg.max_overflow,
            pool_pre_ping=True,
            pool_recycle=pg.pool_recycle,
            echo=True, # В проде поставить False
            connect_args=connect_args,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )


    async def close(self) -> None:
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None


    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self.session_factory:
            raise RuntimeError("Менеджер БД не инициализирован. Вызовите init().")

        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise  


postgres_manager = PostgresSessionManager()


# Ф-ция для FastAPI dependency
async def get_psql() -> AsyncGenerator[AsyncSession, None]:
    async for session in postgres_manager.get_session():
        yield session