from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    database_url: str = "sqlite:///./sentinelai.db"
    secret_key: str = "sentinelai-secret"

settings = Settings()


