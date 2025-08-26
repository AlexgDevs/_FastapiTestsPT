from typing import List
from ... import (
    Base,
    Mapped,
    mapped_column,
    String,
    relationship
    )

class User(Base):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(512))
    email: Mapped[str]

    accounts: Mapped[List['Account']] = relationship('Account', back_populates='user')
    cards: Mapped[List['Card']] = relationship('Card', back_populates='user')

    transactions: Mapped[List['Transaction']] = relationship('Transaction', back_populates='user')
    account_transactions: Mapped[List['AccountTransaction']] = relationship('AccountTransaction', back_populates='user')