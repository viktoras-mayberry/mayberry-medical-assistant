"""
Medical Knowledge Base Models
Defines the structure for medical knowledge storage and relationships
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# Association tables for many-to-many relationships
symptom_disease_association = Table(
    'symptom_disease_mapping',
    Base.metadata,
    Column('symptom_id', String, ForeignKey('symptoms.id'), primary_key=True),
    Column('disease_id', String, ForeignKey('diseases.id'), primary_key=True),
    Column('probability_weight', Float, default=0.5),
    Column('severity_modifier', Float, default=1.0)
)

disease_treatment_association = Table(
    'disease_treatment_mapping',
    Base.metadata,
    Column('disease_id', String, ForeignKey('diseases.id'), primary_key=True),
    Column('treatment_id', String, ForeignKey('treatments.id'), primary_key=True),
    Column('effectiveness_score', Float, default=0.5),
    Column('recommendation_level', String, default='standard')  # 'primary', 'secondary', 'alternative'
)

drug_interaction_association = Table(
    'drug_interaction_mapping',
    Base.metadata,
    Column('drug_a_id', String, ForeignKey('medications.id'), primary_key=True),
    Column('drug_b_id', String, ForeignKey('medications.id'), primary_key=True),
    Column('interaction_severity', String),  # 'mild', 'moderate', 'severe', 'contraindicated'
    Column('interaction_description', Text)
)

class MedicalSpecialty(Base):
    """Medical specialties for categorizing diseases and treatments"""
    __tablename__ = "medical_specialties"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    diseases = relationship("Disease", back_populates="specialty")
    treatments = relationship("Treatment", back_populates="specialty")

class Symptom(Base):
    """Individual symptoms with detailed information"""
    __tablename__ = "symptoms"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    category = Column(String)  # 'physical', 'psychological', 'behavioral'
    body_system = Column(String)  # 'respiratory', 'cardiovascular', 'neurological', etc.
    severity_scale = Column(String)  # 'mild_moderate_severe', 'numeric_1_10', etc.
    common_triggers = Column(Text)  # JSON string
    red_flags = Column(Text)  # JSON string - warning signs
    is_emergency_symptom = Column(Boolean, default=False)
    prevalence_rate = Column(Float)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    diseases = relationship("Disease", secondary=symptom_disease_association, back_populates="symptoms")

class Disease(Base):
    """Diseases and medical conditions"""
    __tablename__ = "diseases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    icd_10_code = Column(String)  # International Classification of Diseases
    snomed_ct_code = Column(String)  # SNOMED CT code
    description = Column(Text)
    causes = Column(Text)  # JSON string
    risk_factors = Column(Text)  # JSON string
    complications = Column(Text)  # JSON string
    prognosis = Column(Text)
    prevalence = Column(Float)  # Population prevalence rate
    mortality_rate = Column(Float)
    age_group_affected = Column(String)  # 'children', 'adults', 'elderly', 'all'
    gender_bias = Column(String)  # 'male', 'female', 'none'
    severity_level = Column(String)  # 'mild', 'moderate', 'severe', 'critical'
    is_chronic = Column(Boolean, default=False)
    is_contagious = Column(Boolean, default=False)
    specialty_id = Column(String, ForeignKey("medical_specialties.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    specialty = relationship("MedicalSpecialty", back_populates="diseases")
    symptoms = relationship("Symptom", secondary=symptom_disease_association, back_populates="diseases")
    treatments = relationship("Treatment", secondary=disease_treatment_association, back_populates="diseases")
    lab_markers = relationship("LabMarker", back_populates="disease")

class Treatment(Base):
    """Treatment options including medications, procedures, lifestyle changes"""
    __tablename__ = "treatments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String)  # 'medication', 'procedure', 'lifestyle', 'therapy'
    description = Column(Text)
    indications = Column(Text)  # When to use
    contraindications = Column(Text)  # When not to use
    side_effects = Column(Text)  # JSON string
    dosage_guidelines = Column(Text)
    effectiveness_rate = Column(Float)  # 0.0 to 1.0
    cost_category = Column(String)  # 'low', 'medium', 'high'
    requires_prescription = Column(Boolean, default=False)
    specialty_id = Column(String, ForeignKey("medical_specialties.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    specialty = relationship("MedicalSpecialty", back_populates="treatments")
    diseases = relationship("Disease", secondary=disease_treatment_association, back_populates="treatments")

class Medication(Base):
    """Specific medications with detailed information"""
    __tablename__ = "medications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    generic_name = Column(String, nullable=False)
    brand_names = Column(Text)  # JSON string
    drug_class = Column(String)
    mechanism_of_action = Column(Text)
    indications = Column(Text)  # JSON string
    contraindications = Column(Text)  # JSON string
    side_effects = Column(Text)  # JSON string
    drug_interactions = Column(Text)  # JSON string
    dosage_forms = Column(Text)  # JSON string - tablets, capsules, injection, etc.
    pregnancy_category = Column(String)  # A, B, C, D, X
    requires_monitoring = Column(Boolean, default=False)
    is_controlled_substance = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LabMarker(Base):
    """Laboratory test markers and normal ranges"""
    __tablename__ = "lab_markers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    test_type = Column(String)  # 'blood', 'urine', 'stool', 'csf', etc.
    units = Column(String)  # mg/dL, mmol/L, etc.
    normal_range_min = Column(Float)
    normal_range_max = Column(Float)
    normal_range_text = Column(String)  # For non-numeric ranges
    critical_low = Column(Float)
    critical_high = Column(Float)
    age_dependent = Column(Boolean, default=False)
    gender_dependent = Column(Boolean, default=False)
    clinical_significance = Column(Text)
    disease_id = Column(String, ForeignKey("diseases.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    disease = relationship("Disease", back_populates="lab_markers")

class MedicalGuideline(Base):
    """Evidence-based medical guidelines and protocols"""
    __tablename__ = "medical_guidelines"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    organization = Column(String)  # WHO, AHA, AMA, etc.
    version = Column(String)
    publication_date = Column(DateTime)
    last_updated = Column(DateTime)
    evidence_level = Column(String)  # 'A', 'B', 'C' based on strength of evidence
    guideline_type = Column(String)  # 'diagnosis', 'treatment', 'prevention', 'screening'
    content = Column(Text)
    references = Column(Text)  # JSON string
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicalKnowledgeSource(Base):
    """Track sources of medical knowledge for citation and credibility"""
    __tablename__ = "knowledge_sources"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String)  # 'journal', 'database', 'organization', 'textbook'
    url = Column(String)
    credibility_score = Column(Float)  # 0.0 to 1.0
    last_accessed = Column(DateTime)
    is_peer_reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DrugInteraction(Base):
    """Drug-drug interactions with severity levels"""
    __tablename__ = "drug_interactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    drug_a_id = Column(String, ForeignKey("medications.id"), nullable=False)
    drug_b_id = Column(String, ForeignKey("medications.id"), nullable=False)
    interaction_type = Column(String)  # 'major', 'moderate', 'minor', 'contraindicated'
    severity_level = Column(Integer)  # 1-5 scale
    mechanism = Column(Text)  # How the interaction occurs
    clinical_effect = Column(Text)  # What happens clinically
    management = Column(Text)  # How to manage the interaction
    evidence_level = Column(String)  # 'established', 'probable', 'suspected'
    onset = Column(String)  # 'rapid', 'delayed'
    documentation = Column(String)  # 'excellent', 'good', 'fair', 'poor'
    created_at = Column(DateTime, default=datetime.utcnow)

class ClinicalTrial(Base):
    """Clinical trials and research data"""
    __tablename__ = "clinical_trials"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nct_number = Column(String, unique=True)  # ClinicalTrials.gov identifier
    title = Column(String, nullable=False)
    status = Column(String)  # 'recruiting', 'completed', 'terminated', etc.
    phase = Column(String)  # 'Phase I', 'Phase II', etc.
    study_type = Column(String)  # 'interventional', 'observational'
    condition = Column(String)
    intervention = Column(Text)
    primary_outcome = Column(Text)
    enrollment = Column(Integer)
    start_date = Column(DateTime)
    completion_date = Column(DateTime)
    sponsor = Column(String)
    results_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class DifferentialDiagnosis(Base):
    """Differential diagnosis relationships"""
    __tablename__ = "differential_diagnoses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    primary_disease_id = Column(String, ForeignKey("diseases.id"), nullable=False)
    differential_disease_id = Column(String, ForeignKey("diseases.id"), nullable=False)
    similarity_score = Column(Float)  # 0.0 to 1.0
    distinguishing_features = Column(Text)  # JSON string
    key_differences = Column(Text)  # What sets them apart
    diagnostic_tests = Column(Text)  # Tests to differentiate
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicalProcedure(Base):
    """Medical procedures and diagnostic tests"""
    __tablename__ = "medical_procedures"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    cpt_code = Column(String)  # Current Procedural Terminology code
    category = Column(String)  # 'diagnostic', 'therapeutic', 'preventive'
    body_system = Column(String)
    description = Column(Text)
    indications = Column(Text)  # When to perform
    contraindications = Column(Text)  # When not to perform
    preparation = Column(Text)  # Patient preparation required
    procedure_steps = Column(Text)  # How it's performed
    risks = Column(Text)  # Potential complications
    normal_results = Column(Text)  # What normal results look like
    abnormal_results = Column(Text)  # What abnormal results indicate
    recovery_time = Column(String)
    cost_category = Column(String)  # 'low', 'medium', 'high', 'very_high'
    requires_anesthesia = Column(Boolean, default=False)
    is_invasive = Column(Boolean, default=False)
    specialty_id = Column(String, ForeignKey("medical_specialties.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class RiskFactor(Base):
    """Risk factors for diseases"""
    __tablename__ = "risk_factors"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    category = Column(String)  # 'modifiable', 'non_modifiable', 'genetic'
    description = Column(Text)
    relative_risk = Column(Float)  # How much it increases risk
    population_prevalence = Column(Float)  # How common in population
    evidence_level = Column(String)  # 'strong', 'moderate', 'weak'
    created_at = Column(DateTime, default=datetime.utcnow)

# Association table for diseases and risk factors
disease_risk_factor_association = Table(
    'disease_risk_factors',
    Base.metadata,
    Column('disease_id', String, ForeignKey('diseases.id'), primary_key=True),
    Column('risk_factor_id', String, ForeignKey('risk_factors.id'), primary_key=True),
    Column('risk_magnitude', Float, default=1.0),  # How much this factor increases risk for this disease
    Column('evidence_quality', String, default='moderate')  # 'high', 'moderate', 'low'
)

class PreventiveMeasure(Base):
    """Preventive measures for diseases"""
    __tablename__ = "preventive_measures"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String)  # 'primary', 'secondary', 'tertiary'
    category = Column(String)  # 'lifestyle', 'screening', 'vaccination', 'medication'
    description = Column(Text)
    target_population = Column(String)  # Who should follow this measure
    frequency = Column(String)  # How often to do it
    effectiveness = Column(Float)  # 0.0 to 1.0
    evidence_level = Column(String)  # 'A', 'B', 'C', 'D'
    cost_effectiveness = Column(String)  # 'high', 'moderate', 'low'
    created_at = Column(DateTime, default=datetime.utcnow)

# Association table for diseases and preventive measures
disease_prevention_association = Table(
    'disease_prevention',
    Base.metadata,
    Column('disease_id', String, ForeignKey('diseases.id'), primary_key=True),
    Column('preventive_measure_id', String, ForeignKey('preventive_measures.id'), primary_key=True),
    Column('prevention_effectiveness', Float, default=0.5),
    Column('recommendation_strength', String, default='moderate')  # 'strong', 'moderate', 'weak'
)

class SymptomCluster(Base):
    """Groups of symptoms that commonly occur together"""
    __tablename__ = "symptom_clusters"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # 'syndrome', 'constellation', 'pattern'
    clinical_significance = Column(Text)
    urgency_level = Column(String)  # 'emergency', 'urgent', 'routine'
    created_at = Column(DateTime, default=datetime.utcnow)

# Association table for symptom clusters
symptom_cluster_association = Table(
    'symptom_cluster_mapping',
    Base.metadata,
    Column('cluster_id', String, ForeignKey('symptom_clusters.id'), primary_key=True),
    Column('symptom_id', String, ForeignKey('symptoms.id'), primary_key=True),
    Column('frequency_in_cluster', Float, default=0.5),  # How often this symptom appears in this cluster
    Column('diagnostic_weight', Float, default=1.0)  # Importance for diagnosis
)
