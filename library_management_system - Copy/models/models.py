from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.now)
    wallet_balance = db.Column(db.Integer, default=100)  # Starting balance of 100 tokens
    
    # New fields for preferences
    preferred_categories = db.Column(db.String(500), nullable=True)  # Stored as JSON string
    reading_history = db.Column(db.Text, nullable=True)  # Stored as JSON string
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True)
    ratings = db.relationship('BookRating', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    books = db.relationship('Book', backref='category_rel', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(200), nullable=True)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    added_date = db.Column(db.DateTime, default=datetime.now)
    token_cost = db.Column(db.Integer, default=5)  # Default cost is 5 tokens
    
    # New fields for ML features
    average_rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    popularity_score = db.Column(db.Float, default=0.0)
    
    # Relationships
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)
    ratings = db.relationship('BookRating', backref='book', lazy=True)
    
    def __repr__(self):
        return f'<Book {self.title}>'

class BookRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review = db.Column(db.Text, nullable=True)
    date_rated = db.Column(db.DateTime, default=datetime.now)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='unique_user_book_rating'),)
    
    def __repr__(self):
        return f'<BookRating {self.id}>'

class BorrowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    returned = db.Column(db.Boolean, default=False)
    fine = db.Column(db.Integer, default=0)  # Changed to Integer for token-based fines
    fine_paid = db.Column(db.Boolean, default=False)
    tokens_paid = db.Column(db.Integer, default=0)  # Track tokens paid for borrowing
    
    def __repr__(self):
        return f'<BorrowRecord {self.id}>'

class SystemConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<SystemConfig {self.key}>' 