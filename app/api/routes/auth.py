from fastapi import APIRouter, Depends, HTTPException, Form, status
from app.services.telegram_auth import TelegramAuthService
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserBase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/telegram", response_model=UserBase)
async def telegram_auth(
    id: int = Form(...),
    username: str = Form(...),
    first_name: str = Form(None),
    last_name: str = Form(None),
    photo_url: str = Form(None),
    hash: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    data = {
        "id": id,
        "username": username,
        "first_name": first_name or "",
        "last_name": last_name or "",
        "photo_url": photo_url or "",
        "hash": hash
    }

    if not TelegramAuthService.verify(data.copy()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth data")

    user = await session.get(User, id)
    if not user:
        user = User(user_id=id, username=username, first_name=first_name, last_name=last_name, photo_url=photo_url)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


@router.post("/register", response_model=UserBase)
async def register_user(
    user_data: UserBase,
    session: AsyncSession = Depends(get_async_session)
):
    existing_user = await session.get(User, user_data.user_id)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(**user_data.dict())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
