#!/usr/bin/env python3
"""
Test script to verify that analysis detail endpoint works for doctor-created analyses
when accessed by patients.
"""

import requests
import json

def test_analysis_detail_fix():
    """Test the analysis detail endpoint with patient_email parameter"""
    
    base_url = "http://localhost:5001"
    
    # Test 1: Get analysis detail without patient_email parameter
    print("=== Test 1: Analysis detail without patient_email parameter ===")
    try:
        response = requests.get(f"{base_url}/api/history/13")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            if data.get('analysis'):
                analysis = data['analysis']
                print(f"Analysis ID: {analysis.get('id')}")
                print(f"Patient Name: {analysis.get('patient_name')}")
                print(f"Patient Email: {analysis.get('patient_email')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Test 2: Get analysis detail with patient_email parameter
    print("=== Test 2: Analysis detail with patient_email parameter ===")
    try:
        # Use a test patient email
        test_email = "priyanshu@gmail.com"
        response = requests.get(f"{base_url}/api/history/13?patient_email={test_email}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            if data.get('analysis'):
                analysis = data['analysis']
                print(f"Analysis ID: {analysis.get('id')}")
                print(f"Patient Name: {analysis.get('patient_name')}")
                print(f"Patient Email: {analysis.get('patient_email')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Test 3: List all analyses to see what's available
    print("=== Test 3: List all analyses ===")
    try:
        response = requests.get(f"{base_url}/api/history")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total analyses: {data.get('count', 0)}")
            if data.get('history'):
                for i, analysis in enumerate(data['history'][:3]):  # Show first 3
                    print(f"  {i+1}. ID: {analysis.get('id')}, Patient: {analysis.get('patient_name')}, Email: {analysis.get('patient_email')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_analysis_detail_fix()
