"""
FastAPI web application for Smart Function Recommender - NEW WORKING VERSION
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

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

app = FastAPI(
    title="Smart Function Recommender",
    description="Convert natural language to reusable code snippets",
    version="1.0.0"
)


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
    """Serve the main web interface."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Function Recommender</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .content { padding: 40px; }
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex: 1;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
        }
        input[type="text"]:focus { outline: none; border-color: #667eea; }
        select {
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            background: white;
            min-width: 150px;
        }
        button {
            padding: 15px 30px;
            font-size: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        .results { margin-top: 30px; }
        .result-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .result-title {
            font-size: 1.5em;
            color: #333;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            margin: 15px 0;
            white-space: pre-wrap;
        }
        .loading { text-align: center; padding: 40px; color: #667eea; font-size: 1.2em; }
        .error { background: #fee; color: #c33; padding: 15px; border-radius: 10px; margin-top: 20px; }
        .copy-btn {
            background: #28a745;
            padding: 8px 15px;
            font-size: 0.9em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Smart Function Recommender</h1>
            <p>Convert natural language to reusable code snippets</p>
        </div>
        <div class="content">
            <div class="input-group">
                <input type="text" id="queryInput" placeholder="Describe what you need... (e.g., 'sort a list')" />
                <select id="languageSelect">
                    <option value="">All Languages</option>
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="csharp">C#</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                </select>
                <select id="topKSelect">
                    <option value="1">Top 1</option>
                    <option value="3">Top 3</option>
                    <option value="5">Top 5</option>
                </select>
                <button type="button" id="searchBtn">Search</button>
            </div>
            <div id="results" class="results"></div>
        </div>
    </div>

    <script>
        console.log('Script loaded successfully!');
        
        var searchFunction = async function() {
            console.log('Search function called');
            var query = document.getElementById('queryInput').value.trim();
            var topK = parseInt(document.getElementById('topKSelect').value);
            var language = document.getElementById('languageSelect').value;
            var resultsDiv = document.getElementById('results');
            
            if (!query) {
                resultsDiv.innerHTML = '<div class="error">Please enter a query</div>';
                return;
            }
            
            resultsDiv.innerHTML = '<div class="loading">Searching for functions...</div>';
            
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
                console.log('API response received:', data);
                displayResults(data);
            } catch (error) {
                console.error('Search error:', error);
                resultsDiv.innerHTML = '<div class="error">Error: ' + error.message + '</div>';
            }
        };
        
        function displayResults(data) {
            var resultsDiv = document.getElementById('results');
            
            if (!data || (Array.isArray(data) && data.length === 0)) {
                resultsDiv.innerHTML = '<div class="error">No functions found. Try rephrasing your query.</div>';
                return;
            }
            
            var results = Array.isArray(data) ? data : [data];
            var html = '';
            
            // Store codes for copy function
            window.functionCodes = results.map(function(func) { return func.code; });
            
            results.forEach(function(func, index) {
                var relevance = (func.relevance_score * 100).toFixed(1);
                var codeHtml = escapeHtml(func.code);
                var usageHtml = func.usage ? escapeHtml(func.usage) : '';
                
                html += '<div class="result-card">';
                html += '<div class="result-title">' + (index + 1) + '. ' + escapeHtml(func.name);
                html += ' <span style="font-size: 0.7em; color: #888;">(' + (func.language || 'python') + ')</span></div>';
                html += '<div style="color: #666; margin: 10px 0;">' + escapeHtml(func.description) + '</div>';
                html += '<div class="code-block">' + codeHtml + '</div>';
                if (usageHtml) {
                    html += '<div class="code-block" style="background: #e9ecef; color: #333;">' + usageHtml + '</div>';
                }
                html += '<div style="margin-top: 15px; color: #888; font-size: 0.9em;">';
                if (func.complexity) {
                    html += '<span style="background: #e9ecef; padding: 5px 12px; border-radius: 15px; margin-right: 10px;">Complexity: ' + escapeHtml(func.complexity) + '</span>';
                }
                if (func.popularity) {
                    html += '<span style="background: #e9ecef; padding: 5px 12px; border-radius: 15px;">Popularity: ' + func.popularity + '/10</span>';
                }
                html += '</div>';
                html += '<button class="copy-btn" onclick="copyCode(' + index + ')">Copy Code</button>';
                html += '</div>';
            });
            
            resultsDiv.innerHTML = html;
        }
        
        function escapeHtml(text) {
            if (!text) return '';
            var div = document.createElement('div');
            div.textContent = text;
            var escaped = div.innerHTML;
            // Replace newlines
            escaped = escaped.replace(/\\n/g, '<br>');
            escaped = escaped.replace(/\\r\\n/g, '<br>');
            escaped = escaped.replace(/\\r/g, '<br>');
            return escaped;
        }
        
        function copyCode(index) {
            var code = window.functionCodes && window.functionCodes[index] ? window.functionCodes[index] : '';
            if (!code) {
                alert('Error: Code not found');
                return;
            }
            
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(code).then(function() {
                    alert('Code copied to clipboard!');
                }).catch(function(err) {
                    console.error('Failed to copy:', err);
                    fallbackCopy(code);
                });
            } else {
                fallbackCopy(code);
            }
        }
        
        function fallbackCopy(text) {
            var textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                alert('Code copied to clipboard!');
            } catch (e) {
                alert('Failed to copy. Please select and copy manually.');
            }
            document.body.removeChild(textArea);
        }
        
        // Make functions globally available
        window.searchFunction = searchFunction;
        window.displayResults = displayResults;
        window.escapeHtml = escapeHtml;
        window.copyCode = copyCode;
        
        console.log('All functions initialized');
        
        // Setup event listeners
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, setting up event listeners');
            
            var searchBtn = document.getElementById('searchBtn');
            if (searchBtn) {
                searchBtn.addEventListener('click', function() {
                    console.log('Search button clicked');
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
            
            console.log('Event listeners attached');
        });
        
        // Also setup immediately if DOM already loaded
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            var searchBtn = document.getElementById('searchBtn');
            if (searchBtn) {
                searchBtn.onclick = function() {
                    console.log('Search button clicked (onclick)');
                    searchFunction();
                };
            }
        }
        
        console.log('Script initialization complete!');
    </script>
</body>
</html>"""
    
    return HTMLResponse(content=html, media_type="text/html; charset=utf-8")


@app.post("/api/search")
async def search_functions_api(request: QueryRequest):
    """Search for functions based on natural language query."""
    try:
        if request.top_k == 1:
            result = get_function(request.query, language=request.language)
            if result:
                return [result]
            return []
        else:
            results = recommend_functions(request.query, top_k=request.top_k, language=request.language)
            return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Smart Function Recommender"}


if __name__ == "__main__":
    import uvicorn
    import io
    
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    print("\n" + "="*60)
    print("Smart Function Recommender Web Interface - NEW VERSION")
    print("="*60)
    print("\nServer starting...")
    print("Web Interface: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("\nTip: If browser doesn't open automatically, visit http://localhost:8000")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
