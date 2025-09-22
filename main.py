from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from config import settings
from database import engine
from models import Base
from routers import auth, medical, knowledge, privacy
from schemas import HealthStatus
import time

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="MAYBERRY Medical AI - Your trusted partner for intelligent healthcare guidance",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Store app start time for uptime calculation
start_time = time.time()

# Set up CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(medical.router, prefix="/medical", tags=["medical"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge-base"])
app.include_router(privacy.router, prefix="/privacy", tags=["privacy-security"])

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthStatus)
def health_check():
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    
    uptime_str = f"{uptime_days}d {uptime_hours % 24}h {uptime_minutes % 60}m {uptime_seconds % 60}s"
    
    return {
        "status": "healthy",
        "version": "2.0.0",
        "features": {
            "authentication": True,
            "medical_chat": True,
            "symptom_checker": True,
            "second_opinion": True,
            "lab_analysis": True,
            "local_ai": True,
            "privacy_dashboard": settings.PRIVACY_DASHBOARD_ENABLED,
            "medical_memory": settings.MEDICAL_MEMORY_ENABLED,
            "emergency_ai": settings.EMERGENCY_AI_ENABLED,
            "interactive_body_map": settings.INTERACTIVE_BODY_MAP_ENABLED,
            "advanced_ai_models": settings.USE_ADVANCED_AI_MODELS,
            "hipaa_compliant": settings.HIPAA_COMPLIANT,
            "gdpr_compliant": settings.GDPR_COMPLIANT,
            "local_processing": settings.LOCAL_PROCESSING_ENABLED,
            "zero_knowledge_architecture": settings.ZERO_KNOWLEDGE_ARCHITECTURE
        },
        "uptime": uptime_str
    }

