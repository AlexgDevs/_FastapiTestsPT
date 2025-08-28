from fastapi import HTTPException, status  
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
    DateTime,
    select
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    joinedload)

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


class DBHelper:
    @staticmethod
    async def get_user(user_id: int):
        async with Session() as session:
            user = await session.scalar(
                select(User)
                .where(User.id == user_id)
            )

            if user:
                return user
            
        return None
    

    @staticmethod
    async def get_card(user_id: int, card_id: int):
        async with Session() as session:
            card = await session.scalar(
                select(Card)
                .where(Card.id == card_id, Card.user_id == user_id)
            )

            if card:
                return card
            
        return None
    

    @staticmethod
    async def get_account(user_id: int, account_id: int):
        async with Session() as session:
            account = await session.scalar(
                select(Account)
                .where(Account.id == account_id, Account.user_id == user_id)
                .options(joinedload(Account.user))
            )

            if account:
                return account
        
        return None 


async def get_session(begin: bool = False):
    async with Session() as session:
        try:
            if begin:
                async with session.begin():
                    yield session
            else:
                yield session
        finally:
            await session.close()


async def get_session_begin():
    await get_session(begin=True)


from .models import (
    User,
    Account,
    Card,
    Transaction,
    AccountTransaction
)


