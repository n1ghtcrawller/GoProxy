from pydantic import BaseModel, HttpUrl
from typing import Optional

class UserBase(BaseModel):
    user_id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    photo_url: Optional[str]

    class Config:
        from_attributes = True

