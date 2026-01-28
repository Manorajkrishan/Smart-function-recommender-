# Multi-Language Support

## Overview

Smart Function Recommender now supports multiple programming languages! You can get code snippets in Python, JavaScript, Java, C#, Go, Rust, and more.

## Supported Languages

1. **Python** (default) - Full coverage with 20+ functions
2. **JavaScript** - Common operations
3. **Java** - Enterprise-grade functions
4. **C#** - .NET operations
5. **Go** - System programming functions
6. **Rust** - Memory-safe operations

## Usage Examples

### CLI

```bash
# Python (default)
smart-func "sort list descending"

# JavaScript
smart-func "sort list descending" --lang javascript

# Java
smart-func "merge dictionaries" --lang java

# C#
smart-func "reverse string" --lang csharp

# Go
smart-func "find maximum" --lang go

# Rust
smart-func "sort unique" --lang rust
```

### Python Library

```python
from smart_func import get_function, recommend_functions

# Python (default)
result = get_function("sort list descending")

# JavaScript
js_result = get_function("sort list descending", language="javascript")

# Multiple languages
results = recommend_functions("merge dictionaries", top_k=5, language="java")
```

### Web Interface

1. Open http://localhost:8000
2. Select your preferred language from the dropdown
3. Enter your query
4. Get code in your chosen language!

## Language-Specific Functions

### JavaScript
- `sortUniqueDesc()` - Sort array descending, remove duplicates
- `mergeObjects()` - Merge two objects
- `reverseString()` - Reverse a string
- `findMaximum()` - Find max value in array

### Java
- `sortUniqueDesc()` - Sort list descending, remove duplicates
- `mergeMaps()` - Merge two maps
- `reverseString()` - Reverse a string

### C#
- `SortUniqueDesc()` - Sort list descending, remove duplicates
- `MergeDictionaries()` - Merge two dictionaries
- `ReverseString()` - Reverse a string

### Go
- `SortUniqueDesc()` - Sort slice descending, remove duplicates
- `ReverseString()` - Reverse a string
- `FindMaximum()` - Find max value in slice

### Rust
- `sort_unique_desc()` - Sort vector descending, remove duplicates
- `reverse_string()` - Reverse a string
- `find_maximum()` - Find max value in vector

## Adding More Languages

To add support for a new language:

1. Add functions to `smart_func/database.json` with `"language": "yourlang"`
2. Update CLI choices in `smart_func/cli.py`
3. Update web interface dropdown in `web_app/app.py`
4. Test with: `smart-func "your query" --lang yourlang`

## Future Languages

Planned additions:
- TypeScript
- PHP
- Ruby
- Swift
- Kotlin
- C/C++

## Contributing

Want to add functions in your favorite language? Contributions welcome! Just follow the existing database structure and add functions with proper metadata.
