import secrets
import random
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ss_link import SSLink
from app.models.user import User
from sqlalchemy import select
from app.db.session import get_async_session

class SSGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _generate_password(self, length: int = 16) -> str:
        return secrets.token_urlsafe(length)

    async def _get_available_port(self, min_port: int = 30000, max_port: int = 40000) -> int:
        used_ports = await self.db.scalars(select(SSLink.port))
        used = set(used_ports.all())

        for _ in range(1000):
            port = random.randint(min_port, max_port)
            if port not in used:
                return port
        raise RuntimeError("No available ports found")

    async def create_link(self, user: User, method: str = "aes-256-gcm") -> SSLink:
        password = await self._generate_password()
        port = await self._get_available_port()

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
