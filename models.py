from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    health_records = relationship("HealthRecord", back_populates="user")
    second_opinions = relationship("SecondOpinion", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous users
    session_id = Column(String, nullable=False)  # For anonymous sessions
    message_type = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    risk_level = Column(String, nullable=True)  # 'low', 'medium', 'high', 'critical'
    confidence_score = Column(Float, nullable=True)
    extra_data = Column(Text, nullable=True)  # JSON string for additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="conversations")

class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    record_type = Column(String, nullable=False)  # 'symptom_check', 'lab_result', 'medication'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    data = Column(Text, nullable=True)  # JSON string for structured data
    file_path = Column(String, nullable=True)  # For uploaded files
    ai_analysis = Column(Text, nullable=True)
    risk_assessment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="health_records")

class SecondOpinion(Base):
    __tablename__ = "second_opinions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    session_id = Column(String, nullable=False)
    original_diagnosis = Column(Text, nullable=False)
    symptoms = Column(Text, nullable=False)
    current_treatment = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    ai_opinion = Column(Text, nullable=True)
    expert_panel_opinion = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    recommendations = Column(Text, nullable=True)  # JSON string
    status = Column(String, default="pending")  # 'pending', 'completed', 'reviewed'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="second_opinions")

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    log_level = Column(String, nullable=False)  # 'info', 'warning', 'error', 'critical'
    message = Column(Text, nullable=False)
    user_id = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    extra_data = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
