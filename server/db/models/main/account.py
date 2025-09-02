import string
from typing import List
from secrets import choice
from ... import (
    Base,
    Mapped,
    mapped_column,
    String,
    ForeignKey,
    relationship,
    DateTime,
    datetime
    )


class Account(Base):
    __tablename__ = 'accounts'
    account_number: Mapped[str] = mapped_column(String(20), default=lambda: ''.join(choice(string.digits) for _ in range(20)))
    account_name: Mapped[str] = mapped_column(String(150), default='Main face account')
    balance: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='accounts', uselist=False)

    cards: Mapped[List['Card']] = relationship('Card', back_populates='account')

    transactions: Mapped[List['Transaction']] = relationship('Transaction', back_populates='account')
    
    from_account_transactions: Mapped[List['AccountTransaction']] = relationship('AccountTransaction', back_populates='from_account', foreign_keys='AccountTransaction.from_account_id')
    to_account_transactions: Mapped[List['AccountTransaction']] = relationship('AccountTransaction', back_populates='to_account', foreign_keys='AccountTransaction.to_account_id')
