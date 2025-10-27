#!/usr/bin/env python3
"""
Setup test patient with sample data for testing the patient dashboard
"""

from app import app, db, Patient, Analysis
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def setup_test_patient():
    with app.app_context():
        # Create or update test patient
        patient = Patient.query.filter_by(email='ravi@gmail.com').first()
        if not patient:
            patient = Patient(
                username='ravi',
                email='ravi@gmail.com',
                password_hash=generate_password_hash('password123'),
                full_name='Ravi Kumar',
                phone='+91-9876543210',
                gender='Male',
                address='Mumbai, Maharashtra, India'
            )
            db.session.add(patient)
            db.session.commit()
            print("✅ Created test patient")
        else:
            # Update password
            patient.password_hash = generate_password_hash('password123')
            db.session.commit()
            print("✅ Updated test patient password")
        
        # Create some sample analyses for the patient
        sample_analyses = [
            {
                'patient_name': 'Ravi Kumar',
                'patient_email': 'ravi@gmail.com',
                'age': 35,
                'gender': 'Male',
                'location': 'Mumbai, Maharashtra, India',
                'diagnosis': 'Benign Nevus',
                'confidence': 85.5,
                'created_at': datetime.utcnow() - timedelta(days=5)
            },
            {
                'patient_name': 'Ravi Kumar',
                'patient_email': 'ravi@gmail.com',
                'age': 35,
                'gender': 'Male',
                'location': 'Mumbai, Maharashtra, India',
                'diagnosis': 'Actinic Keratoses',
                'confidence': 72.3,
                'created_at': datetime.utcnow() - timedelta(days=2)
            },
            {
                'patient_name': 'Ravi Kumar',
                'patient_email': 'ravi@gmail.com',
                'age': 35,
                'gender': 'Male',
                'location': 'Mumbai, Maharashtra, India',
                'diagnosis': 'Benign Nevus',
                'confidence': 91.2,
                'created_at': datetime.utcnow() - timedelta(hours=6)
            }
        ]
        
        # Clear existing analyses for this patient
        Analysis.query.filter_by(patient_id=patient.id).delete()
        
        # Add sample analyses
        for analysis_data in sample_analyses:
            analysis = Analysis(
                user_id=None,  # No admin/doctor performed this analysis
                patient_id=patient.id,
                patient_name=analysis_data['patient_name'],
                patient_email=analysis_data['patient_email'],
                age=analysis_data['age'],
                gender=analysis_data['gender'],
                location=analysis_data['location'],
                diagnosis=analysis_data['diagnosis'],
                confidence=analysis_data['confidence'],
                image_path='/static/uploads/sample1.jpg',
                viz_path='/static/uploads/viz_sample1.jpg',
                report_path='/static/uploads/report_sample1.pdf',
                all_predictions='{"Benign Nevus": 85.5, "Actinic Keratoses": 10.2, "Melanoma": 4.3}',
                llm_advice='This appears to be a benign lesion. Regular monitoring is recommended.',
                created_at=analysis_data['created_at']
            )
            db.session.add(analysis)
        
        db.session.commit()
        print("✅ Created sample analyses for test patient")
        print(f"✅ Patient ID: {patient.id}")
        print(f"✅ Patient Email: {patient.email}")
        print(f"✅ Patient Password: password123")
        print(f"✅ Number of analyses: {len(sample_analyses)}")

if __name__ == '__main__':
    setup_test_patient()
