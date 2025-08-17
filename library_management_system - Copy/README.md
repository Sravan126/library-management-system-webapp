# Library Management System

A modern, user-friendly web application for managing library operations, built with Flask and Bootstrap 5.

## Features

- **Homepage** – Welcoming banner, search bar for books, and quick links to login/register.
- **User Dashboard** – Displays borrowed books, due dates, and fines.
- **Admin Panel** – For adding, updating, and deleting books, managing users, and tracking inventory.
- **Book Catalog** – Lists available books with search, filter, and borrow options.
- **Borrow & Return System** – Borrow books, return them, and receive automatic fine calculations.
- **Responsive Design** – Optimized for desktop and mobile.
- **Authentication** – Role-based access for users and administrators.

## Installation

1. Clone the repository
   ```
   git clone <repository-url>
   cd library_management_system
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables (optional)
   ```
   # Create .env file
   SECRET_KEY=your_secret_key_here
   ```

5. Initialize the database
   ```
   python app.py
   ```

## Usage

1. Run the application
   ```
   python app.py
   ```

2. Access the application in your web browser
   ```
   http://localhost:5000
   ```

3. Default admin account
   - Email: admin@example.com
   - Password: admin123

4. Default user account
   - Email: user@example.com
   - Password: user123

## Admin Features

- Add, edit, and delete books
- Manage user accounts and roles
- View borrowing statistics and overdue books
- Monitor library inventory

## User Features

- Browse and search the book catalog
- Filter books by category
- Borrow and return books
- View borrowing history and due dates
- Check fines for overdue books

## Project Structure

```
library_management_system/
│
├── app.py                     # Main application file
├── models/                    # Database models
│   ├── __init__.py
│   └── models.py              # SQLAlchemy models
│
├── static/                    # Static files
│   ├── css/
│   │   └── styles.css         # Custom CSS
│   ├── js/
│   │   └── scripts.js         # Custom JavaScript
│   └── images/
│       └── library_hero.svg   # Hero image
│
├── templates/                 # HTML templates
│   ├── index.html             # Homepage
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # User dashboard
│   ├── catalog.html           # Book catalog
│   └── admin/                 # Admin templates
│       ├── panel.html         # Admin panel
│       ├── add_book.html      # Add book form
│       ├── edit_book.html     # Edit book form
│       └── manage_users.html  # User management
│
└── requirements.txt           # Python dependencies
```

## Technology Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, CSS, JavaScript
- **Database**: SQLite (can be easily changed to other databases)
- **Authentication**: Flask-Login

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) 