"""
Knowledge Base API Router
Provides endpoints for accessing medical knowledge base
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database import get_db
import sys
import os

# Add knowledge base to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from knowledge_base.service import knowledge_service
except ImportError:
    knowledge_service = None

router = APIRouter()

# Pydantic models for requests/responses
class SymptomSearchResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    body_system: str
    is_emergency: bool
    prevalence_rate: Optional[float]

class DiseaseSearchResponse(BaseModel):
    id: str
    name: str
    icd_10_code: Optional[str]
    description: str
    severity_level: str
    is_contagious: bool
    prevalence: Optional[float]

class DiseasePredictionResponse(BaseModel):
    id: str
    name: str
    description: str
    match_score: float
    matching_symptoms: int
    total_symptoms: int
    severity_level: str

class MedicationInfoResponse(BaseModel):
    id: str
    generic_name: str
    brand_names: Optional[str]
    drug_class: str
    indications: Optional[str]
    contraindications: Optional[str]
    side_effects: Optional[str]
    pregnancy_category: Optional[str]

class LabInterpretationRequest(BaseModel):
    marker_name: str
    value: float

class LabInterpretationResponse(BaseModel):
    marker_name: str
    value: float
    units: Optional[str]
    normal_range: str
    interpretation: str
    status: str
    clinical_significance: Optional[str]

@router.get("/symptoms/search", response_model=List[SymptomSearchResponse])
def search_symptoms(
    query: str = Query(..., description="Search term for symptoms"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Search for symptoms by name or description"""
    if not knowledge_service:
        raise HTTPException(status_code=503, detail="Knowledge base service unavailable")
    
    try:
        results = knowledge_service.search_symptoms(query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/diseases/search", response_model=List[DiseaseSearchResponse])
def search_diseases(
    query: str = Query(..., description="Search term for diseases"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Search for diseases by name or description"""
    if not knowledge_service:
        raise HTTPException(status_code=503, detail="Knowledge base service unavailable")
    
    try:
        results = knowledge_service.search_diseases(query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/diseases/predict", response_model=List[DiseasePredictionResponse])
def predict_diseases_by_symptoms(
    symptoms: List[str],
    age: Optional[int] = None,
    gender: Optional[str] = None
):
    """Predict possible diseases based on symptoms"""
    if not knowledge_service:
        raise HTTPException(status_code=503, detail="Knowledge base service unavailable")
    
    if not symptoms:
        raise HTTPException(status_code=400, detail="At least one symptom is required")
    
    try:
        results = knowledge_service.get_diseases_by_symptoms(symptoms)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/medications/{medication_name}", response_model=MedicationInfoResponse)
def get_medication_info(medication_name: str):
    """Get detailed information about a medication"""
    if not knowledge_service:
        raise HTTPException(status_code=503, detail="Knowledge base service unavailable")
    
    try:
        result = knowledge_service.get_medication_info(medication_name)
        if not result:
            raise HTTPException(status_code=404, detail="Medication not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve medication info: {str(e)}")

@router.post("/lab/interpret", response_model=LabInterpretationResponse)
def interpret_lab_result(request: LabInterpretationRequest):
    """Interpret a laboratory test result"""
    if not knowledge_service:
        raise HTTPException(status_code=503, detail="Knowledge base service unavailable")
    
    try:
        result = knowledge_service.get_lab_marker_interpretation(
            request.marker_name, 
            request.value
        )
        if not result:
            raise HTTPException(status_code=404, detail="Lab marker not found in database")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lab interpretation failed: {str(e)}")

@router.get("/guidelines/search")
def search_guidelines(
    topic: str = Query(..., description="Topic to search for"),
    organization: Optional[str] = Query(None, description="Filter by organization")
):
    """Search for medical guidelines"""
    if not knowledge_service:
        raise HTTPException(status_code=503, detail="Knowledge base service unavailable")
    
    try:
        results = knowledge_service.get_medical_guidelines(topic, organization)
        return {"guidelines": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Guidelines search failed: {str(e)}")

@router.get("/emergency-symptoms")
def get_emergency_symptoms():
    """Get list of emergency symptoms"""
    if not knowledge_service:
        raise HTTPException(status_code=503, detail="Knowledge base service unavailable")
    
    try:
        results = knowledge_service.get_emergency_symptoms()
        return {"emergency_symptoms": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve emergency symptoms: {str(e)}")

@router.post("/analyze-symptoms")
def comprehensive_symptom_analysis(
    symptoms: List[str],
    age: Optional[int] = None,
    gender: Optional[str] = None
):
    """Comprehensive analysis of symptom combination"""
    if not knowledge_service:
        raise HTTPException(status_code=503, detail="Knowledge base service unavailable")
    
    if not symptoms:
        raise HTTPException(status_code=400, detail="At least one symptom is required")
    
    try:
        analysis = knowledge_service.analyze_symptom_combination(symptoms, age, gender)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Symptom analysis failed: {str(e)}")

@router.get("/health-check")
def knowledge_base_health():
    """Check knowledge base service health"""
    if not knowledge_service:
        return {
            "status": "unavailable",
            "message": "Knowledge base service is not available"
        }
    
    try:
        # Test basic functionality
        symptoms = knowledge_service.search_symptoms("fever", limit=1)
        return {
            "status": "healthy",
            "message": "Knowledge base service is operational",
            "test_result": f"Found {len(symptoms)} symptom(s) for test query"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Knowledge base service error: {str(e)}"
        }
