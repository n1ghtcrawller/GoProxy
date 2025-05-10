import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    BOT_TOKEN: str
    HOST: str
    SS_STATIC_PASSWORD: str
    SS_STATIC_PORT: int

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()