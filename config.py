from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Core settings
    APP_NAME: str = "MAYBERRY Medical AI"
    DEBUG: bool = False
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"

    # Database settings
    DATABASE_URL: str = "sqlite:///./mayberry_medical.db"

    # JWT settings
    JWT_SECRET: str = "your-jwt-secret-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours

    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
