# Smart Function Recommender - Web Interface

A beautiful web interface for the Smart Function Recommender.

## 🚀 Quick Start

### Installation

```bash
# Install web app dependencies
cd web_app
pip install -r requirements.txt
```

### Run the Web App

```bash
# From the web_app directory
python app.py

# Or using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Access the Web Interface

Open your browser and navigate to:
- **Web Interface**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/api/health

## 📡 API Endpoints

### POST `/api/search`

Search for functions based on a natural language query.

**Request Body:**
```json
{
  "query": "sort a list in descending order and remove duplicates",
  "top_k": 3
}
```

**Response:**
```json
[
  {
    "id": "sort_desc_unique",
    "name": "sort_unique_desc",
    "code": "def sort_unique_desc(numbers):\n    ...",
    "description": "Sorts a list in descending order and removes duplicates",
    "relevance_score": 0.95,
    "usage": "result = sort_unique_desc([3, 1, 4, 1, 5, 9, 2, 6, 5])",
    "complexity": "O(n log n)",
    "popularity": 8
  }
]
```

### GET `/api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Smart Function Recommender"
}
```

## 🎨 Features

- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Search**: Instant function recommendations
- **Multiple Results**: View top 1, 3, or 5 recommendations
- **Copy to Clipboard**: One-click code copying
- **Example Queries**: Quick-start examples
- **Responsive Design**: Works on desktop and mobile

## 🛠️ Development

### Run in Development Mode

```bash
uvicorn app:app --reload
```

The `--reload` flag enables auto-reload on code changes.

### Customize Port

```bash
uvicorn app:app --port 8080
```

## 📝 Notes

- The web app requires the main `smart_func` package to be installed
- Make sure you're in the project root or have `smart_func` in your Python path
- The web interface is built with vanilla HTML/CSS/JavaScript (no framework dependencies)
