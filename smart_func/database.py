"""
Database layer for Smart Function Recommender.
Supports both JSON (development) and SQLite (production) backends.
"""

import json
import os
import sqlite3
from typing import List, Dict, Optional
from contextlib import contextmanager
import threading

# Thread-local storage for database connections
_local = threading.local()


class DatabaseBackend:
    """Base class for database backends."""
    
    def get_functions(self, language: Optional[str] = None) -> List[Dict]:
        """Get all functions, optionally filtered by language."""
        raise NotImplementedError
    
    def search_functions(self, query: str, language: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Search functions by keywords."""
        raise NotImplementedError
    
    def get_function_by_id(self, func_id: str) -> Optional[Dict]:
        """Get a function by its ID."""
        raise NotImplementedError
    
    def add_function(self, func: Dict) -> bool:
        """Add a new function to the database."""
        raise NotImplementedError
    
    def update_function(self, func_id: str, func: Dict) -> bool:
        """Update an existing function."""
        raise NotImplementedError
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        raise NotImplementedError


class JSONBackend(DatabaseBackend):
    """JSON file backend (for development)."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'database.json')
        self.db_path = db_path
        self._cache = None
        self._cache_time = 0
    
    def _load_data(self) -> List[Dict]:
        """Load data from JSON file with caching."""
        import time
        current_time = time.time()
        
        # Cache for 5 seconds
        if self._cache is None or (current_time - self._cache_time) > 5:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
            self._cache_time = current_time
        
        return self._cache
    
    def get_functions(self, language: Optional[str] = None) -> List[Dict]:
        data = self._load_data()
        if language:
            language = language.lower()
            return [f for f in data if f.get('language', 'python').lower() == language]
        return data
    
    def search_functions(self, query: str, language: Optional[str] = None, limit: int = 100) -> List[Dict]:
        data = self.get_functions(language)
        query_lower = query.lower()
        results = []
        
        for func in data:
            # Simple keyword matching
            keywords = ' '.join(func.get('keywords', [])).lower()
            name = func.get('name', '').lower()
            description = func.get('description', '').lower()
            
            if query_lower in keywords or query_lower in name or query_lower in description:
                results.append(func)
        
        return results[:limit]
    
    def get_function_by_id(self, func_id: str) -> Optional[Dict]:
        data = self._load_data()
        for func in data:
            if func.get('id') == func_id:
                return func
        return None
    
    def add_function(self, func: Dict) -> bool:
        data = self._load_data()
        data.append(func)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self._cache = None  # Clear cache
        return True
    
    def update_function(self, func_id: str, func: Dict) -> bool:
        data = self._load_data()
        for i, f in enumerate(data):
            if f.get('id') == func_id:
                data[i] = func
                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                self._cache = None  # Clear cache
                return True
        return False
    
    def get_stats(self) -> Dict:
        data = self._load_data()
        languages = {}
        for func in data:
            lang = func.get('language', 'python')
            languages[lang] = languages.get(lang, 0) + 1
        
        return {
            'total_functions': len(data),
            'languages': languages
        }


class SQLiteBackend(DatabaseBackend):
    """SQLite database backend (for production)."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'functions.db')
        self.db_path = db_path
        self._init_database()
    
    @contextmanager
    def _get_connection(self):
        """Get a thread-local database connection."""
        if not hasattr(_local, 'connection'):
            _local.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            _local.connection.row_factory = sqlite3.Row
        yield _local.connection
    
    def _init_database(self):
        """Initialize the database schema."""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS functions (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    code TEXT NOT NULL,
                    language TEXT DEFAULT 'python',
                    action TEXT,
                    data_type TEXT,
                    order_type TEXT,
                    usage TEXT,
                    complexity TEXT,
                    popularity INTEGER DEFAULT 5,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    function_id TEXT NOT NULL,
                    keyword TEXT NOT NULL,
                    FOREIGN KEY (function_id) REFERENCES functions(id) ON DELETE CASCADE
                )
            ''')
            
            # Create indexes for performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_language ON functions(language)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_action ON functions(action)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_data_type ON functions(data_type)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_keyword ON keywords(keyword)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_function_keyword ON keywords(function_id)')
            
            conn.commit()
    
    def _row_to_dict(self, row) -> Dict:
        """Convert a database row to a dictionary."""
        return {
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
            'code': row['code'],
            'language': row['language'],
            'action': row['action'],
            'data_type': row['data_type'],
            'order': row['order_type'],
            'usage': row['usage'],
            'complexity': row['complexity'],
            'popularity': row['popularity']
        }
    
    def get_functions(self, language: Optional[str] = None) -> List[Dict]:
        with self._get_connection() as conn:
            if language:
                cursor = conn.execute(
                    'SELECT * FROM functions WHERE language = ? ORDER BY popularity DESC',
                    (language.lower(),)
                )
            else:
                cursor = conn.execute('SELECT * FROM functions ORDER BY popularity DESC')
            
            results = []
            for row in cursor:
                func = self._row_to_dict(row)
                # Load keywords
                keyword_cursor = conn.execute(
                    'SELECT keyword FROM keywords WHERE function_id = ?',
                    (func['id'],)
                )
                func['keywords'] = [row[0] for row in keyword_cursor]
                results.append(func)
            
            return results
    
    def search_functions(self, query: str, language: Optional[str] = None, limit: int = 100) -> List[Dict]:
        with self._get_connection() as conn:
            query_lower = query.lower()
            
            # Search in keywords, name, and description
            sql = '''
                SELECT DISTINCT f.* FROM functions f
                LEFT JOIN keywords k ON f.id = k.function_id
                WHERE (
                    k.keyword LIKE ? OR
                    f.name LIKE ? OR
                    f.description LIKE ?
                )
            '''
            params = [f'%{query_lower}%', f'%{query_lower}%', f'%{query_lower}%']
            
            if language:
                sql += ' AND f.language = ?'
                params.append(language.lower())
            
            sql += ' ORDER BY f.popularity DESC LIMIT ?'
            params.append(limit)
            
            cursor = conn.execute(sql, params)
            results = []
            for row in cursor:
                func = self._row_to_dict(row)
                keyword_cursor = conn.execute(
                    'SELECT keyword FROM keywords WHERE function_id = ?',
                    (func['id'],)
                )
                func['keywords'] = [row[0] for row in keyword_cursor]
                results.append(func)
            
            return results
    
    def get_function_by_id(self, func_id: str) -> Optional[Dict]:
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT * FROM functions WHERE id = ?', (func_id,))
            row = cursor.fetchone()
            if row:
                func = self._row_to_dict(row)
                keyword_cursor = conn.execute(
                    'SELECT keyword FROM keywords WHERE function_id = ?',
                    (func_id,)
                )
                func['keywords'] = [row[0] for row in keyword_cursor]
                return func
            return None
    
    def add_function(self, func: Dict) -> bool:
        with self._get_connection() as conn:
            try:
                conn.execute('''
                    INSERT INTO functions 
                    (id, name, description, code, language, action, data_type, order_type, usage, complexity, popularity)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    func.get('id'),
                    func.get('name'),
                    func.get('description'),
                    func.get('code'),
                    func.get('language', 'python'),
                    func.get('action'),
                    func.get('data_type'),
                    func.get('order'),
                    func.get('usage'),
                    func.get('complexity'),
                    func.get('popularity', 5)
                ))
                
                # Insert keywords
                keywords = func.get('keywords', [])
                for keyword in keywords:
                    conn.execute(
                        'INSERT INTO keywords (function_id, keyword) VALUES (?, ?)',
                        (func.get('id'), keyword.lower())
                    )
                
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def update_function(self, func_id: str, func: Dict) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT id FROM functions WHERE id = ?', (func_id,))
            if not cursor.fetchone():
                return False
            
            conn.execute('''
                UPDATE functions SET
                    name = ?, description = ?, code = ?, language = ?,
                    action = ?, data_type = ?, order_type = ?, usage = ?,
                    complexity = ?, popularity = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                func.get('name'),
                func.get('description'),
                func.get('code'),
                func.get('language', 'python'),
                func.get('action'),
                func.get('data_type'),
                func.get('order'),
                func.get('usage'),
                func.get('complexity'),
                func.get('popularity', 5),
                func_id
            ))
            
            # Update keywords
            conn.execute('DELETE FROM keywords WHERE function_id = ?', (func_id,))
            keywords = func.get('keywords', [])
            for keyword in keywords:
                conn.execute(
                    'INSERT INTO keywords (function_id, keyword) VALUES (?, ?)',
                    (func_id, keyword.lower())
                )
            
            conn.commit()
            return True
    
    def get_stats(self) -> Dict:
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT language, COUNT(*) as count FROM functions GROUP BY language')
            languages = {row[0]: row[1] for row in cursor}
            
            cursor = conn.execute('SELECT COUNT(*) FROM functions')
            total = cursor.fetchone()[0]
            
            return {
                'total_functions': total,
                'languages': languages
            }
    
    def migrate_from_json(self, json_path: str = None):
        """Migrate data from JSON file to SQLite database."""
        if json_path is None:
            json_path = os.path.join(os.path.dirname(__file__), 'database.json')
        
        if not os.path.exists(json_path):
            print(f"Error: {json_path} not found!")
            return 0
        
        with open(json_path, 'r', encoding='utf-8') as f:
            functions = json.load(f)
        
        migrated = 0
        skipped = 0
        for func in functions:
            # Check if function already exists
            existing = self.get_function_by_id(func.get('id'))
            if existing:
                skipped += 1
                continue
            
            if self.add_function(func):
                migrated += 1
        
        if skipped > 0:
            print(f"Skipped {skipped} functions (already exist)")
        
        return migrated


# Global backend instance
_backend = None


def get_backend(backend_type: str = 'auto', db_path: str = None) -> DatabaseBackend:
    """
    Get the database backend instance.
    
    Args:
        backend_type: 'json', 'sqlite', or 'auto' (auto-detect)
        db_path: Optional path to database file
    """
    global _backend
    
    if _backend is not None:
        return _backend
    
    if backend_type == 'auto':
        # Check if SQLite database exists
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'functions.db')
        
        if os.path.exists(db_path):
            backend_type = 'sqlite'
        else:
            backend_type = 'json'
    
    if backend_type == 'sqlite':
        _backend = SQLiteBackend(db_path)
    else:
        _backend = JSONBackend(db_path)
    
    return _backend


def migrate_to_sqlite(json_path: str = None, db_path: str = None):
    """Migrate from JSON to SQLite database."""
    backend = SQLiteBackend(db_path)
    migrated = backend.migrate_from_json(json_path)
    
    # Verify migration
    stats = backend.get_stats()
    print(f"Database now contains {stats['total_functions']} functions")
    
    return migrated
