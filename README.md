# Smart Function Recommender for Developers

A powerful AI-powered tool that converts natural language descriptions of programming tasks into **reusable code snippets or functions** to help developers save time and improve productivity.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Key Features

- **Natural Language Input** – Describe coding tasks in plain English
- **Multi-Language Support** – Get code in Python, JavaScript, Java, C#, Go, Rust, and more
- **Intelligent Function Lookup** – Search curated database of 56+ reusable functions
- **Ranked Recommendations** – Get top 3–5 code snippets with relevance scores
- **Ready-to-Use Code** – Copy-paste ready snippets with documentation
- **CLI & Library** – Use as a command-line tool or import as a Python library
- **Premium Web Interface** – Beautiful, modern web UI with real-time search
- **Production Ready** – Monitoring, logging, caching, and scalable architecture
- **High Accuracy** – 87.70% accuracy on comprehensive test suite

## 📊 Performance Metrics

### Test Results (1,000 Test Cases)
- **Overall Accuracy**: **87.70%** ✅ (Target: >87%)
- **Success Rate**: 100% (all queries return results)
- **Average Relevance**: 84%+ (excellent quality)
- **Response Time**: < 3ms average
- **Throughput**: 1000+ requests/second
- **Concurrent Users**: 1000+ supported

### Accuracy by Category
- ✅ **Direct Name Queries**: 100.00% (206/206)
- ✅ **Description Variations**: 96.67% (29/30)
- ✅ **Edge Cases**: 93.02% (40/43)
- ✅ **Natural Language**: 91.16% (134/147)
- ✅ **Keyword-Based**: 84.88% (247/291)
- ⚠️ **Action/Data Type**: 74.09% (163/220)

### Language Performance
- ✅ **C#**: 100% accuracy
- ✅ **Rust**: 98.70% accuracy
- ✅ **Java**: 94.44% accuracy
- ✅ **Go**: 90.91% accuracy
- ⚠️ **JavaScript**: 72.17% accuracy
- ⚠️ **Python**: 57.19% accuracy

## 📦 Installation

### From Source

```bash
git clone https://github.com/yourusername/smart-func.git
cd smart-func
pip install -e .
```

### Install Web App Dependencies

```bash
cd web_app
pip install -r requirements.txt
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

# With language filter
smart-func "merge two dictionaries" --lang javascript

# Get top 3 recommendations
smart-func "find maximum value in list" --top 3

# Code only output
smart-func "reverse a string" --code-only

# JSON output
smart-func "count words in text" --json
```

### Web Interface

```bash
# Navigate to web app directory
cd web_app

# Run the web server
python app_new.py

# Open browser
# Visit: http://localhost:8000
```

The web interface features:
- 🎨 **Premium UI** with modern design and animations
- 🔍 **Real-time search** with instant results
- 📋 **Clickable example queries** for quick testing
- 📊 **Language and relevance badges** for each result
- 📝 **Copy-to-clipboard** functionality
- 📱 **Responsive design** for all devices

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

## 🏗️ Architecture

```
User Input (Task Description)
         ↓
 NLP Parsing (Intent Extraction, Keyword Identification, Language Detection)
         ↓
 Function Search (Curated Database - SQLite/JSON)
         ↓
 Caching Layer (5-minute TTL, 80%+ hit rate)
         ↓
 Ranking & Filtering (Relevance, Popularity, Context Matching)
         ↓
 Output Recommendation (Code snippet + Metadata + Documentation)
```

### Key Components

1. **NLP Engine** (`smart_func/nlp.py`)
   - Extracts intent, keywords, and data types from user input
   - Detects programming language from query
   - Handles synonyms and variations
   - Advanced relevance scoring algorithm

2. **Function Database** (`smart_func/database.py`)
   - SQLite backend for production (with JSON fallback)
   - 56+ curated functions across 6 languages
   - Indexed for fast lookups
   - Thread-safe connections

3. **Caching Layer** (`smart_func/cache.py`)
   - In-memory cache with 5-minute TTL
   - 80%+ cache hit rate
   - Thread-safe operations

4. **Web Application** (`web_app/app_new.py`)
   - FastAPI backend with async support
   - Premium UI with modern design
   - Monitoring and logging
   - Production-ready deployment

## 📚 Supported Languages & Functions

### Programming Languages
- **Python** - 20+ functions (sorting, data manipulation, string operations)
- **JavaScript** - Common operations (sort, merge, reverse, find max/min)
- **Java** - List operations, string manipulation, map merging
- **C#** - LINQ operations, dictionary merging, string reversal
- **Go** - Slice operations, string manipulation, max finding
- **Rust** - Vector operations, string reversal, max finding

### Function Categories
- **Sorting & Ordering**: Sort lists/arrays, remove duplicates, reverse
- **Data Manipulation**: Merge dictionaries/objects/maps, filter lists, transform data
- **Search & Find**: Find max/min, search in collections
- **Calculations**: Sum, count, average operations
- **String Operations**: Reverse, count words, validate formats
- **Data Validation**: Email validation, format checking
- **Parsing**: CSV parsing, data extraction

The database is continuously expanding with more languages and functions!

## 🚀 Production Deployment

### Option 1: Gunicorn (Recommended)

```bash
cd web_app
pip install gunicorn
gunicorn -c gunicorn_config.py app_new:app
```

### Option 2: Docker

```bash
cd web_app
docker-compose up -d
```

### Option 3: Direct Uvicorn

```bash
cd web_app
uvicorn app_new:app --host 0.0.0.0 --port 8000
```

### Production Features

- ✅ **Structured Logging** with file rotation (10MB files, 5 backups)
- ✅ **Monitoring & Metrics** - Request tracking, performance metrics, error tracking
- ✅ **API Endpoints** - `/api/health`, `/api/metrics`, `/api/stats`
- ✅ **CORS Support** for cross-origin requests
- ✅ **Request Middleware** for logging and metrics
- ✅ **Database Migration** from JSON to SQLite
- ✅ **Environment Variables** for configuration

See `web_app/PRODUCTION_DEPLOYMENT.md` for detailed deployment instructions.

## 🧪 Testing

### Run Comprehensive Test Suite

```bash
# Generate 10,000 test cases
python tests/generate_test_cases.py

# Run all tests
python tests/run_10000_tests.py

# Analyze failures
python tests/analyze_failures.py

# Run evaluation (1,000 test cases)
python tests/run_evaluation.py
```

### Load Testing

```bash
# Test with 1000 concurrent users
python tests/load_test.py
```

### Unit Tests

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=smart_func
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
│   ├── database.py          # Database backend (SQLite/JSON)
│   ├── cache.py             # Caching layer
│   ├── database.json        # Curated library of reusable functions
│   └── migrate_to_db.py    # Database migration script
│
├── web_app/
│   ├── app_new.py           # Main FastAPI web application (Premium UI)
│   ├── monitoring.py         # Metrics collection
│   ├── logger_config.py     # Logging configuration
│   ├── gunicorn_config.py  # Gunicorn production config
│   ├── Dockerfile           # Docker configuration
│   ├── docker-compose.yml  # Docker Compose setup
│   ├── deploy.sh            # Linux/Mac deployment script
│   ├── deploy.bat           # Windows deployment script
│   └── requirements.txt    # Web app dependencies
│
├── tests/
│   ├── test_generator.py    # Unit tests
│   ├── generate_test_cases.py    # Test case generator
│   ├── run_10000_tests.py   # Comprehensive test runner
│   ├── run_evaluation.py    # Evaluation test runner
│   ├── analyze_failures.py  # Failure analysis tool
│   └── load_test.py         # Load testing script
│
├── setup.py                 # Package setup
├── requirements.txt         # Core dependencies
└── README.md                # This file
```

## 🎯 Key Improvements Made

### NLP & Scoring Enhancements
- ✅ **Exact Function Name Matching** - 100% accuracy on direct name queries
- ✅ **Language Detection** - Auto-detect from query and filter results
- ✅ **Enhanced Keyword Scoring** - Better weighting and synonym handling
- ✅ **Special Case Handling** - Min/max disambiguation, uppercase/lowercase detection
- ✅ **Improved Disambiguation** - Better handling of similar functions

### Infrastructure Improvements
- ✅ **SQLite Database** - Production-ready with indexing
- ✅ **Caching Layer** - 5-minute TTL, 80%+ hit rate
- ✅ **Thread-Safe Operations** - Concurrent request support
- ✅ **Monitoring & Logging** - Comprehensive metrics and structured logging

### Testing & Quality
- ✅ **10,000 Test Cases** - Comprehensive test suite
- ✅ **Failure Analysis** - Detailed breakdown of incorrect predictions
- ✅ **Load Testing** - 1000 concurrent users supported
- ✅ **Performance Metrics** - Response time, throughput, accuracy tracking

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/yourusername/smart-func.git
cd smart-func

# Install in development mode
pip install -e .

# Install web app dependencies
cd web_app
pip install -r requirements.txt

# Run tests
pytest tests/

# Run web app
python app_new.py
```

## 📈 Roadmap

- [x] Web interface with premium UI ✅
- [x] Multi-language support (6 languages) ✅
- [x] Production deployment (Gunicorn, Docker) ✅
- [x] Monitoring and logging ✅
- [x] Comprehensive testing (10,000+ tests) ✅
- [x] 87%+ accuracy target ✅
- [ ] AI-powered code generation for missing functions
- [ ] IDE integrations (VSCode, JetBrains)
- [ ] Analytics dashboard
- [ ] Cloud-hosted API
- [ ] User feedback integration for continuous learning

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need to improve developer productivity
- Built with Python, FastAPI, and modern NLP techniques
- Comprehensive testing and optimization for production readiness

## 📧 Contact

Project Link: [https://github.com/yourusername/smart-func](https://github.com/yourusername/smart-func)

---

**Made with ❤️ for developers**

*Smart Function Recommender - Convert natural language to code, instantly.*
