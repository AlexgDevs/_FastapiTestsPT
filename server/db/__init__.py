from typing import List, Literal
from datetime import datetime

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession)

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship)

from .config import db_settings


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


engine = create_async_engine(
    url=db_settings.database_url,
    echo=db_settings.echo_sql
)


Session = async_sessionmaker(
    bind=engine,
    expire_on_commit=True
)


async def get_db():
    async with Session() as session:
            yield session



class DBManager:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine


    async def up(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    async def drop(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


    async def migrate(self):
        await self.drop()
        await self.up()


db_manager = DBManager(engine)


from .models import (
    User,
    Account,
    Card,
    Transaction,
    AccountTransaction
)


