import sys
import os
import re
from typing import Dict, List, Optional

# Add knowledge base to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from knowledge_base.service import knowledge_service
except ImportError:
    knowledge_service = None
    print("Warning: Knowledge base service not available for medical AI")

class LocalMedicalAI:
    """Enhanced medical AI with knowledge base integration"""
    
    def __init__(self, model_name="MAYBERRY-Medical-AI-v1.0"):
        self.model_name = model_name
        self.knowledge_service = knowledge_service
        print(f"Initialized MAYBERRY Medical AI - Model: {model_name}")
        if self.knowledge_service:
            print("✓ Knowledge base integrated successfully")
        else:
            print("⚠ Running in fallback mode without knowledge base")
    
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
    
    def generate_response(self, prompt: str, context: Dict = None) -> Dict[str, any]:
        """Generate comprehensive medical response"""
        # Extract medical entities from prompt
        entities = self.extract_medical_entities(prompt)
        
        # Generate response
        if self.knowledge_service:
            response_text = self.generate_knowledge_based_response(prompt, entities)
            knowledge_used = True
        else:
            response_text = self.generate_fallback_response(prompt)
            knowledge_used = False
        
        # Determine risk level based on content
        risk_level = "low"
        if any(keyword in prompt.lower() for keyword in ['emergency', 'urgent', 'severe', 'critical', 'chest pain', 'difficulty breathing']):
            risk_level = "high"
        elif any(keyword in prompt.lower() for keyword in ['pain', 'fever', 'bleeding', 'infection']):
            risk_level = "medium"
        
        return {
            "response": response_text,
            "risk_level": risk_level,
            "confidence_score": 0.85 if knowledge_used else 0.65,
            "knowledge_base_used": knowledge_used,
            "extracted_entities": entities,
            "recommendations": self._generate_recommendations(risk_level)
        }
    
    def _generate_recommendations(self, risk_level: str) -> List[str]:
        """Generate recommendations based on risk level"""
        if risk_level == "high":
            return [
                "Seek immediate medical attention",
                "Do not delay in contacting emergency services if symptoms worsen",
                "Have someone stay with you if possible"
            ]
        elif risk_level == "medium":
            return [
                "Consider scheduling an appointment with your healthcare provider",
                "Monitor your symptoms closely",
                "Keep a record of when symptoms occur"
            ]
        else:
            return [
                "Maintain good health practices",
                "Stay hydrated and get adequate rest",
                "Contact a healthcare provider if symptoms persist or worsen"
            ]

# Instantiate the enhanced medical AI
local_medical_ai = LocalMedicalAI()
