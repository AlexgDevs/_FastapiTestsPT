from ... import (
    Base,
    Mapped,
    mapped_column,
    String
    )

class User(Base):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(512))
    email: Mapped[str]