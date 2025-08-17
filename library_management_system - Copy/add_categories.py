from app import app, db
from models.models import Category

def add_categories():
    with app.app_context():
        categories = [
            {'name': 'Fiction', 'description': 'Literary works created from imagination'},
            {'name': 'Science Fiction', 'description': 'Fiction dealing with futuristic concepts and technology'},
            {'name': 'Fantasy', 'description': 'Fiction featuring magical and supernatural elements'},
            {'name': 'Science', 'description': 'Books about scientific discoveries and concepts'},
            {'name': 'Technology', 'description': 'Books about technological advancements and computing'},
            {'name': 'Romance', 'description': 'Stories focusing on romantic relationships'},
            {'name': 'Non-Fiction', 'description': 'Factual works based on real events and topics'}
        ]
        
        for category_data in categories:
            category = Category(**category_data)
            db.session.add(category)
        
        db.session.commit()
        print("Categories added successfully!")

if __name__ == '__main__':
    add_categories() 