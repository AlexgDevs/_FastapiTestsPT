from typing import List
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
    account_name: Mapped[str] = mapped_column(String(150), default='Main face account')
    balance: Mapped[int]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='accounts', uselist=False)

    cards: Mapped[List['Card']] = relationship('Card', back_populates='account')

    transactions: Mapped[List['Transaction']] = relationship('Transaction', back_populates='account')
    
    from_account_transactions: Mapped[List['AccountTransaction']] = relationship('AccountTransaction', back_populates='from_account')
    to_account_transactions: Mapped[List['AccountTransaction']] = relationship('AccountTransaction', back_populates='to_account')
