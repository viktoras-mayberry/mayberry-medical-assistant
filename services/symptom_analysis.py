import random

def analyze_symptoms_model(symptoms, duration=None, severity=None, age=None, gender=None, additional_info=None):
    # Simulate AI analysis with random mock results
    possible_conditions = [
        {"name": "Common Cold", "probability": random.uniform(0.0, 0.2)},
        {"name": "Flu", "probability": random.uniform(0.0, 0.15)},
        {"name": "Allergies", "probability": random.uniform(0.0, 0.1)},
        {"name": "COVID-19", "probability": random.uniform(0.0, 0.05)}
    ]
    
    # Randomly calculate total risk level
    possible_conditions = sorted(possible_conditions, key=lambda x: x["probability"], reverse=True)
    risk_level = "low"
    if sum([c["probability"] for c in possible_conditions]) > 0.1:
        risk_level = "medium"
    if sum([c["probability"] for c in possible_conditions]) > 0.3:
        risk_level = "high"

    # Create output dictionary
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
        "disclaimer": "This analysis is for informational purposes only and does not constitute medical advice."
    }

    return analysis
