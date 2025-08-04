"""
Data Retrieval and Testing Script
Verify access to the populated knowledge base
"""

import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from knowledge_base.models import Symptom, Disease, Treatment

try:
    from config import settings
except ImportError:
    # Fallback configuration
    class Settings:
        DATABASE_URL = "sqlite:///./mayberry_medical.db"
    settings = Settings()

def test_data_retrieval(db: Session):
    """Retrieve and verify data from the knowledge base"""
    print("Retrieving symptoms...")
    symptoms = db.query(Symptom).all()
    for symptom in symptoms:
        print(f"Symptom: {symptom.name}, Description: {symptom.description}")
    
    print("\nRetrieving diseases...")
    diseases = db.query(Disease).all()
    for disease in diseases:
        print(f"Disease: {disease.name}, ICD-10 Code: {disease.icd_10_code}")
    
    print("\nRetrieving treatments...")
    treatments = db.query(Treatment).all()
    for treatment in treatments:
        print(f"Treatment: {treatment.name}, Type: {treatment.type}")

if __name__ == "__main__":
    # Create database session
    engine = create_engine(settings.DATABASE_URL)
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        test_data_retrieval(db)
    finally:
        db.close()
