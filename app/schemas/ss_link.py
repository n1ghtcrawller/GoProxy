from pydantic import BaseModel

class SSLinkBase(BaseModel):
    id: str
    access_url: str

    class Config:
        orm_mode = True
