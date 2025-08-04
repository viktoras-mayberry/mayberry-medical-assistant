import sys
import os
from typing import List, Dict, Optional

# Add knowledge base to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from knowledge_base.service import knowledge_service
except ImportError:
    knowledge_service = None
    print("Warning: Knowledge base service not available, using fallback analysis")

def analyze_symptoms_model(symptoms, duration=None, severity=None, age=None, gender=None, additional_info=None):
    """Enhanced symptom analysis using knowledge base"""
    
    if knowledge_service:
        # Use knowledge base for intelligent analysis
        if isinstance(symptoms, str):
            symptoms = [s.strip().title() for s in symptoms.split(',')]
        elif isinstance(symptoms, list):
            symptoms = [s.strip().title() for s in symptoms]
        
        # Get analysis from knowledge base
        kb_analysis = knowledge_service.analyze_symptom_combination(
            symptoms=symptoms,
            age=age,
            gender=gender
        )
        
        # Convert to expected format
        possible_conditions = []
        for disease in kb_analysis.get('possible_diseases', []):
            possible_conditions.append({
                "name": disease['name'],
                "probability": disease['match_score'],
                "description": disease.get('description', ''),
                "icd_10_code": disease.get('icd_10_code', ''),
                "severity_level": disease.get('severity_level', 'unknown')
            })
        
        # Calculate confidence based on match scores
        confidence_score = 0.5
        if possible_conditions:
            max_match = max(c['probability'] for c in possible_conditions)
            confidence_score = min(0.95, 0.5 + (max_match * 0.4))
        
        # Enhanced recommendations based on knowledge base
        recommendations = kb_analysis.get('recommendations', [])
        
        # Add general health recommendations
        if kb_analysis.get('risk_level') != 'critical':
            recommendations.extend([
                "Stay hydrated and get adequate rest",
                "Monitor your symptoms for any changes",
                "Maintain good hygiene practices"
            ])
        
        analysis = {
            "possible_conditions": possible_conditions,
            "risk_level": kb_analysis.get('risk_level', 'low'),
            "recommendations": recommendations,
            "should_seek_immediate_care": kb_analysis.get('has_emergency_symptoms', False),
            "confidence_score": confidence_score,
            "disclaimer": "This analysis is for informational purposes only and does not constitute medical advice.",
            "knowledge_base_used": True,
            "demographic_factors": kb_analysis.get('demographic_factors', {})
        }
        
    else:
        # Fallback to original mock analysis
        import random
        possible_conditions = [
            {"name": "Common Cold", "probability": random.uniform(0.0, 0.2)},
            {"name": "Flu", "probability": random.uniform(0.0, 0.15)},
            {"name": "Allergies", "probability": random.uniform(0.0, 0.1)},
            {"name": "COVID-19", "probability": random.uniform(0.0, 0.05)}
        ]
        
        possible_conditions = sorted(possible_conditions, key=lambda x: x["probability"], reverse=True)
        risk_level = "low"
        if sum([c["probability"] for c in possible_conditions]) > 0.1:
            risk_level = "medium"
        if sum([c["probability"] for c in possible_conditions]) > 0.3:
            risk_level = "high"

        analysis = {
            "possible_conditions": possible_conditions,
            "risk_level": risk_level,
            "recommendations": [
                "Stay hydrated",
                "Rest",
                "Consult a doctor if symptoms persist"
            ],
            "should_seek_immediate_care": random.choice([False, True]),
            "confidence_score": random.uniform(0.7, 0.9),
            "disclaimer": "This analysis is for informational purposes only and does not constitute medical advice.",
            "knowledge_base_used": False
        }

    return analysis
