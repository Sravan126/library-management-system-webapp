"""
Initialize database with sample data for the Library Management System
"""

from app import app, db
from models.models import User, SystemConfig
from werkzeug.security import generate_password_hash
from datetime import datetime
import json

def init_db():
    """Create sample data for the library database"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@library.com').first()
        if not admin:
            # Create admin user
            admin = User(
                email='admin@library.com',
                password=generate_password_hash('admin123'),
                name='Administrator',
                is_admin=True,
                date_joined=datetime.now(),
                reading_history=json.dumps([]),
                preferred_categories=json.dumps([])
            )
            db.session.add(admin)
            print("Admin user created")
        
        # Set default late fee rate if not exists
        late_fee_config = SystemConfig.query.filter_by(key='late_fee_rate').first()
        if not late_fee_config:
            late_fee_config = SystemConfig(
                key='late_fee_rate',
                value='5.0',
                description='Late fee rate in Indian Rupees per day'
            )
            db.session.add(late_fee_config)
            print("Default late fee rate set")
        
        # Commit all changes
        db.session.commit()
        print("Database initialization completed")

if __name__ == '__main__':
    init_db() 