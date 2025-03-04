from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session
from typing import Any

from db import Base


class AsyncBaseRepository(ABC):
    @abstractmethod
    async def retrieve(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def retrieve_many(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def create(self, *args, **kwargs) -> None:
        pass


class SqlAlchemyRepository(AsyncBaseRepository):
    def __init__(self, session: async_scoped_session):
        self.session = session

    async def retrieve(self, model: type[Base], where_clause: list | None = None, order_by: list | None = None) -> Any:
        statement = select(model)

        if where_clause:
            statement = statement.where(*where_clause)
        if order_by:
            statement = statement.order_by(*order_by)

        async with self.session() as session:
            results = await session.execute(statement=statement)
            return results.scalar_one_or_none()

    async def retrieve_many(
        self, model: type[Base], where_clause: list | None = None, order_by: list | None = None
    ) -> Any:
        statement = select(model)

        if where_clause:
            statement = statement.where(*where_clause)
        if order_by:
            statement = statement.order_by(*order_by)

        async with self.session() as session:
            results = await session.execute(statement=statement)
            return results.scalars().all()

    async def create(self, model: type[Base], **kwargs) -> None:
        self.session.add(model)
        await self.session.commit()
