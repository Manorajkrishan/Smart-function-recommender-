"""
Migrate JSON database to SQLite for production use.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_func.database import migrate_to_sqlite

def main():
    """Migrate JSON to SQLite."""
    print("Migrating JSON database to SQLite...")
    
    json_path = os.path.join(os.path.dirname(__file__), 'database.json')
    db_path = os.path.join(os.path.dirname(__file__), 'functions.db')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found!")
        return
    
    migrated = migrate_to_sqlite(json_path, db_path)
    
    print(f"SUCCESS: Migrated {migrated} functions to SQLite database")
    print(f"Database location: {db_path}")
    print("\nThe system will now use SQLite for better performance!")

if __name__ == '__main__':
    main()
