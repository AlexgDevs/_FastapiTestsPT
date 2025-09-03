from datetime import timedelta
import random
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


class Card(Base):
    __tablename__ = 'cards'
    cardholder_name: Mapped[str] = mapped_column(String(150))
    card_number: Mapped[str] = mapped_column(String(16),  default=lambda: '4' + ''.join([str(random.randint(0, 9)) for _ in range(15)]))
    cvv: Mapped[str] = mapped_column(String(3),  default=lambda: ''.join([str(random.randint(0, 9)) for _ in range(3)]))
    expire_date: Mapped[str] = mapped_column(String(5), default=lambda: (datetime.now() + timedelta(days=365*3)).strftime('%m/%y'))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    account: Mapped['Account'] = relationship('Account', back_populates='cards', uselist=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='cards', uselist=False)

    transactions: Mapped[List['Transaction']] = relationship('Transaction', back_populates='card')
    account_transactions: Mapped[List['AccountTransaction']] = relationship('AccountTransaction', back_populates='card')