#!/usr/bin/env python3
"""
Test script to verify that analysis detail endpoint works for doctor-created analyses
when accessed by patients - using correct analysis IDs.
"""

import requests
import json

def test_analysis_detail_fix():
    """Test the analysis detail endpoint with patient_email parameter"""
    
    base_url = "http://localhost:5001"
    
    # Test with analysis ID 17 (belongs to priyanshu@gmail.com)
    print("=== Test 1: Analysis ID 17 (priyanshu@gmail.com) without patient_email parameter ===")
    try:
        response = requests.get(f"{base_url}/api/history/17")
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
    
    # Test with analysis ID 17 with patient_email parameter
    print("=== Test 2: Analysis ID 17 with patient_email parameter ===")
    try:
        test_email = "priyanshu@gmail.com"
        response = requests.get(f"{base_url}/api/history/17?patient_email={test_email}")
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
    
    # Test with analysis ID 13 (belongs to ravi@gmail.com) with wrong email
    print("=== Test 3: Analysis ID 13 (ravi@gmail.com) with wrong patient_email ===")
    try:
        wrong_email = "priyanshu@gmail.com"
        response = requests.get(f"{base_url}/api/history/13?patient_email={wrong_email}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Test with analysis ID 13 with correct email
    print("=== Test 4: Analysis ID 13 (ravi@gmail.com) with correct patient_email ===")
    try:
        correct_email = "ravi@gmail.com"
        response = requests.get(f"{base_url}/api/history/13?patient_email={correct_email}")
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

if __name__ == "__main__":
    test_analysis_detail_fix()
