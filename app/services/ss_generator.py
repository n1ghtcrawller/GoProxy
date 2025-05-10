from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ss_link import SSLink
from app.models.user import User


class SSGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_link(
            self,
            user: User,
            password: str,
            port: int,
            method: str = "aes-256-gcm"
    ) -> SSLink:
        ss_link = SSLink(
            user_id=user.user_id,
            method=method,
            password=password,
            port=port
        )

        self.db.add(ss_link)
        await self.db.commit()
        await self.db.refresh(ss_link)

        return ss_link