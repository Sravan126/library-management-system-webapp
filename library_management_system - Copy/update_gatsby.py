from app import app, db
from models.models import Book

def update_gatsby_cover():
    with app.app_context():
        book = Book.query.filter_by(title='The Great Gatsby').first()
        if book:
            book.cover_image = 'https://covers.openlibrary.org/b/id/12001847-L.jpg'
            db.session.commit()
            print('Updated The Great Gatsby cover image successfully!')
        else:
            print('Book not found!')

if __name__ == '__main__':
    update_gatsby_cover() 