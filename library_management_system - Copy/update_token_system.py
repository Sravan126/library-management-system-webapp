from app import app, db
from models.models import User, Book
import random

def update_token_system():
    with app.app_context():
        # Update all users with a starting balance of 100 tokens
        users = User.query.all()
        for user in users:
            user.wallet_balance = 100
        print(f"Updated {len(users)} users with starting balance of 100 tokens")

        # Update all books with token costs between 5 and 10
        books = Book.query.all()
        for book in books:
            # Assign token cost based on popularity or randomly
            if book.popularity_score > 0.7:
                book.token_cost = 10
            elif book.popularity_score > 0.4:
                book.token_cost = 7
            else:
                book.token_cost = 5
        print(f"Updated {len(books)} books with token costs")

        db.session.commit()
        print("Token system update completed successfully!")

if __name__ == '__main__':
    update_token_system() 