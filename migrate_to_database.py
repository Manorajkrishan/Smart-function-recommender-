"""
Migrate from JSON to SQLite database.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from smart_func.database import migrate_to_sqlite

def main():
    """Migrate data from JSON to SQLite."""
    print("Migrating from JSON to SQLite database...")
    
    json_path = os.path.join('smart_func', 'database.json')
    db_path = os.path.join('smart_func', 'functions.db')
    
    migrated = migrate_to_sqlite(json_path, db_path)
    
    print(f"✅ Migrated {migrated} functions to SQLite database")
    print(f"Database location: {db_path}")
    print("\nThe system will now use SQLite for better performance!")

if __name__ == '__main__':
    main()
