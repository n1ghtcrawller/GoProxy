from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.services.ss_generator import SSGenerator
from app.models.user import User
from app.models.ss_link import SSLink
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
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_current_user(user_id, session)

    generator = SSGenerator(session)
    ss_data = await generator.create_access_key()

    key_id = ss_data["id"]
    access_url = ss_data["accessUrl"]

    new_link = SSLink(
        user_id=user.user_id,
        key_id=key_id,
        access_url=access_url
    )
    session.add(new_link)
    await session.commit()
    await session.refresh(new_link)

    return SSLinkBase(id=key_id, access_url=access_url)

@router.get("test")
async def test_ss_server(session: AsyncSession = Depends(get_async_session)):
    generator = SSGenerator(session)
    response = await generator.test_server()
    return response

@router.get("/me", response_model=list[SSLinkBase])
async def users_link(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user = await get_current_user(user_id, session)
    links = user.ss_links
    return