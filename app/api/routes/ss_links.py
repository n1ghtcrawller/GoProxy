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

from sqlalchemy.future import select
from fastapi import HTTPException

@router.get("/me", response_model=SSLinkBase)
async def users_link(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user = await get_current_user(user_id, session)

    result = await session.execute(
        select(SSLink).where(SSLink.user_id == user.user_id).order_by(SSLink.id.desc())
    )
    link = result.scalars().first()
    if not link:
        raise HTTPException(status_code=404, detail="Access link not found for this user")
    generator = SSGenerator(session)
    ss_data = await generator.get_access_key(link.key_id)

    if not ss_data:
        raise HTTPException(status_code=404, detail="Access key not found on remote server")

    return SSLinkBase(id=ss_data["id"], access_url=ss_data["accessUrl"])

@router.delete("/me", status_code=204)
async def delete_users_link(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user = await get_current_user(user_id, session)

    result = await session.execute(
        select(SSLink).where(SSLink.user_id == user.user_id).order_by(SSLink.id.desc())
    )
    link = result.scalars().first()

    if not link:
        raise HTTPException(status_code=404, detail="Access link not found for this user")

    generator = SSGenerator(session)

    deleted = await generator.delete_access_key(link.key_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Access key not found on remote server")

    await session.delete(link)
    await session.commit()

    return
