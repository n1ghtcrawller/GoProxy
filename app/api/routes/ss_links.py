from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.services.ss_generator import SSGenerator
from app.models.user import User
from app.schemas.ss_link import SSLinkBase
from app.core.config import settings

router = APIRouter(prefix="/ss-links", tags=["ss-links"])

async def get_current_user(id: int, session: AsyncSession) -> User:
    user = await session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/generate", response_model=SSLinkBase)
async def generate_ss_link(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    user = await get_current_user(user_id, session)

    generator = SSGenerator(session)
    ss_link = await generator.create_link(
        user=user,
        password=settings.SS_STATIC_PASSWORD,
        port=settings.SS_STATIC_PORT
    )

    url = ss_link.generate_ss_url(settings.HOST)

    return SSLinkBase(
        id=ss_link.id,
        user_id=ss_link.user_id,
        method=ss_link.method,
        port=ss_link.port,
        url=url
    )


@router.get("/me", response_model=list[SSLinkBase])
async def list_my_links(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user = await get_current_user(user_id, session)
    links = user.ss_links
    return [SSLinkBase(
        id=l.id,
        user_id=l.user_id,
        method=l.method,
        port=l.port,
        url=l.generate_ss_url(settings.HOST)
    ) for l in links]