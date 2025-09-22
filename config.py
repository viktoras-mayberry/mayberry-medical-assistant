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
    
    # Privacy & Security Settings
    HIPAA_COMPLIANT: bool = True
    GDPR_COMPLIANT: bool = True
    LOCAL_PROCESSING_ENABLED: bool = True
    DATA_ENCRYPTION_ENABLED: bool = True
    ZERO_KNOWLEDGE_ARCHITECTURE: bool = True
    ANONYMOUS_MODE_ENABLED: bool = True
    
    # AI Model Settings
    USE_ADVANCED_AI_MODELS: bool = True
    BIOBERT_MODEL_ENABLED: bool = True
    CLINICALBERT_MODEL_ENABLED: bool = True
    PREDICTIVE_ANALYTICS_ENABLED: bool = True
    
    # Feature Flags
    MEDICAL_MEMORY_ENABLED: bool = True
    SYMPTOM_DETECTIVE_ENABLED: bool = True
    HEALTH_TIMELINE_ENABLED: bool = True
    EMERGENCY_AI_ENABLED: bool = True
    PRIVACY_DASHBOARD_ENABLED: bool = True
    INTERACTIVE_BODY_MAP_ENABLED: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
