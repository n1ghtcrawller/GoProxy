from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class SSLink(Base):
    __tablename__ = "ss_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    method: Mapped[str] = mapped_column(String(32), default="aes-256-gcm")
    password: Mapped[str] = mapped_column(String(128))
    port: Mapped[int] = mapped_column(Integer)

    user: Mapped["User"] = relationship("User", back_populates="ss_links")

    def generate_ss_url(self, host: str) -> str:
        from base64 import urlsafe_b64encode
        config = f"{self.method}:{self.password}@{host}:{self.port}"
        encoded = urlsafe_b64encode(config.encode()).decode()
        return f"ss://{encoded}"
