from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from models.models import db, User, Book, BorrowRecord, BookRating, SystemConfig, Category
from utils.recommendations import RecommendationEngine
from utils.fee_calculator import FeeCalculator
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import json

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Security configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize security headers
Talisman(app, 
    content_security_policy={
        'default-src': "'self'",
        'img-src': "'self' data: https:",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net",
        'style-src': "'self' 'unsafe-inline' https: https://cdnjs.cloudflare.com",
        'font-src': "'self' https: data: https://cdnjs.cloudflare.com",
    }
)

# Initialize recommendation engine and fee calculator
recommendation_engine = RecommendationEngine(db.session)
fee_calculator = FeeCalculator(db.session)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Add current datetime to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Routes
@app.route('/')
def home():
    books = Book.query.order_by(Book.title).limit(6).all()
    if current_user.is_authenticated:
        recommendations = recommendation_engine.get_recommendations(current_user.id)
    else:
        recommendations = []
    return render_template('index.html', books=books, recommendations=recommendations)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            user.last_login = datetime.now()
            db.session.commit()
            
            next_page = request.args.get('next')
            flash('Successfully logged in!', 'success')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        is_admin = False
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login instead.', 'warning')
            return redirect(url_for('login'))
        
        new_user = User(
            email=email,
            password=generate_password_hash(password),
            name=name,
            is_admin=is_admin,
            reading_history=json.dumps([]),
            preferred_categories=json.dumps([])
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    borrowed_books = BorrowRecord.query.filter_by(user_id=current_user.id, returned=False).all()
    history = BorrowRecord.query.filter_by(user_id=current_user.id, returned=True).order_by(BorrowRecord.return_date.desc()).limit(5).all()
    
    # Calculate fines for borrowed books
    for record in borrowed_books:
        record.fine = fee_calculator.calculate_late_fee(record)
    
    # Get fee summary
    fee_summary = fee_calculator.get_fee_summary(current_user.id)
    
    # Get recommendations
    recommendations = recommendation_engine.get_recommendations(current_user.id)
    
    return render_template('dashboard.html', 
                         borrowed_books=borrowed_books, 
                         history=history,
                         fee_summary=fee_summary,
                         recommendations=recommendations)

@app.route('/catalog')
def catalog():
    search_query = request.args.get('search', '')
    category_id = request.args.get('category', '')
    
    query = Book.query
    
    if search_query:
        query = query.filter(Book.title.contains(search_query) | Book.author.contains(search_query))
    
    if category_id:
        query = query.filter_by(category_id=category_id)
        
    books = query.order_by(Book.title).all()
    categories = Category.query.all()
    
    return render_template('catalog.html', books=books, categories=categories, search=search_query, selected_category=category_id)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    user_rating = None
    if current_user.is_authenticated:
        user_rating = BookRating.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    return render_template('book_details.html', book=book, user_rating=user_rating)

@app.route('/rate_book/<int:book_id>', methods=['POST'])
@login_required
def rate_book(book_id):
    rating = int(request.form.get('rating', 0))
    review = request.form.get('review', '')
    
    if not 1 <= rating <= 5:
        flash('Invalid rating value.', 'danger')
        return redirect(url_for('book_details', book_id=book_id))
    
    existing_rating = BookRating.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if existing_rating:
        existing_rating.rating = rating
        existing_rating.review = review
    else:
        new_rating = BookRating(
            user_id=current_user.id,
            book_id=book_id,
            rating=rating,
            review=review
        )
        db.session.add(new_rating)
    
    # Update book's average rating
    book = Book.query.get(book_id)
    ratings = BookRating.query.filter_by(book_id=book_id).all()
    book.average_rating = sum(r.rating for r in ratings) / len(ratings)
    book.rating_count = len(ratings)
    
    db.session.commit()
    flash('Rating submitted successfully!', 'success')
    return redirect(url_for('book_details', book_id=book_id))

@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if book.available_copies <= 0:
        flash('This book is currently unavailable.', 'danger')
        return redirect(url_for('catalog'))
    
    existing_borrow = BorrowRecord.query.filter_by(user_id=current_user.id, book_id=book_id, returned=False).first()
    if existing_borrow:
        flash('You already have this book borrowed.', 'warning')
        return redirect(url_for('dashboard'))
    
    # Check if user has enough tokens
    if current_user.wallet_balance < book.token_cost:
        flash(f'Insufficient tokens. This book requires {book.token_cost} tokens to borrow.', 'danger')
        return redirect(url_for('catalog'))
    
    due_date = datetime.now() + timedelta(days=14)
    new_borrow = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        borrow_date=datetime.now(),
        due_date=due_date,
        returned=False,
        tokens_paid=book.token_cost
    )
    
    # Deduct tokens from user's wallet
    current_user.wallet_balance -= book.token_cost
    book.available_copies -= 1
    
    # Update user's reading history
    reading_history = json.loads(current_user.reading_history or '[]')
    reading_history.append(book_id)
    current_user.reading_history = json.dumps(reading_history)
    
    db.session.add(new_borrow)
    db.session.commit()
    
    # Update user preferences
    recommendation_engine.update_user_preferences(current_user.id)
    
    flash(f'You have borrowed "{book.title}" for {book.token_cost} tokens. Please return by {due_date.strftime("%B %d, %Y")}.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    borrow_record = BorrowRecord.query.get_or_404(borrow_id)
    
    if borrow_record.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Calculate late fee (1 token per day)
    days_overdue = (datetime.now() - borrow_record.due_date).days
    late_fee = max(0, days_overdue)  # 1 token per day if overdue
    
    borrow_record.returned = True
    borrow_record.return_date = datetime.now()
    borrow_record.fine = late_fee
    
    book = Book.query.get(borrow_record.book_id)
    book.available_copies += 1
    
    # Deduct late fee from user's wallet if there are overdue days
    if late_fee > 0:
        if current_user.wallet_balance >= late_fee:
            current_user.wallet_balance -= late_fee
            borrow_record.fine_paid = True
            flash(f'Book returned with a late fee of {late_fee} tokens, which has been deducted from your wallet.', 'warning')
        else:
            flash(f'Book returned. You have a late fee of {late_fee} tokens, but insufficient balance to pay it.', 'danger')
    else:
        flash('Book returned successfully. Thank you!', 'success')
    
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/pay_fee/<int:borrow_id>', methods=['POST'])
@login_required
def pay_fee(borrow_id):
    if fee_calculator.mark_fee_as_paid(borrow_id):
        flash('Fee payment recorded successfully.', 'success')
    else:
        flash('Error processing payment.', 'danger')
    return redirect(url_for('dashboard'))

# Admin routes
@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    
    books = Book.query.all()
    users = User.query.all()
    recent_borrows = BorrowRecord.query.order_by(BorrowRecord.borrow_date.desc()).limit(10).all()
    
    return render_template('admin/panel.html', books=books, users=users, recent_borrows=recent_borrows)

@app.route('/admin/update_fee_rate', methods=['POST'])
@login_required
def update_fee_rate():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        new_rate = float(request.form.get('rate'))
        if new_rate < 0:
            raise ValueError("Rate cannot be negative")
        fee_calculator.update_late_fee_rate(new_rate)
        flash('Late fee rate updated successfully.', 'success')
    except ValueError as e:
        flash(f'Invalid rate value: {str(e)}', 'danger')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/process_overdue')
@login_required
def process_overdue():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    
    fee_calculator.process_overdue_books()
    flash('Overdue books processed successfully.', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/update_popularity')
@login_required
def update_popularity():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    
    recommendation_engine.update_book_popularity()
    flash('Book popularity scores updated successfully.', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        total_copies = int(request.form.get('total_copies'))
        cover_image = request.form.get('cover_image')
        token_cost = int(request.form.get('token_cost'))
        new_book = Book(
            title=title,
            author=author,
            isbn=isbn,
            category_id=category_id,
            description=description,
            total_copies=total_copies,
            available_copies=total_copies,
            cover_image=cover_image,
            token_cost=token_cost
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{title}" added successfully!', 'success')
        return redirect(url_for('admin_panel'))
    return render_template('admin/add_book.html', categories=categories)

@app.route('/admin/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    book = Book.query.get_or_404(book_id)
    categories = Category.query.all()
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.isbn = request.form.get('isbn')
        book.category_id = request.form.get('category_id')
        book.description = request.form.get('description')
        book.cover_image = request.form.get('cover_image')
        book.token_cost = int(request.form.get('token_cost'))
        new_total = int(request.form.get('total_copies'))
        # Adjust available copies if total changes
        difference = new_total - book.total_copies
        book.total_copies = new_total
        book.available_copies += difference
        db.session.commit()
        flash(f'Book "{book.title}" updated successfully!', 'success')
        return redirect(url_for('admin_panel'))
    return render_template('admin/edit_book.html', book=book, categories=categories)

@app.route('/admin/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    
    book = Book.query.get_or_404(book_id)
    
    # Check if book is currently borrowed
    active_borrows = BorrowRecord.query.filter_by(book_id=book_id, returned=False).first()
    if active_borrows:
        flash(f'Cannot delete "{book.title}" as it is currently borrowed by users.', 'danger')
        return redirect(url_for('admin_panel'))
    
    db.session.delete(book)
    db.session.commit()
    
    flash(f'Book "{book.title}" deleted successfully!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/manage_users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@app.route('/admin/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        flash('You do not have admin privileges.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Prevent self-demotion
    if user_id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('manage_users'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    action = "granted" if user.is_admin else "revoked"
    flash(f'Admin privileges {action} for {user.name}.', 'success')
    return redirect(url_for('manage_users'))

@app.context_processor
def utility_processor():
    def days_overdue(due_date):
        if due_date < datetime.now():
            return (datetime.now() - due_date).days
        return 0
    
    return dict(days_overdue=days_overdue)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 