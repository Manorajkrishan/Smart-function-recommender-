"""
FastAPI web application for Smart Function Recommender - PREMIUM UI VERSION
With comprehensive monitoring and logging
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
import time
from contextlib import asynccontextmanager

# Add parent directory to path to import smart_func
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from smart_func import get_function, recommend_functions
except ImportError as e:
    print(f"ERROR: Cannot import smart_func: {e}")
    raise

# Import monitoring and logging
# Add current directory to path for imports
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from monitoring import get_metrics
    from logger_config import setup_logging, get_logger
except ImportError as e:
    print(f"Warning: Could not import monitoring/logging modules: {e}")
    print("Creating minimal fallback implementations...")
    # Minimal fallback
    class DummyMetrics:
        def record_request(self, *args, **kwargs): pass
        def record_error(self, *args, **kwargs): pass
        def record_cache_hit(self): pass
        def record_cache_miss(self): pass
        def get_stats(self): return {}
    
    def get_metrics():
        return DummyMetrics()
    
    def setup_logging(*args, **kwargs):
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger("smart_func_recommender")
    
    def get_logger(name="smart_func_recommender"):
        import logging
        return logging.getLogger(name)

# Setup logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = setup_logging(log_level=log_level)
metrics = get_metrics()

logger.info("="*60)
logger.info("🚀 Smart Function Recommender - Starting Application")
logger.info("="*60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Application startup - initializing services...")
    try:
        from smart_func.cache import get_cache
        cache = get_cache()
        logger.info(f"Cache initialized: {cache.get_stats()}")
    except Exception as e:
        logger.warning(f"Cache initialization warning: {e}")
    
    logger.info("✅ Application startup complete")
    yield
    # Shutdown
    logger.info("Application shutdown - cleaning up...")


app = FastAPI(
    title="Smart Function Recommender",
    description="Convert natural language to reusable code snippets",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and track metrics."""
    start_time = time.time()
    endpoint = f"{request.method} {request.url.path}"
    
    # Log request
    logger.info(f"Request: {endpoint} | Client: {request.client.host if request.client else 'unknown'}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Record metrics
        metrics.record_request(endpoint, process_time)
        
        # Add response headers
        response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
        
        # Log response
        logger.info(f"Response: {endpoint} | Status: {response.status_code} | Time: {process_time*1000:.2f}ms")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        error_msg = str(e)
        error_type = type(e).__name__
        
        # Record error
        metrics.record_error(endpoint, error_type, error_msg)
        logger.error(f"Error: {endpoint} | Type: {error_type} | Message: {error_msg} | Time: {process_time*1000:.2f}ms", exc_info=True)
        
        raise


class QueryRequest(BaseModel):
    query: str
    top_k: int = 1
    language: Optional[str] = None


@app.get("/favicon.ico")
async def favicon():
    """Serve favicon to avoid 404 errors."""
    return JSONResponse(content={}, status_code=204)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface with premium design."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Function Recommender - AI Code Assistant</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #8b5cf6;
            --accent: #ec4899;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            --card-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            --card-shadow-hover: 0 30px 80px rgba(0, 0, 0, 0.2);
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-gradient);
            background-attachment: fixed;
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(236, 72, 153, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }
        
        .header-section {
            text-align: center;
            margin-bottom: 40px;
            animation: fadeInDown 0.8s ease-out;
        }
        
        .header-section h1 {
            font-size: 3.5em;
            font-weight: 800;
            color: white;
            margin-bottom: 15px;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            letter-spacing: -0.02em;
        }
        
        .header-section .subtitle {
            font-size: 1.3em;
            color: rgba(255, 255, 255, 0.95);
            font-weight: 400;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .main-card {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            box-shadow: var(--card-shadow);
            overflow: hidden;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }
        
        .search-section {
            padding: 50px;
            background: linear-gradient(to bottom, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.95));
        }
        
        .input-container {
            display: grid;
            grid-template-columns: 1fr auto auto auto;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .search-input-wrapper {
            position: relative;
        }
        
        .search-input-wrapper::before {
            content: '🔍';
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2em;
            z-index: 1;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 18px 20px 18px 55px;
            font-size: 16px;
            border: 2px solid #e5e7eb;
            border-radius: 15px;
            transition: all 0.3s ease;
            background: white;
            font-family: 'Inter', sans-serif;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
            transform: translateY(-1px);
        }
        
        select {
            padding: 18px 20px;
            font-size: 15px;
            border: 2px solid #e5e7eb;
            border-radius: 15px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            min-width: 140px;
        }
        
        select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }
        
        .search-btn {
            padding: 18px 40px;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            white-space: nowrap;
        }
        
        .search-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        }
        
        .search-btn:active {
            transform: translateY(0);
        }
        
        .search-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .examples-section {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid #e5e7eb;
        }
        
        .examples-title {
            font-size: 0.9em;
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 15px;
        }
        
        .examples-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .example-chip {
            padding: 10px 20px;
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            border: 1px solid #d1d5db;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            font-weight: 500;
            color: #374151;
        }
        
        .example-chip:hover {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border-color: transparent;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }
        
        .results-section {
            padding: 0 50px 50px;
        }
        
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-top: 30px;
        }
        
        .results-count {
            font-size: 1.1em;
            color: #6b7280;
            font-weight: 600;
        }
        
        .result-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
            animation: slideIn 0.5s ease-out both;
            position: relative;
            overflow: hidden;
        }
        
        .result-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
            transform: scaleY(0);
            transition: transform 0.3s ease;
        }
        
        .result-card:hover {
            transform: translateX(5px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            border-color: var(--primary);
        }
        
        .result-card:hover::before {
            transform: scaleY(1);
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        
        .result-title-section {
            flex: 1;
        }
        
        .result-number {
            display: inline-block;
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border-radius: 8px;
            text-align: center;
            line-height: 32px;
            font-weight: 700;
            font-size: 0.9em;
            margin-right: 12px;
        }
        
        .result-name {
            font-size: 1.6em;
            font-weight: 700;
            color: #111827;
            display: inline-block;
        }
        
        .result-language {
            display: inline-block;
            padding: 4px 12px;
            background: #f3f4f6;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
            color: #6b7280;
            margin-left: 10px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .relevance-badge {
            padding: 8px 16px;
            background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
            color: white;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
        }
        
        .result-description {
            color: #6b7280;
            font-size: 1.05em;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .code-block {
            background: #1e293b;
            color: #e2e8f0;
            padding: 25px;
            border-radius: 15px;
            overflow-x: auto;
            font-family: 'Fira Code', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.8;
            margin: 20px 0;
            position: relative;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        .code-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        .usage-block {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            color: #334155;
            padding: 20px;
            border-radius: 12px;
            font-family: 'Fira Code', 'Courier New', monospace;
            font-size: 13px;
            margin: 15px 0;
        }
        
        .metadata-row {
            display: flex;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .metadata-badge {
            padding: 8px 16px;
            background: #f1f5f9;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
            color: #475569;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .metadata-badge::before {
            content: '⚡';
            font-size: 1.1em;
        }
        
        .copy-btn {
            margin-top: 20px;
            padding: 12px 30px;
            background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }
        
        .copy-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
        }
        
        .copy-btn:active {
            transform: translateY(0);
        }
        
        .copy-btn.copied {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        .loading {
            text-align: center;
            padding: 60px 20px;
            color: var(--primary);
        }
        
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #e5e7eb;
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        .loading-text {
            font-size: 1.2em;
            font-weight: 600;
            color: #6b7280;
        }
        
        .error {
            background: #fef2f2;
            border: 2px solid var(--error);
            color: #991b1b;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            font-weight: 500;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #6b7280;
        }
        
        .empty-state-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .empty-state-text {
            font-size: 1.2em;
            font-weight: 500;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .input-container {
                grid-template-columns: 1fr;
            }
            
            .header-section h1 {
                font-size: 2.5em;
            }
            
            .search-section {
                padding: 30px 20px;
            }
            
            .results-section {
                padding: 0 20px 30px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-section">
            <h1>🚀 Smart Function Recommender</h1>
            <p class="subtitle">Transform natural language into production-ready code</p>
        </div>
        
        <div class="main-card">
            <div class="search-section">
                <div class="input-container">
                    <div class="search-input-wrapper">
                        <input type="text" id="queryInput" placeholder="Describe what you need... (e.g., 'sort a list in descending order')" />
                    </div>
                    <select id="languageSelect">
                        <option value="">🌐 All Languages</option>
                        <option value="python">🐍 Python</option>
                        <option value="javascript">⚡ JavaScript</option>
                        <option value="java">☕ Java</option>
                        <option value="csharp">🔷 C#</option>
                        <option value="go">🐹 Go</option>
                        <option value="rust">🦀 Rust</option>
                    </select>
                    <select id="topKSelect">
                        <option value="1">Top 1</option>
                        <option value="3">Top 3</option>
                        <option value="5">Top 5</option>
                    </select>
                    <button type="button" id="searchBtn" class="search-btn">Search</button>
                </div>
                
                <div class="examples-section">
                    <div class="examples-title">💡 Try these examples:</div>
                    <div class="examples-grid">
                        <div class="example-chip" data-query="sort a list in descending order and remove duplicates">Sort & Remove Duplicates</div>
                        <div class="example-chip" data-query="merge two dictionaries">Merge Dictionaries</div>
                        <div class="example-chip" data-query="find the upper case">Find Uppercase</div>
                        <div class="example-chip" data-query="calculate the minimum">Find Minimum</div>
                        <div class="example-chip" data-query="reverse a string">Reverse String</div>
                        <div class="example-chip" data-query="count words in text">Count Words</div>
                        <div class="example-chip" data-query="short list">Get Short List</div>
                        <div class="example-chip" data-query="flatten nested list">Flatten List</div>
                    </div>
                </div>
            </div>
            
            <div class="results-section">
                <div id="results"></div>
            </div>
        </div>
    </div>

    <script>
        console.log('🚀 Premium UI Script loaded successfully!');
        
        var searchFunction = async function() {
            console.log('🔍 Search function called');
            var query = document.getElementById('queryInput').value.trim();
            var topK = parseInt(document.getElementById('topKSelect').value);
            var language = document.getElementById('languageSelect').value;
            var resultsDiv = document.getElementById('results');
            var searchBtn = document.getElementById('searchBtn');
            
            if (!query) {
                resultsDiv.innerHTML = '<div class="error">⚠️ Please enter a query</div>';
                return;
            }
            
            searchBtn.disabled = true;
            searchBtn.textContent = 'Searching...';
            
            resultsDiv.innerHTML = '<div class="loading"><div class="loading-spinner"></div><div class="loading-text">Searching for the perfect function...</div></div>';
            
            try {
                var requestBody = { query: query, top_k: topK };
                if (language) {
                    requestBody.language = language;
                }
                
                var response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestBody)
                });
                
                if (!response.ok) {
                    throw new Error('Search failed');
                }
                
                var data = await response.json();
                console.log('✅ API response received:', data);
                displayResults(data);
            } catch (error) {
                console.error('❌ Search error:', error);
                resultsDiv.innerHTML = '<div class="error">❌ Error: ' + error.message + '</div>';
            } finally {
                searchBtn.disabled = false;
                searchBtn.textContent = 'Search';
            }
        };
        
        function displayResults(data) {
            var resultsDiv = document.getElementById('results');
            
            if (!data || (Array.isArray(data) && data.length === 0)) {
                resultsDiv.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🔍</div><div class="empty-state-text">No functions found. Try rephrasing your query.</div></div>';
                return;
            }
            
            var results = Array.isArray(data) ? data : [data];
            var html = '<div class="results-header"><div class="results-count">📊 Found ' + results.length + ' result' + (results.length > 1 ? 's' : '') + '</div></div>';
            
            window.functionCodes = results.map(function(func) { return func.code; });
            
            results.forEach(function(func, index) {
                var relevance = (func.relevance_score * 100).toFixed(1);
                var codeHtml = escapeHtml(func.code);
                var usageHtml = func.usage ? escapeHtml(func.usage) : '';
                
                html += '<div class="result-card" style="animation-delay: ' + (index * 0.1) + 's">';
                html += '<div class="result-header">';
                html += '<div class="result-title-section">';
                html += '<span class="result-number">' + (index + 1) + '</span>';
                html += '<span class="result-name">' + escapeHtml(func.name) + '</span>';
                html += '<span class="result-language">' + (func.language || 'python') + '</span>';
                html += '</div>';
                html += '<div class="relevance-badge">' + relevance + '% Match</div>';
                html += '</div>';
                html += '<div class="result-description">' + escapeHtml(func.description) + '</div>';
                html += '<div class="code-block">' + codeHtml + '</div>';
                if (usageHtml) {
                    html += '<div class="usage-block">' + usageHtml + '</div>';
                }
                html += '<div class="metadata-row">';
                if (func.complexity) {
                    html += '<div class="metadata-badge">Complexity: ' + escapeHtml(func.complexity) + '</div>';
                }
                if (func.popularity) {
                    html += '<div class="metadata-badge">⭐ Popularity: ' + func.popularity + '/10</div>';
                }
                html += '</div>';
                html += '<button class="copy-btn" onclick="copyCode(' + index + ', this)">📋 Copy Code</button>';
                html += '</div>';
            });
            
            resultsDiv.innerHTML = html;
        }
        
        function escapeHtml(text) {
            if (!text) return '';
            var div = document.createElement('div');
            div.textContent = text;
            var escaped = div.innerHTML;
            escaped = escaped.replace(/\\n/g, '<br>');
            escaped = escaped.replace(/\\r\\n/g, '<br>');
            escaped = escaped.replace(/\\r/g, '<br>');
            return escaped;
        }
        
        function copyCode(index, button) {
            var code = window.functionCodes && window.functionCodes[index] ? window.functionCodes[index] : '';
            if (!code) {
                alert('❌ Error: Code not found');
                return;
            }
            
            var originalText = button.textContent;
            
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(code).then(function() {
                    button.textContent = '✅ Copied!';
                    button.classList.add('copied');
                    setTimeout(function() {
                        button.textContent = originalText;
                        button.classList.remove('copied');
                    }, 2000);
                }).catch(function(err) {
                    console.error('Failed to copy:', err);
                    fallbackCopy(code, button, originalText);
                });
            } else {
                fallbackCopy(code, button, originalText);
            }
        }
        
        function fallbackCopy(text, button, originalText) {
            var textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                button.textContent = '✅ Copied!';
                button.classList.add('copied');
                setTimeout(function() {
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }, 2000);
            } catch (e) {
                alert('⚠️ Failed to copy. Please select and copy manually.');
            }
            document.body.removeChild(textArea);
        }
        
        window.searchFunction = searchFunction;
        window.displayResults = displayResults;
        window.escapeHtml = escapeHtml;
        window.copyCode = copyCode;
        
        console.log('✅ All functions initialized');
        
        document.addEventListener('DOMContentLoaded', function() {
            console.log('📄 DOM loaded, setting up event listeners');
            
            var searchBtn = document.getElementById('searchBtn');
            if (searchBtn) {
                searchBtn.addEventListener('click', function() {
                    console.log('🔘 Search button clicked');
                    searchFunction();
                });
            }
            
            var queryInput = document.getElementById('queryInput');
            if (queryInput) {
                queryInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        searchFunction();
                    }
                });
            }
            
            var exampleChips = document.querySelectorAll('.example-chip');
            exampleChips.forEach(function(chip) {
                chip.addEventListener('click', function() {
                    var query = this.getAttribute('data-query');
                    document.getElementById('queryInput').value = query;
                    searchFunction();
                });
            });
            
            console.log('✅ Event listeners attached');
        });
        
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            var searchBtn = document.getElementById('searchBtn');
            if (searchBtn) {
                searchBtn.onclick = function() {
                    console.log('🔘 Search button clicked (onclick)');
                    searchFunction();
                };
            }
        }
        
        console.log('🎉 Script initialization complete!');
    </script>
</body>
</html>"""
    
    return HTMLResponse(content=html, media_type="text/html; charset=utf-8")


@app.post("/api/search")
async def search_functions_api(request: QueryRequest):
    """Search for functions based on natural language query."""
    start_time = time.time()
    logger.info(f"Search request: query='{request.query[:50]}...' | top_k={request.top_k} | language={request.language}")
    
    try:
        if request.top_k == 1:
            result = get_function(request.query, language=request.language)
            if result:
                elapsed = time.time() - start_time
                logger.info(f"Search success: found '{result.get('name', 'unknown')}' | time={elapsed*1000:.2f}ms")
                return [result]
            logger.warning(f"Search: no results found for query='{request.query[:50]}...'")
            return []
        else:
            results = recommend_functions(request.query, top_k=request.top_k, language=request.language)
            elapsed = time.time() - start_time
            logger.info(f"Search success: found {len(results)} results | time={elapsed*1000:.2f}ms")
            return results
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Search error: query='{request.query[:50]}...' | error={str(e)} | time={elapsed*1000:.2f}ms", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint with basic status."""
    return {
        "status": "healthy",
        "service": "Smart Function Recommender",
        "version": "2.0.0",
        "timestamp": time.time()
    }


@app.get("/api/metrics")
async def get_metrics_endpoint():
    """Get comprehensive application metrics."""
    stats = metrics.get_stats()
    logger.debug("Metrics requested")
    return stats


@app.get("/api/stats")
async def get_stats_endpoint():
    """Get simplified statistics for monitoring dashboards."""
    stats = metrics.get_stats()
    return {
        "uptime_hours": round(stats["uptime"]["hours"], 2),
        "total_requests": stats["requests"]["total"],
        "requests_per_second": stats["requests"]["per_second"],
        "error_rate_percent": stats["errors"]["rate_percent"],
        "avg_response_time_ms": stats["performance"]["avg_response_time_ms"],
        "p95_response_time_ms": stats["performance"]["p95_ms"],
        "cache_hit_rate_percent": stats["cache"]["hit_rate_percent"],
        "status": "healthy" if stats["errors"]["rate_percent"] < 5 else "degraded"
    }


if __name__ == "__main__":
    import uvicorn
    import io
    
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    logger.info("="*60)
    logger.info("🚀 Smart Function Recommender - Premium UI")
    logger.info("="*60)
    logger.info("✨ Server starting...")
    logger.info("🌐 Web Interface: http://localhost:8000")
    logger.info("📚 API Docs: http://localhost:8000/docs")
    logger.info("❤️  Health Check: http://localhost:8000/api/health")
    logger.info("📊 Metrics: http://localhost:8000/api/metrics")
    logger.info("📈 Stats: http://localhost:8000/api/stats")
    logger.info("💡 Tip: Visit http://localhost:8000 for the premium experience!")
    logger.info("="*60)
    
    print("\n" + "="*60)
    print("🚀 Smart Function Recommender - Premium UI")
    print("="*60)
    print("\n✨ Server starting...")
    print("🌐 Web Interface: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/api/health")
    print("📊 Metrics: http://localhost:8000/api/metrics")
    print("📈 Stats: http://localhost:8000/api/stats")
    print("\n💡 Tip: Visit http://localhost:8000 for the premium experience!")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)  # We handle logging ourselves
