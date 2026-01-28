# How to Run Smart Function Recommender

## 📦 Installation

First, install the package in development mode:

```bash
pip install -e .
```

Or if you're in the project directory:

```bash
cd e:\Recomender
pip install -e .
```

## 🚀 Running the CLI Tool

After installation, you can use the `smart-func` command from anywhere:

### Basic Usage

```bash
smart-func "sort a list in descending order and remove duplicates"
```

### Get Multiple Recommendations

```bash
smart-func "merge two dictionaries" --top 3
```

### Code Only Output (No Metadata)

```bash
smart-func "reverse a string" --code-only
```

### JSON Output Format

```bash
smart-func "find maximum value" --json
```

### All CLI Options

```bash
smart-func --help
```

## 🐍 Using as Python Library

### In Python Script

```python
from smart_func import get_function, recommend_functions

# Get single recommendation
result = get_function("sort a list in descending order and remove duplicates")
print(result['code'])

# Get multiple recommendations
results = recommend_functions("merge two dictionaries", top_k=3)
for func in results:
    print(func['name'], func['relevance_score'])
```

### Run Example Script

```bash
python example.py
```

### Interactive Python

```bash
python
```

Then in Python:

```python
>>> from smart_func import get_function
>>> result = get_function("sort list descending")
>>> print(result['code'])
```

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Or using Python unittest
python -m pytest tests/ -v

# Run with coverage
pytest tests/ --cov=smart_func
```

## 📝 Example Commands

### Example 1: Sort and Remove Duplicates
```bash
smart-func "sort a list in descending order and remove duplicates"
```

### Example 2: Merge Dictionaries
```bash
smart-func "merge two dictionaries" --top 3
```

### Example 3: Find Maximum
```bash
smart-func "find maximum value in list" --code-only
```

### Example 4: Reverse String
```bash
smart-func "reverse a string"
```

### Example 5: Filter Even Numbers
```bash
smart-func "filter even numbers from list"
```

## 🔧 Troubleshooting

### Command Not Found

If `smart-func` command is not found:

1. Make sure you installed the package: `pip install -e .`
2. Check if Python Scripts directory is in your PATH
3. Try using Python module directly:
   ```bash
   python -m smart_func.cli "your query here"
   ```

### Import Error

If you get import errors:

```bash
# Reinstall the package
pip install -e . --force-reinstall
```

## 📚 Quick Reference

| Task | Command |
|------|---------|
| Install package | `pip install -e .` |
| Run CLI | `smart-func "your query"` |
| Get top 3 | `smart-func "query" --top 3` |
| Code only | `smart-func "query" --code-only` |
| JSON output | `smart-func "query" --json` |
| Run tests | `pytest tests/ -v` |
| Run example | `python example.py` |
