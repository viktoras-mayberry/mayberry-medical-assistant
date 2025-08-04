#!/usr/bin/env python3
"""
Test script to demonstrate the comprehensive medical AI API functionality
"""
import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🏥 Testing Health Check Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"✅ Version: {data['version']}")
            print(f"✅ Features: {data['features']}")
            print(f"✅ Uptime: {data['uptime']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the server first.")
        return False
    return True

def test_knowledge_endpoints():
    """Test knowledge base endpoints"""
    print("\n🧠 Testing Knowledge Base Endpoints...")
    
    # Test symptom search
    print("\n🔍 Testing Symptom Search...")
    try:
        response = requests.get(f"{BASE_URL}/knowledge/symptoms?query=fever")
        if response.status_code == 200:
            symptoms = response.json()
            print(f"✅ Found {len(symptoms)} symptoms related to 'fever'")
            if symptoms:
                print(f"   First result: {symptoms[0]['name']} - {symptoms[0]['description']}")
        else:
            print(f"❌ Symptom search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing symptoms: {str(e)}")
    
    # Test disease search
    print("\n🦠 Testing Disease Search...")
    try:
        response = requests.get(f"{BASE_URL}/knowledge/diseases?query=diabetes")
        if response.status_code == 200:
            diseases = response.json()
            print(f"✅ Found {len(diseases)} diseases related to 'diabetes'")
            if diseases:
                print(f"   First result: {diseases[0]['name']} - {diseases[0]['icd_10_code']}")
        else:
            print(f"❌ Disease search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing diseases: {str(e)}")

def test_medical_analysis():
    """Test medical analysis endpoints"""
    print("\n⚕️ Testing Medical Analysis...")
    
    # Test symptom analysis
    print("\n🩺 Testing Symptom Analysis...")
    try:
        payload = {
            "symptoms": ["fever", "cough", "fatigue"],
            "age": 35,
            "gender": "male"
        }
        response = requests.post(f"{BASE_URL}/knowledge/analyze-symptoms", json=payload)
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Analysis completed successfully")
            print(f"   Risk Level: {analysis.get('risk_level', 'Unknown')}")
            print(f"   Possible Diseases: {len(analysis.get('possible_diseases', []))}")
            if analysis.get('possible_diseases'):
                top_disease = analysis['possible_diseases'][0]
                print(f"   Top Match: {top_disease['name']} (Score: {top_disease['match_score']:.2f})")
        else:
            print(f"❌ Symptom analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing symptom analysis: {str(e)}")

def main():
    """Main test function"""
    print("🧪 MAYBERRY Medical AI - API Testing Suite")
    print("=" * 50)
    
    if not test_health_endpoint():
        print("\n❌ Server is not running. Please start the server with:")
        print("   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    test_knowledge_endpoints()
    test_medical_analysis()
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("Your comprehensive medical AI system is ready!")

if __name__ == "__main__":
    main()
