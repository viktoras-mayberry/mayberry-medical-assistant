from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_current_active_user
from database import get_db
from models import User
from schemas import (
    ChatMessage, 
    ChatResponse, 
    SymptomInput, 
    SymptomAnalysis, 
    SecondOpinionRequest, 
    SecondOpinionResponse, 
    LabResultUpload, 
    LabAnalysis
)
from services.local_medical_ai import local_medical_ai
from services.symptom_analysis import analyze_symptoms_model

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_with_ai(message: ChatMessage, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    response = local_medical_ai.generate_response(message.content)
    return {
        "id": "chat_123",
        "content": response,
        "risk_level": "low",
        "confidence_score": 0.9,
        "recommendations": ["Consult a doctor for a full diagnosis."],
        "sources": ["WebMD", "Mayo Clinic"],
        "is_emergency": False,
        "created_at": "2025-07-30T16:11:37.382Z"
    }

@router.post("/symptom-checker", response_model=SymptomAnalysis)
def analyze_symptoms(symptom_input: SymptomInput, db: Session = Depends(get_db)):
    # Use symptom analysis service
    analysis = analyze_symptoms_model(
        symptoms=symptom_input.symptoms,
        duration=symptom_input.duration,
        severity=symptom_input.severity,
        age=symptom_input.age,
        gender=symptom_input.gender,
        additional_info=symptom_input.additional_info
    )
    return analysis

@router.post("/second-opinion", response_model=SecondOpinionResponse)
def request_second_opinion(request: SecondOpinionRequest, db: Session = Depends(get_db)):
    # Placeholder for second opinion logic
    return {
        "id": "so_123",
        "ai_opinion": "The AI agrees with the diagnosis and suggests considering alternative treatments.",
        "expert_panel": [
            {
                "doctor_name": "Dr. Emily Carter",
                "specialty": "Cardiology",
                "opinion": "I concur with the AI's assessment and recommend a follow-up with a specialist.",
                "agreement_level": "agree"
            }
        ],
        "consensus": "General agreement with the original diagnosis, but further tests are recommended.",
        "confidence_score": 0.85,
        "recommendations": ["Schedule an appointment with a cardiologist."],
        "status": "completed",
        "created_at": "2025-07-30T16:11:37.382Z"
    }

@router.post("/lab-analysis", response_model=LabAnalysis)
def analyze_lab_results(upload: LabResultUpload, db: Session = Depends(get_db)):
    # Placeholder for lab analysis logic
    return {
        "test_name": upload.test_name,
        "results": {"hemoglobin": "14.5 g/dL", "hematocrit": "42%"},
        "interpretation": "The results are within the normal range for a healthy adult male.",
        "risk_indicators": [],
        "recommendations": ["No immediate action needed."],
        "requires_followup": False,
        "confidence_score": 0.95
    }
