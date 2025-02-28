import json

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, int_primary, str_unique


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int_primary]
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str_unique]
    password: Mapped[str] = mapped_column(nullable=False)
    __table_args__ = (
        CheckConstraint("LENGTH(password) >= 6", name="password_min_length"),
    )

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }, ensure_ascii=False)

    def __repr__(self):
        return (f"User(id={self.id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', email='{self.email}', "
                f"created_at={self.created_at}, updated_at={self.updated_at})")
