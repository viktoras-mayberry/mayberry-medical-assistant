"""
Knowledge Base Service
Provides intelligent medical knowledge retrieval and analysis
"""

import sys
import os
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_, or_

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from knowledge_base.models import (
    Symptom, Disease, Treatment, Medication, LabMarker, 
    MedicalGuideline, MedicalKnowledgeSource, symptom_disease_association
)

try:
    from config import settings
except ImportError:
    # Fallback configuration
    class Settings:
        DATABASE_URL = "sqlite:///./mayberry_medical.db"
    settings = Settings()

class MedicalKnowledgeService:
    """Service for accessing and analyzing medical knowledge base"""
    
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        from sqlalchemy.orm import sessionmaker
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def search_symptoms(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for symptoms by name or description"""
        db = self.get_session()
        try:
            symptoms = db.query(Symptom).filter(
                or_(
                    Symptom.name.ilike(f"%{query}%"),
                    Symptom.description.ilike(f"%{query}%")
                )
            ).limit(limit).all()
            
            return [
                {
                    "id": symptom.id,
                    "name": symptom.name,
                    "description": symptom.description,
                    "category": symptom.category,
                    "body_system": symptom.body_system,
                    "is_emergency": symptom.is_emergency_symptom,
                    "prevalence_rate": symptom.prevalence_rate
                }
                for symptom in symptoms
            ]
        finally:
            db.close()
    
    def search_diseases(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for diseases by name or description"""
        db = self.get_session()
        try:
            diseases = db.query(Disease).filter(
                or_(
                    Disease.name.ilike(f"%{query}%"),
                    Disease.description.ilike(f"%{query}%")
                )
            ).limit(limit).all()
            
            return [
                {
                    "id": disease.id,
                    "name": disease.name,
                    "icd_10_code": disease.icd_10_code,
                    "description": disease.description,
                    "severity_level": disease.severity_level,
                    "is_contagious": disease.is_contagious,
                    "prevalence": disease.prevalence
                }
                for disease in diseases
            ]
        finally:
            db.close()
    
    def get_diseases_by_symptoms(self, symptom_names: List[str]) -> List[Dict]:
        """Get possible diseases based on a list of symptoms"""
        db = self.get_session()
        try:
            # Find symptoms that match the input
            symptoms = db.query(Symptom).filter(
                Symptom.name.in_(symptom_names)
            ).all()
            
            if not symptoms:
                return []
            
            # Get diseases associated with these symptoms
            symptom_ids = [s.id for s in symptoms]
            
            # Query diseases with symptom associations
            diseases_query = db.query(Disease).join(symptom_disease_association).filter(
                symptom_disease_association.c.symptom_id.in_(symptom_ids)
            ).all()
            
            # Calculate match scores based on number of matching symptoms
            disease_scores = {}
            for disease in diseases_query:
                matching_symptoms = len([s for s in disease.symptoms if s.name in symptom_names])
                total_symptoms = len(symptom_names)
                score = matching_symptoms / total_symptoms if total_symptoms > 0 else 0
                
                disease_scores[disease.id] = {
                    "disease": disease,
                    "match_score": score,
                    "matching_symptoms": matching_symptoms,
                    "total_symptoms": total_symptoms
                }
            
            # Sort by match score
            sorted_diseases = sorted(disease_scores.values(), key=lambda x: x["match_score"], reverse=True)
            
            return [
                {
                    "id": item["disease"].id,
                    "name": item["disease"].name,
                    "description": item["disease"].description,
                    "icd_10_code": item["disease"].icd_10_code,
                    "severity_level": item["disease"].severity_level,
                    "match_score": item["match_score"],
                    "matching_symptoms": item["matching_symptoms"],
                    "total_symptoms": item["total_symptoms"],
                    "prevalence": item["disease"].prevalence,
                    "is_contagious": item["disease"].is_contagious
                }
                for item in sorted_diseases
            ]
        finally:
            db.close()
    
    def get_treatments_for_disease(self, disease_name: str) -> List[Dict]:
        """Get treatment options for a specific disease"""
        db = self.get_session()
        try:
            disease = db.query(Disease).filter(Disease.name.ilike(f"%{disease_name}%")).first()
            if not disease:
                return []
            
            treatments = disease.treatments
            return [
                {
                    "id": treatment.id,
                    "name": treatment.name,
                    "type": treatment.type,
                    "description": treatment.description,
                    "effectiveness_rate": treatment.effectiveness_rate,
                    "requires_prescription": treatment.requires_prescription,
                    "cost_category": treatment.cost_category
                }
                for treatment in treatments
            ]
        finally:
            db.close()
    
    def get_medication_info(self, medication_name: str) -> Optional[Dict]:
        """Get detailed information about a medication"""
        db = self.get_session()
        try:
            medication = db.query(Medication).filter(
                or_(
                    Medication.generic_name.ilike(f"%{medication_name}%"),
                    Medication.brand_names.ilike(f"%{medication_name}%")
                )
            ).first()
            
            if not medication:
                return None
            
            return {
                "id": medication.id,
                "generic_name": medication.generic_name,
                "brand_names": medication.brand_names,
                "drug_class": medication.drug_class,
                "mechanism_of_action": medication.mechanism_of_action,
                "indications": medication.indications,
                "contraindications": medication.contraindications,
                "side_effects": medication.side_effects,
                "pregnancy_category": medication.pregnancy_category,
                "requires_monitoring": medication.requires_monitoring,
                "is_controlled_substance": medication.is_controlled_substance
            }
        finally:
            db.close()
    
    def get_lab_marker_interpretation(self, marker_name: str, value: float) -> Optional[Dict]:
        """Interpret lab test results"""
        db = self.get_session()
        try:
            marker = db.query(LabMarker).filter(
                LabMarker.name.ilike(f"%{marker_name}%")
            ).first()
            
            if not marker:
                return None
            
            interpretation = "normal"
            status = "within_range"
            
            if marker.critical_low and value < marker.critical_low:
                interpretation = "critically_low"
                status = "critical"
            elif marker.critical_high and value > marker.critical_high:
                interpretation = "critically_high"
                status = "critical"
            elif marker.normal_range_min and value < marker.normal_range_min:
                interpretation = "low"
                status = "abnormal"
            elif marker.normal_range_max and value > marker.normal_range_max:
                interpretation = "high"
                status = "abnormal"
            
            return {
                "marker_name": marker.name,
                "value": value,
                "units": marker.units,
                "normal_range": f"{marker.normal_range_min}-{marker.normal_range_max}",
                "interpretation": interpretation,
                "status": status,
                "clinical_significance": marker.clinical_significance
            }
        finally:
            db.close()
    
    def get_medical_guidelines(self, topic: str, organization: str = None) -> List[Dict]:
        """Get medical guidelines for a specific topic"""
        db = self.get_session()
        try:
            query = db.query(MedicalGuideline).filter(
                MedicalGuideline.title.ilike(f"%{topic}%"),
                MedicalGuideline.is_active == True
            )
            
            if organization:
                query = query.filter(MedicalGuideline.organization.ilike(f"%{organization}%"))
            
            guidelines = query.all()
            
            return [
                {
                    "id": guideline.id,
                    "title": guideline.title,
                    "organization": guideline.organization,
                    "version": guideline.version,
                    "evidence_level": guideline.evidence_level,
                    "guideline_type": guideline.guideline_type,
                    "content": guideline.content,
                    "publication_date": guideline.publication_date.isoformat() if guideline.publication_date else None
                }
                for guideline in guidelines
            ]
        finally:
            db.close()
    
    def get_emergency_symptoms(self) -> List[Dict]:
        """Get list of emergency symptoms"""
        db = self.get_session()
        try:
            symptoms = db.query(Symptom).filter(
                Symptom.is_emergency_symptom == True
            ).all()
            
            return [
                {
                    "name": symptom.name,
                    "description": symptom.description,
                    "body_system": symptom.body_system,
                    "red_flags": symptom.red_flags
                }
                for symptom in symptoms
            ]
        finally:
            db.close()
    
    def analyze_symptom_combination(self, symptoms: List[str], age: int = None, gender: str = None) -> Dict:
        """Analyze a combination of symptoms with demographic factors"""
        diseases = self.get_diseases_by_symptoms(symptoms)
        emergency_symptoms = self.get_emergency_symptoms()
        emergency_symptom_names = [es["name"] for es in emergency_symptoms]
        
        # Check for emergency symptoms
        has_emergency_symptoms = any(symptom in emergency_symptom_names for symptom in symptoms)
        
        # Calculate overall risk level
        risk_level = "low"
        if has_emergency_symptoms:
            risk_level = "critical"
        elif diseases and max(d["match_score"] for d in diseases) > 0.7:
            risk_level = "high"
        elif diseases and max(d["match_score"] for d in diseases) > 0.4:
            risk_level = "medium"
        
        # Generate recommendations
        recommendations = []
        if has_emergency_symptoms:
            recommendations.append("Seek immediate emergency medical attention")
        elif risk_level == "high":
            recommendations.append("Consult with a healthcare provider as soon as possible")
        elif risk_level == "medium":
            recommendations.append("Consider scheduling an appointment with your doctor")
        else:
            recommendations.append("Monitor symptoms and seek medical advice if they worsen")
        
        return {
            "symptoms": symptoms,
            "possible_diseases": diseases[:5],  # Top 5 matches
            "risk_level": risk_level,
            "has_emergency_symptoms": has_emergency_symptoms,
            "recommendations": recommendations,
            "demographic_factors": {
                "age": age,
                "gender": gender
            }
        }

# Singleton instance
knowledge_service = MedicalKnowledgeService()
