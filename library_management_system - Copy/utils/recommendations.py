import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from models.models import Book, BookRating, BorrowRecord, User
import json
from datetime import datetime, timedelta

class RecommendationEngine:
    def __init__(self, db_session):
        self.db_session = db_session
        
    def _get_user_ratings_matrix(self):
        """Create a user-book rating matrix for collaborative filtering"""
        ratings = self.db_session.query(BookRating).all()
        users = self.db_session.query(User).all()
        books = self.db_session.query(Book).all()
        
        # Create rating matrix
        rating_matrix = np.zeros((len(users), len(books)))
        user_idx = {user.id: idx for idx, user in enumerate(users)}
        book_idx = {book.id: idx for idx, book in enumerate(books)}
        
        for rating in ratings:
            if rating.user_id in user_idx and rating.book_id in book_idx:
                rating_matrix[user_idx[rating.user_id]][book_idx[rating.book_id]] = rating.rating
                
        return rating_matrix, users, books, user_idx, book_idx
    
    def _get_content_based_features(self, book):
        """Extract content-based features from book"""
        features = []
        features.extend(book.title.lower().split())
        features.extend(book.author.lower().split())
        features.append(book.category_rel.name.lower())
        if book.description:
            features.extend(book.description.lower().split())
        return list(set(features))
    
    def get_recommendations(self, user_id, n_recommendations=5):
        """Get personalized book recommendations for a user"""
        user = self.db_session.query(User).get(user_id)
        if not user:
            return []
            
        # Get user's reading history and preferences
        reading_history = json.loads(user.reading_history) if user.reading_history else []
        preferred_categories = json.loads(user.preferred_categories) if user.preferred_categories else []
        
        # Get all books
        all_books = self.db_session.query(Book).all()
        
        # Calculate recommendation scores
        recommendations = []
        for book in all_books:
            if book.id in reading_history:
                continue
                
            score = 0.0
            
            # Content-based scoring
            if book.category_rel and book.category_rel.name in preferred_categories:
                score += 2.0
                
            # Popularity-based scoring
            score += book.popularity_score * 0.5
            
            # Rating-based scoring
            if book.average_rating > 0:
                score += book.average_rating * 0.3
                
            recommendations.append((book, score))
            
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [book for book, _ in recommendations[:n_recommendations]]
    
    def update_user_preferences(self, user_id):
        """Update user preferences based on their reading history"""
        user = self.db_session.query(User).get(user_id)
        if not user:
            return
            
        # Get user's recent borrows
        recent_borrows = self.db_session.query(BorrowRecord).filter_by(
            user_id=user_id,
            returned=True
        ).order_by(BorrowRecord.return_date.desc()).limit(10).all()
        
        # Count category frequencies
        category_counts = {}
        for borrow in recent_borrows:
            book = borrow.book
            category_counts[book.category_rel.name] = category_counts.get(book.category_rel.name, 0) + 1
            
        # Get top 3 categories
        preferred_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        preferred_categories = [cat for cat, _ in preferred_categories]
        
        # Update user preferences
        user.preferred_categories = json.dumps(preferred_categories)
        self.db_session.commit()
        
    def update_book_popularity(self):
        """Update popularity scores for all books"""
        books = self.db_session.query(Book).all()
        for book in books:
            # Calculate popularity based on recent borrows and ratings
            recent_borrows = self.db_session.query(BorrowRecord).filter_by(
                book_id=book.id,
                returned=True
            ).filter(
                BorrowRecord.return_date >= datetime.now() - timedelta(days=30)
            ).count()
            
            recent_ratings = self.db_session.query(BookRating).filter_by(
                book_id=book.id
            ).filter(
                BookRating.date_rated >= datetime.now() - timedelta(days=30)
            ).count()
            
            # Update popularity score
            book.popularity_score = (recent_borrows * 0.6 + recent_ratings * 0.4) / 100
            self.db_session.commit() 