#!/usr/bin/env python3
"""
Test patient authentication and API endpoints
"""

import requests
import json

def test_patient_auth():
    base_url = "http://localhost:5001"
    session = requests.Session()
    
    print("🔐 Testing Patient Authentication Flow")
    print("=" * 50)
    
    # Step 1: Patient Login
    print("1. Testing patient login...")
    login_data = {
        "username_or_email": "ravi@gmail.com",
        "password": "password123"
    }
    
    login_response = session.post(
        f"{base_url}/api/patient/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"   Status: {login_response.status_code}")
    if login_response.status_code == 200:
        print("   ✅ Login successful")
        patient_data = login_response.json()
        print(f"   Patient: {patient_data['patient']['full_name']} ({patient_data['patient']['email']})")
    else:
        print(f"   ❌ Login failed: {login_response.text}")
        return
    
    # Step 2: Test patient profile endpoint
    print("\n2. Testing patient profile endpoint...")
    profile_response = session.get(f"{base_url}/api/patient/profile")
    print(f"   Status: {profile_response.status_code}")
    if profile_response.status_code == 200:
        print("   ✅ Profile access successful")
    else:
        print(f"   ❌ Profile access failed: {profile_response.text[:200]}")
    
    # Step 3: Test history endpoint
    print("\n3. Testing history endpoint...")
    history_response = session.get(f"{base_url}/api/history")
    print(f"   Status: {history_response.status_code}")
    if history_response.status_code == 200:
        print("   ✅ History access successful")
        history_data = history_response.json()
        print(f"   Found {len(history_data.get('history', []))} analyses")
    else:
        print(f"   ❌ History access failed: {history_response.text[:200]}")
    
    # Step 4: Test stats endpoint
    print("\n4. Testing stats endpoint...")
    stats_response = session.get(f"{base_url}/api/history/stats")
    print(f"   Status: {stats_response.status_code}")
    if stats_response.status_code == 200:
        print("   ✅ Stats access successful")
        stats_data = stats_response.json()
        print(f"   Stats: {stats_data.get('stats', {})}")
    else:
        print(f"   ❌ Stats access failed: {stats_response.text[:200]}")
    
    print("\n" + "=" * 50)
    print("🎯 Authentication test completed!")

if __name__ == '__main__':
    test_patient_auth()
