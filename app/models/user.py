from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import Optional, List
from app.models.ss_link import SSLink
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    photo_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    ss_links: Mapped[List["SSLink"]] = relationship(
        "SSLink", back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
