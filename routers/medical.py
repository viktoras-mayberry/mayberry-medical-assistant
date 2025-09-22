from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_current_active_user
from database import get_db
from models import User
from datetime import datetime
import json
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
    # Get enhanced response from AI with user context
    ai_response = local_medical_ai.generate_response(
        message.content, 
        context={"session_id": message.session_id},
        user_id=current_user.id
    )
    
    # Determine sources based on knowledge base usage
    sources = []
    if ai_response.get('knowledge_base_used'):
        sources = ["MAYBERRY Medical Knowledge Base", "WHO Guidelines", "Medical Literature", "Clinical Research"]
    else:
        sources = ["General Medical Knowledge", "Health Guidelines"]
    
    # Add privacy and security information
    privacy_status = ai_response.get('privacy_status', {})
    
    response_data = {
        "id": f"chat_{hash(message.content) % 10000}",
        "content": ai_response.get('response', 'I apologize, but I could not process your request at this time.'),
        "risk_level": ai_response.get('risk_level', 'low'),
        "confidence_score": ai_response.get('confidence_score', 0.7),
        "recommendations": ai_response.get('recommendations', ["Consult a healthcare professional for personalized advice."]),
        "sources": sources,
        "is_emergency": ai_response.get('emergency_info', {}).get('immediate_action_required', False),
        "emergency_info": ai_response.get('emergency_info', {}),
        "emergency_response": ai_response.get('emergency_response', {}),
        "privacy_status": privacy_status,
        "medical_memory_used": ai_response.get('medical_memory_used', False),
        "ai_personality": ai_response.get('ai_personality', 'balanced'),
        "model_version": ai_response.get('model_version', 'MAYBERRY-Medical-AI-v1.0'),
        "created_at": ai_response.get('timestamp', "2025-01-04T13:05:00.000Z")
    }
    
    # Store conversation in database
    from models import Conversation
    conversation = Conversation(
        user_id=current_user.id,
        session_id=message.session_id or f"session_{current_user.id}_{int(datetime.utcnow().timestamp())}",
        message_type="user",
        content=message.content,
        risk_level=ai_response.get('risk_level'),
        confidence_score=ai_response.get('confidence_score'),
        extra_data=json.dumps(ai_response.get('extracted_entities', {}))
    )
    db.add(conversation)
    
    # Store AI response
    ai_conversation = Conversation(
        user_id=current_user.id,
        session_id=conversation.session_id,
        message_type="assistant",
        content=ai_response.get('response'),
        risk_level=ai_response.get('risk_level'),
        confidence_score=ai_response.get('confidence_score'),
        extra_data=json.dumps({
            "emergency_info": ai_response.get('emergency_info'),
            "recommendations": ai_response.get('recommendations'),
            "sources": sources
        })
    )
    db.add(ai_conversation)
    db.commit()
    
    return response_data

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
