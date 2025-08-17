from app import app, db
from models.models import Book, Category

def add_category_books():
    with app.app_context():
        # Delete existing books
        Book.query.delete()
        db.session.commit()
        print("Existing books deleted.")

        # Get existing categories
        categories = {
            category.name: category
            for category in Category.query.all()
        }

        # Additional books by category
        new_books = {
            'Fiction': [
                {
                    'title': 'One Hundred Years of Solitude',
                    'author': 'Gabriel García Márquez',
                    'isbn': '9780060883287',
                    'total_copies': 3,
                    'description': 'A landmark of magical realism and one of the most influential literary works of our time.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780060883287-L.jpg',
                    'token_cost': 8
                },
                {
                    'title': 'The Kite Runner',
                    'author': 'Khaled Hosseini',
                    'isbn': '9781594631931',
                    'total_copies': 4,
                    'description': 'A heartbreaking story of family, love, and redemption against the backdrop of Afghanistan\'s history.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9781594631931-L.jpg',
                    'token_cost': 7
                },
                {
                    'title': 'The Book Thief',
                    'author': 'Markus Zusak',
                    'isbn': '9780375842207',
                    'total_copies': 4,
                    'description': 'A story about the power of books and words, narrated by Death during World War II.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780375842207-L.jpg',
                    'token_cost': 6
                },
                {
                    'title': 'Life of Pi',
                    'author': 'Yann Martel',
                    'isbn': '9780156027328',
                    'total_copies': 3,
                    'description': 'A fantasy adventure novel about survival at sea with a Bengal tiger.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780156027328-L.jpg',
                    'token_cost': 6
                }
            ],
            'Science Fiction': [
                {
                    'title': 'Neuromancer',
                    'author': 'William Gibson',
                    'isbn': '9780441569595',
                    'total_copies': 3,
                    'description': 'A groundbreaking cyberpunk novel that coined the term "cyberspace".',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780441569595-L.jpg',
                    'token_cost': 7
                },
                {
                    'title': 'The Hitchhiker\'s Guide to the Galaxy',
                    'author': 'Douglas Adams',
                    'isbn': '9780345391803',
                    'total_copies': 5,
                    'description': 'A comedy science fiction series following the adventures of Arthur Dent.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780345391803-L.jpg',
                    'token_cost': 5
                },
                {
                    'title': 'Ender\'s Game',
                    'author': 'Orson Scott Card',
                    'isbn': '9780812550702',
                    'total_copies': 4,
                    'description': 'A military science fiction novel about a gifted child trained to become Earth\'s greatest military leader.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780812550702-L.jpg',
                    'token_cost': 6
                },
                {
                    'title': 'Snow Crash',
                    'author': 'Neal Stephenson',
                    'isbn': '9780553380958',
                    'total_copies': 3,
                    'description': 'A science fiction novel exploring virtual reality, linguistics, and ancient Sumerian mythology.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780553380958-L.jpg',
                    'token_cost': 7
                }
            ],
            'Fantasy': [
                {
                    'title': 'American Gods',
                    'author': 'Neil Gaiman',
                    'isbn': '9780380789030',
                    'total_copies': 4,
                    'description': 'A blend of Americana, fantasy, and mythology following an ex-convict caught between old and new gods.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780380789030-L.jpg',
                    'token_cost': 8
                },
                {
                    'title': 'The Way of Kings',
                    'author': 'Brandon Sanderson',
                    'isbn': '9780765326355',
                    'total_copies': 3,
                    'description': 'An epic fantasy novel set in a world of stone and storms.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780765326355-L.jpg',
                    'token_cost': 9
                },
                {
                    'title': 'The Night Circus',
                    'author': 'Erin Morgenstern',
                    'isbn': '9780385534635',
                    'total_copies': 4,
                    'description': 'A magical competition between two illusionists set in a mysterious circus.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780385534635-L.jpg',
                    'token_cost': 7
                }
            ],
            'Science': [
                {
                    'title': 'Cosmos',
                    'author': 'Carl Sagan',
                    'isbn': '9780345539435',
                    'total_copies': 4,
                    'description': 'A journey through space-time exploring the mysteries of our universe.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780345539435-L.jpg',
                    'token_cost': 6
                },
                {
                    'title': 'The Elegant Universe',
                    'author': 'Brian Greene',
                    'isbn': '9780393338102',
                    'total_copies': 3,
                    'description': 'An exploration of string theory and the nature of our universe.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780393338102-L.jpg',
                    'token_cost': 7
                },
                {
                    'title': 'The Immortal Life of Henrietta Lacks',
                    'author': 'Rebecca Skloot',
                    'isbn': '9781400052189',
                    'total_copies': 4,
                    'description': 'The story of HeLa cells and their impact on medical research.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9781400052189-L.jpg',
                    'token_cost': 6
                }
            ],
            'Technology': [
                {
                    'title': 'Design Patterns',
                    'author': 'Erich Gamma et al.',
                    'isbn': '9780201633610',
                    'total_copies': 3,
                    'description': 'A seminal book on software design patterns and reusable object-oriented software.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780201633610-L.jpg',
                    'token_cost': 8
                },
                {
                    'title': 'Code Complete',
                    'author': 'Steve McConnell',
                    'isbn': '9780735619678',
                    'total_copies': 4,
                    'description': 'A comprehensive guide to software construction and programming practice.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780735619678-L.jpg',
                    'token_cost': 7
                },
                {
                    'title': 'Zero to One',
                    'author': 'Peter Thiel',
                    'isbn': '9780804139298',
                    'total_copies': 5,
                    'description': 'Notes on startups and how to build the future of technology.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780804139298-L.jpg',
                    'token_cost': 5
                }
            ],
            'Romance': [
                {
                    'title': 'Outlander',
                    'author': 'Diana Gabaldon',
                    'isbn': '9780440212560',
                    'total_copies': 4,
                    'description': 'A time-travel romance set in 18th century Scotland.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780440212560-L.jpg',
                    'token_cost': 6
                },
                {
                    'title': 'The Notebook',
                    'author': 'Nicholas Sparks',
                    'isbn': '9780446520805',
                    'total_copies': 5,
                    'description': 'A love story about the enduring power of true love.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780446520805-L.jpg',
                    'token_cost': 5
                },
                {
                    'title': 'Me Before You',
                    'author': 'Jojo Moyes',
                    'isbn': '9780143124542',
                    'total_copies': 4,
                    'description': 'A heartbreaking modern love story about two people from different worlds.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780143124542-L.jpg',
                    'token_cost': 6
                }
            ],
            'Non-Fiction': [
                {
                    'title': 'Thinking, Fast and Slow',
                    'author': 'Daniel Kahneman',
                    'isbn': '9780374533557',
                    'total_copies': 4,
                    'description': 'An analysis of the two systems that drive the way we think.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780374533557-L.jpg',
                    'token_cost': 7
                },
                {
                    'title': 'Educated',
                    'author': 'Tara Westover',
                    'isbn': '9780399590504',
                    'total_copies': 5,
                    'description': 'A memoir about a woman who leaves her survivalist family to pursue education.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780399590504-L.jpg',
                    'token_cost': 6
                },
                {
                    'title': 'Atomic Habits',
                    'author': 'James Clear',
                    'isbn': '9780735211292',
                    'total_copies': 5,
                    'description': 'A guide to building good habits and breaking bad ones.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg',
                    'token_cost': 5
                },
                {
                    'title': 'Sapiens: A Graphic History',
                    'author': 'Yuval Noah Harari',
                    'isbn': '9780063051331',
                    'total_copies': 3,
                    'description': 'The graphic novel adaptation of the bestselling book about human history.',
                    'cover_image': 'https://covers.openlibrary.org/b/isbn/9780063051331-L.jpg',
                    'token_cost': 7
                }
            ]
        }

        # Add books for each category
        for category_name, books in new_books.items():
            category = categories[category_name]
            for book_data in books:
                book = Book(
                    title=book_data['title'],
                    author=book_data['author'],
                    isbn=book_data['isbn'],
                    category_id=category.id,
                    total_copies=book_data['total_copies'],
                    available_copies=book_data['total_copies'],
                    description=book_data['description'],
                    cover_image=book_data['cover_image'],
                    token_cost=book_data['token_cost']
                )
                db.session.add(book)
        
        db.session.commit()
        print("Additional category books added successfully!")

if __name__ == '__main__':
    add_category_books() 