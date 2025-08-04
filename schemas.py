from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

# User Profile schemas
class UserProfileBase(BaseModel):
    height: Optional[float] = None
    weight: Optional[float] = None
    blood_type: Optional[str] = None
    allergies: Optional[List[str]] = None
    chronic_conditions: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    family_medical_history: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    preferred_language: str = 'en'
    timezone: Optional[str] = None
    ai_interaction_style: str = 'balanced'
    risk_tolerance: str = 'moderate'
    preferred_units: str = 'metric'

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(BaseModel):
    height: Optional[float] = None
    weight: Optional[float] = None
    blood_type: Optional[str] = None
    allergies: Optional[List[str]] = None
    chronic_conditions: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    family_medical_history: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    preferred_language: Optional[str] = None
    timezone: Optional[str] = None
    ai_interaction_style: Optional[str] = None
    risk_tolerance: Optional[str] = None
    preferred_units: Optional[str] = None

class UserProfileResponse(UserProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Chat schemas
class ChatMessage(BaseModel):
    content: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    content: str
    risk_level: Optional[str] = None
    confidence_score: Optional[float] = None
    recommendations: Optional[List[str]] = None
    sources: Optional[List[str]] = None
    is_emergency: bool = False
    created_at: datetime

class ConversationHistory(BaseModel):
    id: str
    message_type: str
    content: str
    risk_level: Optional[str] = None
    confidence_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Symptom checker schemas
class SymptomInput(BaseModel):
    symptoms: List[str]
    duration: Optional[str] = None
    severity: Optional[int] = None  # 1-10 scale
    additional_info: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    session_id: Optional[str] = None

class SymptomAnalysis(BaseModel):
    possible_conditions: List[Dict[str, Any]]
    risk_level: str
    recommendations: List[str]
    should_seek_immediate_care: bool
    confidence_score: float
    disclaimer: str

# Second opinion schemas
class SecondOpinionRequest(BaseModel):
    original_diagnosis: str
    symptoms: str
    current_treatment: Optional[str] = None
    medical_history: Optional[str] = None
    additional_notes: Optional[str] = None
    session_id: Optional[str] = None

class ExpertOpinion(BaseModel):
    doctor_name: str
    specialty: str
    opinion: str
    agreement_level: str  # 'agree', 'partially_agree', 'disagree'
    additional_recommendations: Optional[List[str]] = None

class SecondOpinionResponse(BaseModel):
    id: str
    ai_opinion: str
    expert_panel: List[ExpertOpinion]
    consensus: str
    confidence_score: float
    recommendations: List[str]
    status: str
    created_at: datetime

# Lab analysis schemas
class LabResultUpload(BaseModel):
    test_name: str
    test_type: str
    file_data: Optional[str] = None  # Base64 encoded file
    raw_data: Optional[str] = None  # Manual entry
    session_id: Optional[str] = None

class LabAnalysis(BaseModel):
    test_name: str
    results: Dict[str, Any]
    interpretation: str
    risk_indicators: List[str]
    recommendations: List[str]
    requires_followup: bool
    confidence_score: float

# Health record schemas
class HealthRecordCreate(BaseModel):
    record_type: str
    title: str
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class HealthRecordResponse(BaseModel):
    id: str
    record_type: str
    title: str
    description: Optional[str] = None
    ai_analysis: Optional[str] = None
    risk_assessment: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# System schemas
class HealthStatus(BaseModel):
    status: str
    version: str
    features: Dict[str, bool]
    uptime: str

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    
class ErrorResponse(BaseModel):
    error: str
    detail: str
    code: int
