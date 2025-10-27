#!/usr/bin/env python3
"""
Check what analyses exist in the database
"""

import sqlite3
import json

def check_analyses():
    """Check all analyses in the database"""
    
    # Connect to the database
    conn = sqlite3.connect('instance/skin_cancer.db')
    cursor = conn.cursor()
    
    try:
        # Get all analyses
        cursor.execute("""
            SELECT id, patient_name, patient_email, user_id, diagnosis, created_at 
            FROM analysis 
            ORDER BY id DESC
        """)
        
        analyses = cursor.fetchall()
        
        print(f"Found {len(analyses)} analyses:")
        print("-" * 80)
        
        for analysis in analyses:
            id_val, name, email, user_id, diagnosis, created_at = analysis
            print(f"ID: {id_val}")
            print(f"  Patient Name: {name}")
            print(f"  Patient Email: {email}")
            print(f"  User ID (Doctor): {user_id}")
            print(f"  Diagnosis: {diagnosis}")
            print(f"  Created: {created_at}")
            print("-" * 40)
        
        # Check if there are any analyses with priyanshu@gmail.com
        cursor.execute("""
            SELECT id, patient_name, patient_email, user_id, diagnosis 
            FROM analysis 
            WHERE patient_email = 'priyanshu@gmail.com'
        """)
        
        priyanshu_analyses = cursor.fetchall()
        
        print(f"\nAnalyses for priyanshu@gmail.com: {len(priyanshu_analyses)}")
        for analysis in priyanshu_analyses:
            id_val, name, email, user_id, diagnosis = analysis
            print(f"  ID: {id_val}, Name: {name}, Doctor ID: {user_id}, Diagnosis: {diagnosis}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_analyses()
