"""
Declare SQLAlchemy's Table Objects.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class URL(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(primary_key=True)
    long_url: Mapped[str] = mapped_column(nullable=False)
    short_code: Mapped[str] = mapped_column(unique=True, nullable=True)

    def __repr__(self) -> str:
        return f"URL(id={self.id!r}, long_url={self.long_url!r}, short_code={self.short_code!r})"
