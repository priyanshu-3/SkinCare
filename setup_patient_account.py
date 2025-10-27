#!/usr/bin/env python3
"""
Script to create a patient account and link recent analysis to it
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Analysis, Patient
from werkzeug.security import generate_password_hash

def create_patient_account(email, full_name, username=None):
    """Create a new patient account"""
    
    with app.app_context():
        # Check if patient already exists
        existing_patient = Patient.query.filter_by(email=email).first()
        if existing_patient:
            print(f"✅ Patient account already exists for {email}")
            return existing_patient
        
        # Create new patient account
        if not username:
            username = email.split('@')[0]  # Use email prefix as username
        
        patient = Patient(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=generate_password_hash('password123'),  # Default password
            phone='+1234567890',
            gender='Not Specified',
            is_active=True,
            email_verified=True
        )
        
        try:
            db.session.add(patient)
            db.session.commit()
            print(f"✅ Created patient account for {email}")
            return patient
        except Exception as e:
            print(f"❌ Error creating patient account: {e}")
            db.session.rollback()
            return None

def link_analysis_to_patient(analysis_id, patient_email):
    """Link a specific analysis to a patient account"""
    
    with app.app_context():
        # Find the analysis
        analysis = Analysis.query.get(analysis_id)
        if not analysis:
            print(f"❌ Analysis ID {analysis_id} not found")
            return False
        
        # Find the patient
        patient = Patient.query.filter_by(email=patient_email).first()
        if not patient:
            print(f"❌ Patient with email {patient_email} not found")
            return False
        
        # Update the analysis
        analysis.patient_id = patient.id
        analysis.patient_email = patient_email
        
        try:
            db.session.commit()
            print(f"✅ Linked analysis ID {analysis_id} to patient {patient_email}")
            return True
        except Exception as e:
            print(f"❌ Error linking analysis: {e}")
            db.session.rollback()
            return False

def show_patient_dashboard_info(patient_email):
    """Show information that will appear in patient dashboard"""
    
    with app.app_context():
        patient = Patient.query.filter_by(email=patient_email).first()
        if not patient:
            print(f"❌ Patient with email {patient_email} not found")
            return
        
        print(f"\n👤 Patient Account Information:")
        print(f"   Name: {patient.full_name}")
        print(f"   Email: {patient.email}")
        print(f"   Username: {patient.username}")
        print(f"   Patient ID: {patient.id}")
        
        # Get analyses for this patient
        analyses = Analysis.query.filter_by(patient_id=patient.id).order_by(Analysis.created_at.desc()).all()
        
        print(f"\n📊 Medical History ({len(analyses)} records):")
        for analysis in analyses:
            print(f"   📋 Analysis ID: {analysis.id}")
            print(f"   👤 Patient: {analysis.patient_name}")
            print(f"   🩺 Diagnosis: {analysis.diagnosis}")
            print(f"   📊 Confidence: {analysis.confidence:.2f}%")
            print(f"   📅 Date: {analysis.created_at}")
            if analysis.report_path:
                print(f"   📄 Report: http://localhost:5001{analysis.report_path}")
            print("   " + "-" * 60)
        
        print(f"\n🔐 Login Credentials:")
        print(f"   Email: {patient.email}")
        print(f"   Password: password123")
        print(f"   Login URL: http://localhost:3002/patient-login")

if __name__ == "__main__":
    print("🏥 Skin Cancer Detection System - Patient Account Setup")
    print("=" * 60)
    
    # You can change this email to your specific Gmail address
    patient_email = "your.email@gmail.com"  # Change this to your Gmail
    patient_name = "Your Name"  # Change this to your name
    
    print(f"📧 Setting up patient account for: {patient_email}")
    
    # Create patient account
    patient = create_patient_account(patient_email, patient_name)
    
    if patient:
        # Link the most recent analysis (ID 18) to this patient
        print(f"\n🔗 Linking recent analysis to patient account...")
        success = link_analysis_to_patient(18, patient_email)
        
        if success:
            print(f"\n✅ Setup complete!")
            show_patient_dashboard_info(patient_email)
        else:
            print(f"❌ Failed to link analysis")
    else:
        print(f"❌ Failed to create patient account")
