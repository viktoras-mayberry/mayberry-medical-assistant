"""
Database Population Script
This script populates the medical knowledge base with initial data.
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from knowledge_base.models import (
    Symptom, Disease, Treatment, Medication, LabMarker, MedicalGuideline, MedicalKnowledgeSource
)

try:
    from config import settings
except ImportError:
    # Fallback configuration
    class Settings:
        DATABASE_URL = "sqlite:///./mayberry_medical.db"
    settings = Settings()

# Example data - this should be replaced with real trusted data sources
def populate_symptoms(db: Session):
    symptoms = [
        Symptom(name="Fever", description="An abnormally high body temperature.", category="physical", body_system="general", severity_scale="mild_moderate_severe", prevalence_rate=0.15),
        Symptom(name="Cough", description="A sudden and often repetitively occurring reflex which helps to clear the large breathing passages of fluids, irritants, foreign particles, and microbes.", category="physical", body_system="respiratory", severity_scale="mild_moderate_severe", prevalence_rate=0.25),
    ]
    db.bulk_save_objects(symptoms)


def populate_diseases(db: Session):
    diseases = [
        Disease(name="Common Cold", icd_10_code="J00",
                description="A viral infectious disease of the upper respiratory tract that primarily affects the nose.",
                causes="Viruses like rhinoviruses.", risk_factors="Exposure to cold weather, poor immunity.",
                complications="Sinusitis, ear infections.",
                prognosis="Usually self-resolving in about 7 to 10 days.", prevalence=0.2, mortality_rate=0.0,
                age_group_affected="all", gender_bias="none", severity_level="mild", is_contagious=True),
    ]
    db.bulk_save_objects(diseases)


def populate_treatments(db: Session):
    treatments = [
        Treatment(name="Paracetamol", type="medication",
                  description="Common pain reliever and fever reducer.", indications="Fever, mild pain.",
                  side_effects="Nausea, rash.", requires_prescription=False),
    ]
    db.bulk_save_objects(treatments)


def populate_medications(db: Session):
    medications = [
        Medication(generic_name="Paracetamol", brand_names="Tylenol, Panadol",
                   drug_class="analgesic", mechanism_of_action="Inhibition of prostaglandin synthesis.",
                   indications="Fever, pain relief.", contraindications="Severe liver disease.",
                   side_effects="Elevated liver enzymes, Hepatotoxicity",
                   dosage_forms="tablet, syrup", pregnancy_category="B"),
    ]
    db.bulk_save_objects(medications)


def populate_guidelines(db: Session):
    guidelines = [
        MedicalGuideline(title="COVID-19 Treatment Guidelines",
                         organization="WHO",
                         version="1.0",
                         publication_date=datetime(2020, 4, 1),
                         evidence_level="A",
                         guideline_type="treatment",
                         content="Follow WHO protocol for COVID-19 management.",
                         is_active=True),
    ]
    db.bulk_save_objects(guidelines)


def populate_knowledge_sources(db: Session):
    sources = [
        MedicalKnowledgeSource(name="World Health Organization",
                               type="organization",
                               url="https://www.who.int",
                               credibility_score=0.99,
                               is_peer_reviewed=True),
        MedicalKnowledgeSource(name="PubMed",
                               type="database",
                               url="https://pubmed.ncbi.nlm.nih.gov",
                               credibility_score=0.95,
                               is_peer_reviewed=True),
    ]
    db.bulk_save_objects(sources)


def run_population(db: Session):
    populate_symptoms(db)
    populate_diseases(db)
    populate_treatments(db)
    populate_medications(db)
    populate_guidelines(db)
    populate_knowledge_sources(db)
    db.commit()
    print("Database population completed.")

if __name__ == "__main__":
    # Create database session
    engine = create_engine(settings.DATABASE_URL)
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        run_population(db)
    finally:
        db.close()

