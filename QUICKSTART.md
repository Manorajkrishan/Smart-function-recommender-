# Quick Start Guide

## Installation

```bash
# Install in development mode
pip install -e .
```

## Usage Examples

### CLI Usage

```bash
# Basic usage
smart-func "sort a list in descending order and remove duplicates"

# Get top 3 recommendations
smart-func "merge two dictionaries" --top 3

# Code only output
smart-func "reverse a string" --code-only

# JSON output
smart-func "find maximum value" --json
```

### Python Library Usage

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

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=smart_func
```

## Building for Distribution

```bash
# Build source distribution
python setup.py sdist

# Build wheel
python setup.py bdist_wheel

# Upload to PyPI (requires twine)
pip install twine
twine upload dist/*
```

## Project Structure

```
smart_func/
├── smart_func/          # Main package
│   ├── __init__.py      # Package exports
│   ├── generator.py     # Core recommender logic
│   ├── nlp.py           # NLP parsing
│   ├── cli.py           # CLI interface
│   └── database.json    # Function database
├── tests/               # Unit tests
├── setup.py             # Package setup
├── README.md            # Full documentation
└── example.py           # Usage examples
```

## Next Steps

1. **Expand Database**: Add more functions to `smart_func/database.json`
2. **Improve NLP**: Enhance keyword matching and intent detection
3. **Add Languages**: Support JavaScript, Java, etc.
4. **Web Interface**: Create FastAPI/Flask web app
5. **AI Integration**: Add OpenAI/Codex for generating new functions
