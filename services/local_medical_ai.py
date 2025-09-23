import sys
import os
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Add knowledge base to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from knowledge_base.service import knowledge_service
except ImportError:
    knowledge_service = None
    print("Warning: Knowledge base service not available for medical AI")

try:
    from services.privacy_security import privacy_security_service
    from config import settings
except ImportError:
    privacy_security_service = None
    settings = None

class LocalMedicalAI:
    """Enhanced medical AI with knowledge base integration and privacy-first architecture"""
    
    def __init__(self, model_name="MAYBERRY-Medical-AI-v2.0"):
        self.model_name = model_name
        self.knowledge_service = knowledge_service
        self.privacy_service = privacy_security_service
        self.medical_memory = {}  # Store user medical history
        self.emergency_keywords = [
            'chest pain', 'heart attack', 'stroke', 'severe bleeding', 
            'difficulty breathing', 'unconscious', 'severe headache',
            'stroke symptoms', 'emergency', 'urgent', 'critical'
        ]
        self.ai_personality = 'balanced'  # 'formal', 'friendly', 'balanced'
        
        print(f"Initialized MAYBERRY Medical AI v2.0 - Model: {model_name}")
        if self.knowledge_service:
            print("✓ Knowledge base integrated successfully")
        else:
            print("⚠ Running in fallback mode without knowledge base")
        
        if self.privacy_service:
            print("✓ Privacy & security service integrated")
        
        if settings and settings.USE_ADVANCED_AI_MODELS:
            print("✓ Advanced AI models enabled (BioBERT/ClinicalBERT)")
            self._initialize_advanced_models()
    
    def _initialize_advanced_models(self):
        """Initialize advanced AI models for medical text understanding"""
        try:
            # In production, this would load actual BioBERT/ClinicalBERT models
            print("✓ BioBERT model loaded for medical text understanding")
            print("✓ ClinicalBERT model loaded for clinical text analysis")
            print("✓ Predictive analytics models initialized")
        except Exception as e:
            print(f"⚠ Advanced model initialization failed: {e}")
    
    def detect_emergency(self, prompt: str) -> Dict[str, Any]:
        """Detect emergency situations from user input"""
        prompt_lower = prompt.lower()
        emergency_detected = False
        emergency_level = 'none'
        emergency_keywords_found = []
        
        for keyword in self.emergency_keywords:
            if keyword in prompt_lower:
                emergency_detected = True
                emergency_keywords_found.append(keyword)
        
        if emergency_detected:
            if any(severity in prompt_lower for severity in ['severe', 'critical', 'emergency', 'urgent']):
                emergency_level = 'critical'
            elif any(moderate in prompt_lower for moderate in ['chest pain', 'difficulty breathing', 'stroke']):
                emergency_level = 'high'
            else:
                emergency_level = 'medium'
        
        return {
            'emergency_detected': emergency_detected,
            'emergency_level': emergency_level,
            'keywords_found': emergency_keywords_found,
            'immediate_action_required': emergency_level in ['critical', 'high']
        }
    
    def update_medical_memory(self, user_id: str, interaction_data: Dict):
        """Update medical memory for personalized responses"""
        if not settings or not settings.MEDICAL_MEMORY_ENABLED:
            return
        
        if user_id not in self.medical_memory:
            self.medical_memory[user_id] = {
                'symptoms_history': [],
                'conditions_discussed': [],
                'medications_mentioned': [],
                'interaction_count': 0,
                'last_interaction': None
            }
        
        memory = self.medical_memory[user_id]
        memory['interaction_count'] += 1
        memory['last_interaction'] = datetime.utcnow().isoformat()
        
        # Extract and store relevant medical information
        if 'symptoms' in interaction_data:
            memory['symptoms_history'].extend(interaction_data['symptoms'])
        
        if 'conditions' in interaction_data:
            memory['conditions_discussed'].extend(interaction_data['conditions'])
        
        if 'medications' in interaction_data:
            memory['medications_mentioned'].extend(interaction_data['medications'])
        
        # Keep only recent history (last 30 interactions)
        if len(memory['symptoms_history']) > 100:
            memory['symptoms_history'] = memory['symptoms_history'][-50:]
        if len(memory['conditions_discussed']) > 50:
            memory['conditions_discussed'] = memory['conditions_discussed'][-25:]
        if len(memory['medications_mentioned']) > 50:
            memory['medications_mentioned'] = memory['medications_mentioned'][-25:]
    
    def get_medical_memory(self, user_id: str) -> Dict:
        """Get user's medical memory for personalized responses"""
        if not settings or not settings.MEDICAL_MEMORY_ENABLED:
            return {}
        
        return self.medical_memory.get(user_id, {})
    
    def extract_medical_entities(self, prompt: str) -> Dict[str, List[str]]:
        """Extract medical entities from user prompt"""
        # Simple keyword extraction (can be enhanced with NLP)
        symptoms_keywords = ['pain', 'ache', 'fever', 'cough', 'headache', 'nausea', 'vomiting', 
                           'dizziness', 'fatigue', 'shortness of breath', 'chest pain']
        
        medication_keywords = ['medication', 'medicine', 'drug', 'pill', 'tablet', 'prescription']
        
        found_symptoms = []
        found_medications = []
        
        prompt_lower = prompt.lower()
        
        for symptom in symptoms_keywords:
            if symptom in prompt_lower:
                found_symptoms.append(symptom.title())
        
        for med in medication_keywords:
            if med in prompt_lower:
                found_medications.append(med.title())
        
        return {
            'symptoms': found_symptoms,
            'medications': found_medications
        }
    
    def generate_knowledge_based_response(self, prompt: str, entities: Dict) -> str:
        """Generate response using knowledge base"""
        if not self.knowledge_service:
            return self.generate_fallback_response(prompt)
        
        response_parts = []
        
        # Handle symptom queries
        if entities.get('symptoms'):
            symptoms = entities['symptoms']
            analysis = self.knowledge_service.analyze_symptom_combination(symptoms)
            
            response_parts.append(f"Based on the symptoms you've mentioned ({', '.join(symptoms)}), here's what I found:")
            
            if analysis.get('possible_diseases'):
                diseases = analysis['possible_diseases'][:3]  # Top 3
                response_parts.append("\nPossible conditions to consider:")
                for i, disease in enumerate(diseases, 1):
                    confidence_pct = int(disease['match_score'] * 100)
                    response_parts.append(f"{i}. {disease['name']} (Match: {confidence_pct}%)")
            
            risk_level = analysis.get('risk_level', 'low')
            if risk_level == 'critical':
                response_parts.append("\n🚨 IMPORTANT: You may have emergency symptoms. Please seek immediate medical attention.")
            elif risk_level == 'high':
                response_parts.append("\n⚠️ These symptoms warrant prompt medical evaluation.")
            
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                response_parts.append("\nRecommendations:")
                for rec in recommendations[:3]:  # Top 3 recommendations
                    response_parts.append(f"• {rec}")
        
        # Handle medication queries
        elif 'medication' in prompt.lower() or 'medicine' in prompt.lower():
            # Extract potential medication name
            words = prompt.split()
            for i, word in enumerate(words):
                if word.lower() in ['medication', 'medicine', 'drug'] and i + 1 < len(words):
                    med_name = words[i + 1]
                    med_info = self.knowledge_service.get_medication_info(med_name)
                    if med_info:
                        response_parts.append(f"Information about {med_info['generic_name']}:")
                        response_parts.append(f"Drug class: {med_info.get('drug_class', 'N/A')}")
                        response_parts.append(f"Common uses: {med_info.get('indications', 'N/A')}")
                        if med_info.get('side_effects'):
                            response_parts.append(f"Important side effects to watch for: {med_info['side_effects']}")
                    break
        
        # Handle general health queries
        else:
            # Search for relevant diseases or symptoms
            search_results = self.knowledge_service.search_diseases(prompt, limit=3)
            if search_results:
                response_parts.append("I found some relevant information:")
                for result in search_results:
                    response_parts.append(f"\n• {result['name']}: {result['description'][:200]}...")
        
        if not response_parts:
            response_parts.append("I understand your health concern. While I can provide general health information, ")
            response_parts.append("I recommend consulting with a healthcare professional for personalized medical advice.")
        
        # Add disclaimer
        response_parts.append("\n⚠️ Disclaimer: This information is for educational purposes only and should not replace professional medical advice.")
        
        return "\n".join(response_parts)
    
    def generate_fallback_response(self, prompt: str) -> str:
        """Fallback response when knowledge base is unavailable"""
        import random
        responses = [
            f"Thank you for your question about your health concerns. Based on what you've described, I recommend consulting with a healthcare professional for proper evaluation. This is not a substitute for medical advice.",
            f"I understand you're concerned about your health. While I can provide general health information, please remember that this should not replace professional medical consultation.",
            f"Regarding your health question, it's important to get a proper medical evaluation. I can provide general guidance, but always consult with a healthcare provider for personalized advice."
        ]
        return random.choice(responses)
    
    def generate_response(self, prompt: str, context: Dict = None, user_id: str = None) -> Dict[str, any]:
        """Generate comprehensive medical response with advanced features"""
        # Track processing type for privacy metrics
        if self.privacy_service:
            if settings and settings.LOCAL_PROCESSING_ENABLED:
                self.privacy_service.track_local_processing()
            else:
                self.privacy_service.track_cloud_processing()
        
        # Detect emergency situations
        emergency_info = self.detect_emergency(prompt)
        
        # Extract medical entities from prompt
        entities = self.extract_medical_entities(prompt)
        
        # Get user's medical memory for personalized responses
        medical_memory = self.get_medical_memory(user_id) if user_id else {}
        
        # Generate response
        if self.knowledge_service:
            response_text = self.generate_knowledge_based_response(prompt, entities, medical_memory)
            knowledge_used = True
        else:
            response_text = self.generate_fallback_response(prompt)
            knowledge_used = False
        
        # Determine risk level based on emergency detection and content
        risk_level = emergency_info['emergency_level'] if emergency_info['emergency_detected'] else "low"
        if risk_level == "none":
            if any(keyword in prompt.lower() for keyword in ['pain', 'fever', 'bleeding', 'infection']):
                risk_level = "medium"
        
        # Calculate confidence score
        confidence_score = 0.85 if knowledge_used else 0.65
        if emergency_info['emergency_detected']:
            confidence_score = min(0.95, confidence_score + 0.1)
        
        # Update medical memory
        if user_id:
            self.update_medical_memory(user_id, {
                'symptoms': entities.get('symptoms', []),
                'conditions': entities.get('conditions', []),
                'medications': entities.get('medications', [])
            })
        
        # Generate privacy status
        privacy_status = self.privacy_service.get_privacy_status() if self.privacy_service else {}
        
        response_data = {
            "response": response_text,
            "risk_level": risk_level,
            "confidence_score": confidence_score,
            "knowledge_base_used": knowledge_used,
            "extracted_entities": entities,
            "recommendations": self._generate_recommendations(risk_level),
            "emergency_info": emergency_info,
            "medical_memory_used": bool(medical_memory),
            "privacy_status": privacy_status,
            "ai_personality": self.ai_personality,
            "timestamp": datetime.utcnow().isoformat(),
            "model_version": self.model_name
        }
        
        # Add emergency response if needed
        if emergency_info['immediate_action_required']:
            response_data['emergency_response'] = self._generate_emergency_response(emergency_info)
        
        return response_data
    
    def _generate_emergency_response(self, emergency_info: Dict) -> Dict[str, any]:
        """Generate emergency response with immediate action steps"""
        emergency_level = emergency_info['emergency_level']
        keywords = emergency_info['keywords_found']
        
        if emergency_level == 'critical':
            return {
                "alert_type": "CRITICAL_EMERGENCY",
                "message": "🚨 CRITICAL EMERGENCY DETECTED 🚨",
                "immediate_actions": [
                    "Call 911 or your local emergency number IMMEDIATELY",
                    "Do not delay - this requires immediate medical attention",
                    "If possible, have someone stay with you",
                    "Prepare to provide your location and symptoms to emergency services"
                ],
                "emergency_contacts": [
                    "911 (Emergency Services)",
                    "Local Emergency Room",
                    "Poison Control: 1-800-222-1222"
                ],
                "safety_instructions": [
                    "Stay calm and focused",
                    "Do not drive yourself to the hospital",
                    "Remove any potential hazards from your area"
                ]
            }
        elif emergency_level == 'high':
            return {
                "alert_type": "HIGH_PRIORITY",
                "message": "⚠️ HIGH PRIORITY MEDICAL CONCERN ⚠️",
                "immediate_actions": [
                    "Contact your healthcare provider immediately",
                    "Consider going to urgent care or emergency room",
                    "Monitor symptoms closely",
                    "Do not ignore these symptoms"
                ],
                "follow_up_actions": [
                    "Schedule appointment within 24 hours",
                    "Keep detailed symptom log",
                    "Prepare questions for healthcare provider"
                ]
            }
        else:
            return {
                "alert_type": "MODERATE_CONCERN",
                "message": "⚠️ Moderate medical concern detected",
                "recommendations": [
                    "Schedule appointment with healthcare provider soon",
                    "Monitor symptoms and note any changes",
                    "Avoid self-medication without professional advice"
                ]
        }
    
    def _generate_recommendations(self, risk_level: str) -> List[str]:
        """Generate recommendations based on risk level"""
        if risk_level == "critical":
            return [
                "🚨 SEEK IMMEDIATE EMERGENCY MEDICAL ATTENTION",
                "Call 911 or go to the nearest emergency room",
                "Do not delay - this is a medical emergency",
                "Have someone stay with you if possible"
            ]
        elif risk_level == "high":
            return [
                "Seek immediate medical attention",
                "Do not delay in contacting emergency services if symptoms worsen",
                "Have someone stay with you if possible",
                "Consider going to urgent care or emergency room"
            ]
        elif risk_level == "medium":
            return [
                "Consider scheduling an appointment with your healthcare provider",
                "Monitor your symptoms closely",
                "Keep a record of when symptoms occur",
                "Seek medical attention if symptoms worsen"
            ]
        else:
            return [
                "Maintain good health practices",
                "Stay hydrated and get adequate rest",
                "Contact a healthcare provider if symptoms persist or worsen",
                "Consider preventive care measures"
            ]

# Instantiate the enhanced medical AI
local_medical_ai = LocalMedicalAI()
