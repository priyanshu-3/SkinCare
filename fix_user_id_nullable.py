#!/usr/bin/env python3
"""
Fix user_id column to be nullable in analysis table
"""

from app import app, db
from sqlalchemy import text

def fix_user_id_nullable():
    with app.app_context():
        try:
            print("🔧 Making user_id column nullable in analysis table...")
            
            # SQLite doesn't support ALTER COLUMN directly, so we need to recreate the table
            # First, let's create a backup of existing data
            print("📋 Backing up existing data...")
            result = db.session.execute(text("SELECT * FROM analysis"))
            existing_data = result.fetchall()
            print(f"✅ Found {len(existing_data)} existing records")
            
            # Create new table with correct schema
            print("🔨 Creating new analysis table with nullable user_id...")
            db.session.execute(text("""
                CREATE TABLE analysis_new (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    patient_id INTEGER,
                    patient_name VARCHAR(120) NOT NULL,
                    patient_email VARCHAR(255),
                    age INTEGER NOT NULL,
                    gender VARCHAR(20) NOT NULL,
                    location VARCHAR(255),
                    diagnosis VARCHAR(255) NOT NULL,
                    confidence FLOAT NOT NULL,
                    image_path VARCHAR(500),
                    viz_path VARCHAR(500),
                    report_path VARCHAR(500),
                    all_predictions TEXT,
                    llm_advice TEXT,
                    created_at DATETIME
                )
            """))
            
            # Copy data from old table to new table
            print("📋 Copying data to new table...")
            for row in existing_data:
                # Convert row tuple to dictionary for easier handling
                row_dict = {
                    'id': row[0],
                    'user_id': row[1],
                    'patient_id': row[14] if len(row) > 14 else None,  # patient_id is at index 14
                    'patient_name': row[2],
                    'patient_email': row[15] if len(row) > 15 else None,  # patient_email is at index 15
                    'age': row[3],
                    'gender': row[4],
                    'location': row[5],
                    'diagnosis': row[6],
                    'confidence': row[7],
                    'image_path': row[8],
                    'viz_path': row[9],
                    'report_path': row[10],
                    'all_predictions': row[11],
                    'llm_advice': row[12],
                    'created_at': row[13]
                }
                
                db.session.execute(text("""
                    INSERT INTO analysis_new 
                    (id, user_id, patient_id, patient_name, patient_email, age, gender, location, 
                     diagnosis, confidence, image_path, viz_path, report_path, all_predictions, 
                     llm_advice, created_at)
                    VALUES (:id, :user_id, :patient_id, :patient_name, :patient_email, :age, :gender, :location, 
                            :diagnosis, :confidence, :image_path, :viz_path, :report_path, :all_predictions, 
                            :llm_advice, :created_at)
                """), row_dict)
            
            # Drop old table and rename new table
            print("🔄 Replacing old table...")
            db.session.execute(text("DROP TABLE analysis"))
            db.session.execute(text("ALTER TABLE analysis_new RENAME TO analysis"))
            
            db.session.commit()
            print("✅ Successfully made user_id nullable!")
            
            # Verify the change
            result = db.session.execute(text("PRAGMA table_info(analysis)"))
            columns = result.fetchall()
            for col in columns:
                if col[1] == 'user_id':
                    print(f"✅ user_id is now nullable: {not col[3]}")
                    break
                    
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            raise

if __name__ == '__main__':
    fix_user_id_nullable()
