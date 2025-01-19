from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import (
    VARCHAR,
    TEXT,
)

from src.sqla.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    user_name: Mapped[str] = mapped_column(VARCHAR(length=60), nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.user_name}: {self.description[:20]}"
