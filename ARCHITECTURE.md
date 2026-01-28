# System Architecture

## How Data is Stored

### Current System: JSON File (Not a Database)

The system currently uses a **JSON file** (`smart_func/database.json`) to store all function definitions. This is NOT a traditional database like MySQL, PostgreSQL, or MongoDB.

**Why JSON?**
- ✅ Simple and easy to understand
- ✅ No database setup required
- ✅ Easy to edit and maintain
- ✅ Fast for small to medium datasets
- ✅ Works out of the box

**How it works:**
1. All functions are stored in `smart_func/database.json` as a JSON array
2. When the system starts, it loads the entire JSON file into memory
3. Functions are searched and filtered in memory
4. No database queries - just Python list operations

**File Structure:**
```json
[
  {
    "id": "function_id",
    "name": "function_name",
    "description": "What it does",
    "code": "function code here",
    "language": "python",
    "keywords": ["keyword1", "keyword2"],
    "action": "sort",
    "data_type": "list",
    "usage": "example usage",
    "complexity": "O(n)",
    "popularity": 8
  },
  ...
]
```

## Data Flow

```
User Query
    ↓
NLP Parser (extracts intent, keywords)
    ↓
Load database.json (all functions)
    ↓
Filter by language (if specified)
    ↓
Calculate relevance scores for each function
    ↓
Sort by relevance + popularity
    ↓
Return top K results
```

## Future Improvements

### Option 1: SQLite Database
- **Pros**: Structured queries, indexing, better for large datasets
- **Cons**: Requires database setup, more complex

### Option 2: MongoDB
- **Pros**: Flexible schema, good for JSON-like data
- **Cons**: Requires MongoDB server, more overhead

### Option 3: Keep JSON but Add Caching
- **Pros**: Simple, fast with caching
- **Cons**: Still limited for very large datasets

### Option 4: Hybrid Approach
- Keep JSON for development/easy editing
- Add optional database backend for production
- Best of both worlds

## Current Performance

- **Loading time**: < 100ms for ~50 functions
- **Search time**: < 50ms per query
- **Memory usage**: ~500KB for full database
- **Scalability**: Good up to ~1000 functions

## Recommendations

For now, **JSON is perfect** because:
1. We have ~50 functions (very manageable)
2. No complex queries needed
3. Easy to maintain and update
4. Fast enough for real-time use

**Consider database when:**
- Function count exceeds 1000+
- Need complex queries (joins, aggregations)
- Multiple users accessing simultaneously
- Need transaction support
