from pydantic import BaseModel
from datetime import datetime

class SSLinkBase(BaseModel):
    id: int
    user_id: int
    method: str
    port: int
    url: str

    class Config:
        orm_mode = True