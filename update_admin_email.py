#!/usr/bin/env python3
"""
Script to update admin email to priyanshu@gmail.com
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def update_admin_email():
    """Update or create admin user with new email"""
    with app.app_context():
        # Check if admin user exists
        admin_user = User.query.filter_by(role='admin').first()
        
        if admin_user:
            # Update existing admin user
            print(f"Found existing admin user: {admin_user.email}")
            admin_user.email = 'priyanshu@gmail.com'
            admin_user.name = 'Priyanshu'
            print("Updated admin email to: priyanshu@gmail.com")
        else:
            # Create new admin user
            print("No admin user found, creating new one...")
            admin_user = User(
                name='Priyanshu',
                email='priyanshu@gmail.com',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("Created new admin user: priyanshu@gmail.com")
        
        # Commit changes
        db.session.commit()
        print("✅ Admin email updated successfully!")
        
        # Verify the change
        updated_admin = User.query.filter_by(email='priyanshu@gmail.com').first()
        if updated_admin:
            print(f"✅ Verification: Admin user found with email {updated_admin.email}")
            print(f"   Name: {updated_admin.name}")
            print(f"   Role: {updated_admin.role}")
        else:
            print("❌ Error: Could not verify admin user creation")

if __name__ == '__main__':
    update_admin_email()
