from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class SSLink(Base):
    __tablename__ = "ss_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    key_id: Mapped[str] = mapped_column(String(128), unique=True)
    access_url: Mapped[str] = mapped_column(String(512))
    user: Mapped["User"] = relationship("User", back_populates="ss_links")
