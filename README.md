# Smart Function Recommender for Developers

A powerful tool that converts natural language descriptions of programming tasks into **reusable code snippets or functions** to help developers save time and improve productivity.

## 🚀 Features

- **Natural Language Input** – Describe coding tasks in plain English
- **Multi-Language Support** – Get code in Python, JavaScript, Java, C#, Go, Rust, and more
- **Intelligent Function Lookup** – Search curated database of reusable functions
- **Ranked Recommendations** – Get top 3–5 code snippets with relevance scores
- **Ready-to-Use Code** – Copy-paste ready snippets with documentation
- **CLI & Library** – Use as a command-line tool or import as a Python library
- **Web Interface** – Beautiful web UI with language selector (optional)

## 📦 Installation

### From Source

```bash
git clone https://github.com/yourusername/smart-func.git
cd smart-func
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install smart-func
```

## 💻 Usage

### As a Python Library

```python
from smart_func import get_function, recommend_functions

# Get a single recommendation (Python by default)
result = get_function("Sort a list of numbers in descending order and remove duplicates")
print(result['code'])

# Get code in a specific language
js_result = get_function("sort list descending", language="javascript")
java_result = get_function("merge dictionaries", language="java")
go_result = get_function("reverse string", language="go")

# Get multiple recommendations with language filter
results = recommend_functions("merge two dictionaries", top_k=3, language="csharp")
for func in results:
    print(f"{func['name']} ({func['language']}): {func['relevance_score']:.2%}")
```

### As a CLI Tool

```bash
# Basic usage
smart-func "sort a list in descending order and remove duplicates"

# Get top 3 recommendations
smart-func "merge two dictionaries" --top 3

# Code only output
smart-func "find maximum value in list" --code-only

# JSON output
smart-func "reverse a string" --json
```

## 📋 Example Output

```python
============================================================
Function: sort_unique_desc
============================================================

def sort_unique_desc(numbers):
    """Sorts a list in descending order and removes duplicates"""
    return sorted(set(numbers), reverse=True)

Description: Sorts a list in descending order and removes duplicates

Usage Example:
result = sort_unique_desc([3, 1, 4, 1, 5, 9, 2, 6, 5])
# Returns: [9, 6, 5, 4, 3, 2, 1]

Complexity: O(n log n) | Relevance: 95.00% | Popularity: 8/10
```

## 🏗️ How It Works

```
User Input (Task Description)
         ↓
 NLP Parsing (Intent Extraction, Keyword Identification)
         ↓
 Function Search (Curated Database)
         ↓
 Ranking & Filtering (Relevance, Popularity, Context Matching)
         ↓
 Output Recommendation (Code snippet + Metadata + Documentation)
```

1. **NLP Parsing:** Extracts the main intent, keywords, and data types from user input
2. **Function Search:** Maps the intent to relevant functions from a curated library
3. **Ranking:** Functions ranked based on relevance score, popularity, and code simplicity
4. **Output:** Returns ready-to-use code snippet with proper documentation

## 📚 Supported Languages & Functions

### Programming Languages
- **Python** - Full coverage (20+ functions)
- **JavaScript** - Common operations (sort, merge, reverse, find max)
- **Java** - List operations, string manipulation, map merging
- **C#** - LINQ operations, dictionary merging, string reversal
- **Go** - Slice operations, string manipulation, max finding
- **Rust** - Vector operations, string reversal, max finding

### Function Categories
- **Sorting & Ordering:** Sort lists/arrays, remove duplicates, reverse
- **Data Manipulation:** Merge dictionaries/objects/maps, filter lists, transform data
- **Search & Find:** Find max/min, search in collections
- **Calculations:** Sum, count, average operations
- **String Operations:** Reverse, count words, validate formats
- **Data Validation:** Email validation, format checking
- **Parsing:** CSV parsing, data extraction

The database is continuously expanding with more languages and functions!

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=smart_func
```

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/yourusername/smart-func.git
cd smart-func

# Install in development mode
pip install -e .

# Run tests
pytest tests/
```

## 📝 Project Structure

```
smart_func/
│
├── smart_func/
│   ├── __init__.py          # Package initialization
│   ├── generator.py         # Core function recommender logic
│   ├── nlp.py               # NLP parsing and intent extraction
│   ├── cli.py               # Command-line interface
│   └── database.json        # Curated library of reusable functions
│
├── tests/
│   └── test_generator.py    # Unit tests
│
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
└── README.md                # This file
```

## 🌐 Web Interface

A beautiful web interface is available! 

```bash
# Install web dependencies
cd web_app
pip install -r requirements.txt

# Run the web app
python app.py
```

Then open http://localhost:8000 in your browser.

See `web_app/README.md` for more details.

## 🚧 Roadmap

- [x] Web interface for demo and API access ✅
- [ ] Support for multiple programming languages (JavaScript, Java, etc.)
- [ ] AI-powered code generation for missing functions
- [ ] IDE integrations (VSCode, JetBrains)
- [ ] Analytics: track popular requested functions
- [ ] Cloud-hosted API for developer integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the need to improve developer productivity
- Built with Python and modern NLP techniques

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/smart-func](https://github.com/yourusername/smart-func)

---

**Made with ❤️ for developers**
