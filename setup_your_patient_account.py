#!/usr/bin/env python3
"""
Script to set up your specific patient account and link analyses
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Analysis, Patient
from werkzeug.security import generate_password_hash

def setup_your_patient_account():
    """Set up your specific patient account with your Gmail"""
    
    # CHANGE THESE TO YOUR DETAILS
    YOUR_EMAIL = "priyanshu@gmail.com"  # Change this to your Gmail
    YOUR_NAME = "Priyanshu Mehra"  # Change this to your name
    YOUR_PASSWORD = "password123"  # Change this to your preferred password
    
    with app.app_context():
        print("🏥 Setting up your patient account...")
        print(f"📧 Email: {YOUR_EMAIL}")
        print(f"👤 Name: {YOUR_NAME}")
        
        # Check if patient already exists
        existing_patient = Patient.query.filter_by(email=YOUR_EMAIL).first()
        if existing_patient:
            print(f"✅ Patient account already exists!")
            patient = existing_patient
        else:
            # Create new patient account
            patient = Patient(
                username=YOUR_EMAIL.split('@')[0],
                email=YOUR_EMAIL,
                full_name=YOUR_NAME,
                password_hash=generate_password_hash(YOUR_PASSWORD),
                phone='+1234567890',
                gender='Not Specified',
                is_active=True,
                email_verified=True
            )
            
            try:
                db.session.add(patient)
                db.session.commit()
                print(f"✅ Created your patient account!")
            except Exception as e:
                print(f"❌ Error creating account: {e}")
                return False
        
        # Link recent analyses to your account
        print(f"\n🔗 Linking recent analyses to your account...")
        
        # Get the most recent analyses (IDs 17 and 18)
        recent_analyses = [17, 18]
        linked_count = 0
        
        for analysis_id in recent_analyses:
            analysis = Analysis.query.get(analysis_id)
            if analysis:
                analysis.patient_id = patient.id
                analysis.patient_email = YOUR_EMAIL
                linked_count += 1
                print(f"   ✅ Linked Analysis ID {analysis_id}: {analysis.diagnosis}")
        
        try:
            db.session.commit()
            print(f"✅ Successfully linked {linked_count} analyses to your account!")
        except Exception as e:
            print(f"❌ Error linking analyses: {e}")
            return False
        
        # Show your medical history
        print(f"\n📊 Your Medical History:")
        analyses = Analysis.query.filter_by(patient_id=patient.id).order_by(Analysis.created_at.desc()).all()
        
        for analysis in analyses:
            print(f"\n   📋 Analysis ID: {analysis.id}")
            print(f"   👤 Patient: {analysis.patient_name}")
            print(f"   🩺 Diagnosis: {analysis.diagnosis}")
            print(f"   📊 Confidence: {analysis.confidence:.2f}%")
            print(f"   📅 Date: {analysis.created_at}")
            if analysis.report_path:
                print(f"   📄 Report: http://localhost:5001{analysis.report_path}")
        
        print(f"\n🔐 Your Login Credentials:")
        print(f"   Email: {YOUR_EMAIL}")
        print(f"   Password: {YOUR_PASSWORD}")
        print(f"   Login URL: http://localhost:3002/patient-login")
        
        print(f"\n✅ Setup complete! You can now:")
        print(f"   1. Go to http://localhost:3002/patient-login")
        print(f"   2. Login with your email and password")
        print(f"   3. View your medical history and reports")
        
        return True

if __name__ == "__main__":
    print("🏥 Skin Cancer Detection System - Your Patient Account Setup")
    print("=" * 70)
    
    success = setup_your_patient_account()
    
    if success:
        print(f"\n🎉 Your patient account is ready!")
    else:
        print(f"\n❌ Setup failed!")
        sys.exit(1)
