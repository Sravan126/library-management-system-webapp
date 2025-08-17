from app import app, db
from models.models import Book, Category

def add_sample_books():
    with app.app_context():
        # Create categories
        categories = {
            'Fiction': Category(name='Fiction', description='Fictional literature'),
            'Non-Fiction': Category(name='Non-Fiction', description='Non-fictional literature'),
            'Science': Category(name='Science', description='Scientific books'),
            'History': Category(name='History', description='Historical books'),
            'Technology': Category(name='Technology', description='Technology and computing books'),
            'Fantasy': Category(name='Fantasy', description='Fantasy books'),
            'Romance': Category(name='Romance', description='Romantic novels'),
            'Science Fiction': Category(name='Science Fiction', description='Science fiction novels')
        }
        
        for category in categories.values():
            db.session.add(category)
        db.session.commit()

        # Sample books with cover images
        sample_books = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'category': categories['Fiction'],
                'total_copies': 5,
                'available_copies': 5,
                'description': 'A story of the fabulously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.',
                'cover_image': 'https://covers.openlibrary.org/b/id/12001847-L.jpg'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780446310789',
                'category': categories['Fiction'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'The story of racial injustice and the loss of innocence in the American South.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8228691-L.jpg'
            },
            {
                'title': 'A Brief History of Time',
                'author': 'Stephen Hawking',
                'isbn': '9780553380163',
                'category': categories['Science'],
                'total_copies': 4,
                'available_copies': 4,
                'description': 'An exploration of modern physics and the universe.',
                'cover_image': 'https://covers.openlibrary.org/b/id/240726-L.jpg'
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'isbn': '9780132350884',
                'category': categories['Technology'],
                'total_copies': 6,
                'available_copies': 6,
                'description': 'A handbook of agile software craftsmanship.',
                'cover_image': 'https://covers.openlibrary.org/b/id/9641987-L.jpg'
            },
            {
                'title': 'Sapiens',
                'author': 'Yuval Noah Harari',
                'isbn': '9780062316097',
                'category': categories['History'],
                'total_copies': 4,
                'available_copies': 4,
                'description': 'A brief history of humankind.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8370226-L.jpg'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'category': categories['Science Fiction'],
                'total_copies': 5,
                'available_copies': 5,
                'description': 'A dystopian social science fiction novel and cautionary tale.',
                'cover_image': 'https://covers.openlibrary.org/b/id/7222246-L.jpg'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'category': categories['Romance'],
                'total_copies': 4,
                'available_copies': 4,
                'description': 'A romantic novel of manners that satirizes 19th century society.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8231856-L.jpg'
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780547928227',
                'category': categories['Fantasy'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A fantasy novel about the adventures of Bilbo Baggins.',
                'cover_image': 'https://covers.openlibrary.org/b/id/6979861-L.jpg'
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'isbn': '9780316769488',
                'category': categories['Fiction'],
                'total_copies': 4,
                'available_copies': 4,
                'description': 'A story about adolescent alienation and loss of innocence.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8231996-L.jpg'
            },
            {
                'title': 'Brave New World',
                'author': 'Aldous Huxley',
                'isbn': '9780060850524',
                'category': categories['Science Fiction'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A dystopian novel set in a futuristic World State.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8775116-L.jpg'
            },
            {
                'title': 'Dune',
                'author': 'Frank Herbert',
                'isbn': '9780441172719',
                'category': categories['Science Fiction'],
                'total_copies': 4,
                'available_copies': 4,
                'description': 'A mythic and emotionally charged hero's journey set in a distant desert planet.',
                'cover_image': 'https://covers.openlibrary.org/b/id/12645114-L.jpg'
            },
            {
                'title': 'The Lord of the Rings',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780618640157',
                'category': categories['Fantasy'],
                'total_copies': 5,
                'available_copies': 5,
                'description': 'An epic high-fantasy novel that follows the quest to destroy the One Ring.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8314135-L.jpg'
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'isbn': '9780062315007',
                'category': categories['Fiction'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A mystical story about following your dreams and finding your destiny.',
                'cover_image': 'https://covers.openlibrary.org/b/id/7895088-L.jpg'
            },
            {
                'title': 'The Art of Computer Programming',
                'author': 'Donald E. Knuth',
                'isbn': '9780201896831',
                'category': categories['Technology'],
                'total_copies': 2,
                'available_copies': 2,
                'description': 'A comprehensive monograph written by Donald Knuth that covers many kinds of programming algorithms and their analysis.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8239985-L.jpg'
            },
            {
                'title': 'The Origin of Species',
                'author': 'Charles Darwin',
                'isbn': '9780451529065',
                'category': categories['Science'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A groundbreaking work of scientific literature that is considered to be the foundation of evolutionary biology.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8321547-L.jpg'
            },
            {
                'title': 'The Power of Habit',
                'author': 'Charles Duhigg',
                'isbn': '9781400069286',
                'category': categories['Non-Fiction'],
                'total_copies': 4,
                'available_copies': 4,
                'description': 'An examination of the science behind habit creation and reformation.',
                'cover_image': 'https://covers.openlibrary.org/b/id/7279915-L.jpg'
            },
            {
                'title': 'The Da Vinci Code',
                'author': 'Dan Brown',
                'isbn': '9780307474278',
                'category': categories['Fiction'],
                'total_copies': 5,
                'available_copies': 5,
                'description': 'A mystery thriller novel that follows a symbologist uncovering a religious mystery.',
                'cover_image': 'https://covers.openlibrary.org/b/id/7890195-L.jpg'
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt, David Thomas',
                'isbn': '9780201616224',
                'category': categories['Technology'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A guide to software development best practices and principles.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8520883-L.jpg'
            },
            {
                'title': 'The Selfish Gene',
                'author': 'Richard Dawkins',
                'isbn': '9780198788607',
                'category': categories['Science'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A book on evolution that introduces the influential concept of the selfish gene.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8760472-L.jpg'
            },
            {
                'title': 'The Name of the Wind',
                'author': 'Patrick Rothfuss',
                'isbn': '9780756404741',
                'category': categories['Fantasy'],
                'total_copies': 4,
                'available_copies': 4,
                'description': 'An epic fantasy about a young man who becomes a legend.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8266489-L.jpg'
            },
            {
                'title': 'The Lean Startup',
                'author': 'Eric Ries',
                'isbn': '9780307887894',
                'category': categories['Non-Fiction'],
                'total_copies': 4,
                'available_copies': 4,
                'description': 'A new approach to business that's being adopted around the world.',
                'cover_image': 'https://covers.openlibrary.org/b/id/7205042-L.jpg'
            },
            {
                'title': 'Foundation',
                'author': 'Isaac Asimov',
                'isbn': '9780553293357',
                'category': categories['Science Fiction'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'The first novel in Asimov's Foundation Series, about the decline and rebirth of a galactic empire.',
                'cover_image': 'https://covers.openlibrary.org/b/id/9278726-L.jpg'
            },
            {
                'title': 'Jane Eyre',
                'author': 'Charlotte Brontë',
                'isbn': '9780141441146',
                'category': categories['Romance'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A novel that revolutionized the art of fiction and follows the emotions and experiences of its eponymous heroine.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8322915-L.jpg'
            },
            {
                'title': 'The Art of War',
                'author': 'Sun Tzu',
                'isbn': '9780140439199',
                'category': categories['Non-Fiction'],
                'total_copies': 5,
                'available_copies': 5,
                'description': 'An ancient Chinese military treatise that has influenced both military and business tactics.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8434707-L.jpg'
            },
            {
                'title': 'Wuthering Heights',
                'author': 'Emily Brontë',
                'isbn': '9780141439556',
                'category': categories['Romance'],
                'total_copies': 3,
                'available_copies': 3,
                'description': 'A classic novel of passionate love and revenge on the Yorkshire moors.',
                'cover_image': 'https://covers.openlibrary.org/b/id/8314243-L.jpg'
            }
        ]

        for book_data in sample_books:
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data['isbn'],
                category_id=book_data['category'].id,
                total_copies=book_data['total_copies'],
                available_copies=book_data['available_copies'],
                description=book_data['description'],
                cover_image=book_data['cover_image']
            )
            db.session.add(book)
        
        db.session.commit()
        print("Sample books added successfully!")

if __name__ == '__main__':
    add_sample_books() 