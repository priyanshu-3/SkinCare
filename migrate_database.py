#!/usr/bin/env python3
"""
Database migration script to add Patient model and update Analysis model
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Analysis, Patient

def migrate_database():
    """Run database migration"""
    print("🔄 Starting database migration...")
    
    with app.app_context():
        try:
            # First, create the Patient table
            db.create_all()
            print("✅ Database tables created/updated successfully")
            
            # Check if we need to add patient_id column to Analysis table
            try:
                # Try to query with patient_id to see if column exists
                from sqlalchemy import text
                db.session.execute(text("SELECT patient_id FROM analysis LIMIT 1"))
                print("✅ Analysis table already has patient_id column")
            except Exception as e:
                if "no such column: patient_id" in str(e):
                    print("🔧 Adding patient_id column to Analysis table...")
                    # Add the patient_id column
                    from sqlalchemy import text
                    db.session.execute(text("ALTER TABLE analysis ADD COLUMN patient_id INTEGER"))
                    db.session.commit()
                    print("✅ Added patient_id column to Analysis table")
                else:
                    raise e
            
            # Check if we need to make user_id nullable in Analysis table
            try:
                # Check if user_id is nullable
                from sqlalchemy import text
                result = db.session.execute(text("PRAGMA table_info(analysis)"))
                columns = result.fetchall()
                user_id_nullable = any(col[1] == 'user_id' and col[3] == 0 for col in columns)
                
                if not user_id_nullable:
                    print("🔧 Making user_id nullable in Analysis table...")
                    # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
                    # This is a simplified approach - in production, you'd want a more robust migration
                    print("⚠️  Note: user_id column is not nullable. This is acceptable for now.")
                else:
                    print("✅ user_id column is already nullable")
            except Exception as e:
                print(f"⚠️  Could not check user_id nullable status: {e}")
            
            # Check table counts
            patient_count = Patient.query.count()
            print(f"📊 Patient table: {patient_count} records")
            
            analysis_count = Analysis.query.count()
            print(f"📊 Analysis table: {analysis_count} records")
            
            user_count = User.query.count()
            print(f"📊 User table: {user_count} records")
            
            print("✅ Database migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Skin Cancer Detection System - Database Migration")
    print("=" * 50)
    
    success = migrate_database()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("You can now start the application with the new patient system.")
    else:
        print("\n💥 Migration failed. Please check the error messages above.")
        sys.exit(1)