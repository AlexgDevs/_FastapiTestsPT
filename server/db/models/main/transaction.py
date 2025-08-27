from typing import List, Literal
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


class Transaction(Base):
    __tablename__ = 'transactions'
    card_id: Mapped[int] = mapped_column(ForeignKey('cards.id'))
    card: Mapped['Card'] = relationship('Card', back_populates='transactions', uselist=False)

    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    account: Mapped['Account'] = relationship('Account', back_populates='transactions', uselist=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='transactions', uselist=False)

    transaction_type: Mapped[Literal['from_account', 'to_account']]

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)    
    amount: Mapped[int]


class AccountTransaction(Base):
    __tablename__ = 'account_transactions'
    card_id: Mapped[int] = mapped_column(ForeignKey('cards.id'))
    card: Mapped['Card'] = relationship('Card', back_populates='account_transactions', uselist=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='account_transactions', uselist=False)

    from_account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    from_account: Mapped['Account'] = relationship('Account', back_populates='from_account_transactions', uselist=False, foreign_keys=[from_account_id])

    to_account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    to_account: Mapped['Account'] = relationship('Account', back_populates='to_account_transactions', uselist=False, foreign_keys=[to_account_id])

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    amount: Mapped[int]
