#!/usr/bin/env python
"""
Run script for the Library Management System
This script provides a convenient way to start the application and initialize the database
"""

import argparse
import os
from app import app

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run the Library Management System')
    parser.add_argument('--init-db', action='store_true',
                        help='Initialize the database with sample data before starting')
    parser.add_argument('--port', type=int, default=5000,
                        help='Port to run the application on (default: 5000)')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Host to run the application on (default: 127.0.0.1)')
    parser.add_argument('--debug', action='store_true',
                        help='Run the application in debug mode')
    
    return parser.parse_args()

def main():
    """Main function to run the application"""
    args = parse_args()
    
    if args.init_db:
        print("Initializing database with sample data...")
        from init_db import init_db
        init_db()
    
    # Set default port from environment variable if available
    port = int(os.environ.get('PORT', args.port))
    
    # Run the application
    print(f"Starting Library Management System on http://{args.host}:{port}")
    app.run(host=args.host, port=port, debug=args.debug)

if __name__ == '__main__':
    main() 