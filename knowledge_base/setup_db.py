"""
Database Setup Script for Knowledge Base
Creates all necessary tables for the medical knowledge base
"""

from sqlalchemy import create_engine
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from knowledge_base.models import Base
try:
    from config import settings
except ImportError:
    # Fallback configuration
    class Settings:
        DATABASE_URL = "sqlite:///./mayberry_medical.db"
    settings = Settings()

def create_knowledge_base_tables():
    """Create all knowledge base tables"""
    # Use the same database as the main application
    engine = create_engine(settings.DATABASE_URL)
    
    # Create all tables defined in the knowledge base models
    Base.metadata.create_all(bind=engine)
    
    print("Knowledge base tables created successfully!")
    return engine

if __name__ == "__main__":
    create_knowledge_base_tables()
