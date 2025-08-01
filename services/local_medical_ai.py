import random

class LocalMedicalAI:
    """Simplified medical AI for testing - will be replaced with actual model later"""
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.model_name = model_name
        print(f"Initialized Medical AI (Mock Version) - Model: {model_name}")

    def generate_response(self, prompt: str) -> str:
        # Mock responses for testing
        responses = [
            f"Thank you for your question about '{prompt[:50]}...'. Based on your symptoms, I recommend consulting with a healthcare professional for proper evaluation. This is not a substitute for medical advice.",
            f"I understand you're concerned about '{prompt[:30]}...'. While I can provide general health information, please remember that this should not replace professional medical consultation.",
            f"Regarding your question about '{prompt[:40]}...', it's important to get a proper medical evaluation. I can provide general guidance, but always consult with a healthcare provider."
        ]
        return random.choice(responses)

# Instantiate the local model (could be used as a singleton)
local_medical_ai = LocalMedicalAI()
