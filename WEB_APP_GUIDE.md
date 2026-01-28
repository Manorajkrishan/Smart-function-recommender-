# Web Interface Guide

## ✅ Yes! The project now has a web frontend!

A beautiful, modern web interface has been added to the Smart Function Recommender.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd web_app
pip install -r requirements.txt
```

### 2. Run the Web App

```bash
# From web_app directory
python app.py

# Or from project root
cd web_app && python app.py
```

### 3. Open in Browser

Navigate to: **http://localhost:8000**

## 🎨 Features

- **Beautiful Modern UI** - Gradient design with smooth animations
- **Real-time Search** - Instant function recommendations as you type
- **Multiple Results** - View top 1, 3, or 5 recommendations
- **Copy to Clipboard** - One-click code copying
- **Example Queries** - Quick-start example buttons
- **Responsive Design** - Works on desktop, tablet, and mobile
- **API Endpoints** - RESTful API for integration

## 📡 API Usage

### Search Functions

```bash
curl -X POST "http://localhost:8000/api/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "sort a list in descending order", "top_k": 3}'
```

### Health Check

```bash
curl http://localhost:8000/api/health
```

## 🖼️ Web Interface Preview

The web interface includes:
- Clean, modern design with gradient backgrounds
- Search input with dropdown for result count
- Example query buttons for quick testing
- Result cards showing:
  - Function name and relevance score
  - Code snippet with syntax highlighting
  - Usage examples
  - Metadata (complexity, popularity)
  - Copy to clipboard button

## 🔧 Customization

### Change Port

Edit `web_app/app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Change 8000 to your port
```

### API Documentation

FastAPI automatically generates interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
web_app/
├── app.py              # FastAPI application
├── requirements.txt    # Web dependencies
├── README.md          # Web app documentation
├── run.sh             # Linux/Mac run script
└── run.bat            # Windows run script
```

## 🎯 Example Usage

1. Start the server: `python web_app/app.py`
2. Open browser: http://localhost:8000
3. Type a query: "find the upper case"
4. Click "Search" or press Enter
5. View results and copy code!

## 🌐 Deployment

### Local Development
```bash
uvicorn app:app --reload
```

### Production
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Docker (Future)
The web app can be containerized for easy deployment.

---

**Enjoy the web interface! 🎉**
