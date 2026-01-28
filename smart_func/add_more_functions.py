"""
Script to add more functions to improve accuracy.
Focus on Python and JavaScript functions that are commonly requested.
"""

import json
import os

# Additional functions to add
additional_functions = [
    # Python - String operations
    {
        "id": "title_case_py",
        "name": "title_case",
        "description": "Converts a string to title case (each word capitalized)",
        "code": "def title_case(text):\n    \"\"\"Converts a string to title case (each word capitalized)\"\"\"\n    return text.title()",
        "action": "transform",
        "data_type": "string",
        "keywords": ["title", "case", "capitalize", "each", "word", "string", "text"],
        "language": "python",
        "usage": "result = title_case('hello world')\n# Returns: 'Hello World'",
        "complexity": "O(n)",
        "popularity": 7
    },
    {
        "id": "strip_whitespace_py",
        "name": "strip_whitespace",
        "description": "Removes leading and trailing whitespace from a string",
        "code": "def strip_whitespace(text):\n    \"\"\"Removes leading and trailing whitespace from a string\"\"\"\n    return text.strip()",
        "action": "clean",
        "data_type": "string",
        "keywords": ["strip", "trim", "whitespace", "remove", "string", "text", "clean"],
        "language": "python",
        "usage": "result = strip_whitespace('  hello world  ')\n# Returns: 'hello world'",
        "complexity": "O(n)",
        "popularity": 9
    },
    # Python - List operations
    {
        "id": "get_last_n_py",
        "name": "get_last_n",
        "description": "Gets the last N items from a list",
        "code": "def get_last_n(items, count):\n    \"\"\"Gets the last N items from a list\"\"\"\n    return items[-count:] if count > 0 else []",
        "action": "slice",
        "data_type": "list",
        "keywords": ["last", "items", "list", "array", "slice", "end", "tail"],
        "language": "python",
        "usage": "result = get_last_n([1, 2, 3, 4, 5], 3)\n# Returns: [3, 4, 5]",
        "complexity": "O(n)",
        "popularity": 7
    },
    {
        "id": "count_occurrences_py",
        "name": "count_occurrences",
        "description": "Counts how many times an item appears in a list",
        "code": "def count_occurrences(items, item):\n    \"\"\"Counts how many times an item appears in a list\"\"\"\n    return items.count(item)",
        "action": "calculate",
        "data_type": "list",
        "keywords": ["count", "occurrences", "times", "appears", "list", "item", "frequency"],
        "language": "python",
        "usage": "result = count_occurrences([1, 2, 2, 3, 2], 2)\n# Returns: 3",
        "complexity": "O(n)",
        "popularity": 8
    },
    # JavaScript - Additional functions
    {
        "id": "titleCase_js",
        "name": "titleCase",
        "description": "Converts a string to title case (each word capitalized)",
        "code": "function titleCase(text) {\n    /** Converts a string to title case (each word capitalized) */\n    return text.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');\n}",
        "action": "transform",
        "data_type": "string",
        "keywords": ["title", "case", "capitalize", "each", "word", "string", "text"],
        "language": "javascript",
        "usage": "const result = titleCase('hello world');\n// Returns: 'Hello World'",
        "complexity": "O(n)",
        "popularity": 7
    },
    {
        "id": "trimString_js",
        "name": "trimString",
        "description": "Removes whitespace from both ends of a string",
        "code": "function trimString(text) {\n    /** Removes whitespace from both ends of a string */\n    return text.trim();\n}",
        "action": "clean",
        "data_type": "string",
        "keywords": ["trim", "strip", "whitespace", "remove", "string", "text", "clean"],
        "language": "javascript",
        "usage": "const result = trimString('  hello world  ');\n// Returns: 'hello world'",
        "complexity": "O(n)",
        "popularity": 9
    },
    {
        "id": "getLastN_js",
        "name": "getLastN",
        "description": "Gets the last N items from an array",
        "code": "function getLastN(array, count) {\n    /** Gets the last N items from an array */\n    return array.slice(-count);\n}",
        "action": "slice",
        "data_type": "list",
        "keywords": ["last", "items", "array", "slice", "end", "tail"],
        "language": "javascript",
        "usage": "const result = getLastN([1, 2, 3, 4, 5], 3);\n// Returns: [3, 4, 5]",
        "complexity": "O(n)",
        "popularity": 7
    },
    {
        "id": "countOccurrences_js",
        "name": "countOccurrences",
        "description": "Counts how many times an item appears in an array",
        "code": "function countOccurrences(array, item) {\n    /** Counts how many times an item appears in an array */\n    return array.filter(x => x === item).length;\n}",
        "action": "calculate",
        "data_type": "list",
        "keywords": ["count", "occurrences", "times", "appears", "array", "item", "frequency"],
        "language": "javascript",
        "usage": "const result = countOccurrences([1, 2, 2, 3, 2], 2);\n// Returns: 3",
        "complexity": "O(n)",
        "popularity": 8
    }
]

def add_functions():
    """Add additional functions to database."""
    db_path = os.path.join(os.path.dirname(__file__), 'database.json')
    
    with open(db_path, 'r', encoding='utf-8') as f:
        functions = json.load(f)
    
    # Check which functions already exist
    existing_ids = {f.get('id') for f in functions}
    
    added = 0
    for func in additional_functions:
        if func['id'] not in existing_ids:
            functions.append(func)
            added += 1
    
    # Save updated database
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(functions, f, indent=2, ensure_ascii=False)
    
    print(f"Added {added} new functions")
    print(f"Total functions: {len(functions)}")
    
    return added

if __name__ == '__main__':
    add_functions()
