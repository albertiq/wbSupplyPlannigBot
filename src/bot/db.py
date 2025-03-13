import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from settings import cfg


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(
            url=cfg.postgres_dsn.unicode_string(),
            future=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=60,
        )
        self._session_factory = async_scoped_session(
            async_sessionmaker(bind=self.engine, expire_on_commit=False), asyncio.current_task
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
