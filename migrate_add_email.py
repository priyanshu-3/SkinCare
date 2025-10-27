#!/usr/bin/env python3
"""
Database migration script to add patient_email column to Analysis table
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Analysis

def migrate_add_email():
    """Add patient_email column to Analysis table"""
    print("🔄 Adding patient_email column to Analysis table...")
    
    with app.app_context():
        try:
            # Check if patient_email column already exists
            from sqlalchemy import text
            try:
                db.session.execute(text("SELECT patient_email FROM analysis LIMIT 1"))
                print("✅ patient_email column already exists")
                return True
            except Exception as e:
                if "no such column: patient_email" in str(e):
                    print("🔧 Adding patient_email column to Analysis table...")
                    # Add the patient_email column
                    db.session.execute(text("ALTER TABLE analysis ADD COLUMN patient_email VARCHAR(255)"))
                    db.session.commit()
                    print("✅ Added patient_email column to Analysis table")
                else:
                    raise e
            
            # Check table structure
            result = db.session.execute(text("PRAGMA table_info(analysis)"))
            columns = result.fetchall()
            email_column = any(col[1] == 'patient_email' for col in columns)
            
            if email_column:
                print("✅ patient_email column confirmed in Analysis table")
            else:
                print("❌ patient_email column not found")
                return False
                
            print("✅ Migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🚀 Skin Cancer Detection System - Add Email Column Migration")
    print("=" * 60)
    
    success = migrate_add_email()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("The patient_email column has been added to the Analysis table.")
    else:
        print("\n💥 Migration failed. Please check the error messages above.")
        sys.exit(1)
