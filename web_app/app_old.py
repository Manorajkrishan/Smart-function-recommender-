"""
FastAPI web application for Smart Function Recommender.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
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
    print(f"Current directory: {current_dir}")
    print(f"Parent directory: {parent_dir}")
    print(f"Python path: {sys.path[:3]}")
    raise

app = FastAPI(
    title="Smart Function Recommender",
    description="Convert natural language to reusable code snippets",
    version="0.1.0"
)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 1
    language: Optional[str] = None


class FunctionResponse(BaseModel):
    id: str
    name: str
    code: str
    description: str
    relevance_score: float
    usage: Optional[str] = None
    complexity: Optional[str] = None
    popularity: Optional[int] = None


@app.get("/favicon.ico")
async def favicon():
    """Serve favicon to avoid 404 errors."""
    return JSONResponse(content={}, status_code=204)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface."""
    try:
        html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Function Recommender</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            .content {
                padding: 40px;
            }
            .input-section {
                margin-bottom: 30px;
            }
            .input-group {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }
            input[type="text"] {
                flex: 1;
                padding: 15px 20px;
                font-size: 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
            }
            select {
                padding: 15px 20px;
                font-size: 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                background: white;
                cursor: pointer;
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
                transition: transform 0.2s, box-shadow 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            button:active {
                transform: translateY(0);
            }
            .results {
                margin-top: 30px;
            }
            .result-card {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 20px;
                border-left: 4px solid #667eea;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .result-card:hover {
                transform: translateX(5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .result-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }
            .result-title {
                font-size: 1.5em;
                color: #333;
                font-weight: bold;
            }
            .relevance-badge {
                background: #667eea;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
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
            }
            .description {
                color: #666;
                margin: 10px 0;
                font-size: 1.1em;
            }
            .metadata {
                display: flex;
                gap: 20px;
                margin-top: 15px;
                font-size: 0.9em;
                color: #888;
            }
            .metadata span {
                background: #e9ecef;
                padding: 5px 12px;
                border-radius: 15px;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #667eea;
                font-size: 1.2em;
            }
            .error {
                background: #fee;
                color: #c33;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
            }
            .copy-btn {
                background: #28a745;
                padding: 8px 15px;
                font-size: 0.9em;
                margin-top: 10px;
            }
            .examples {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
            }
            .examples h3 {
                margin-bottom: 15px;
                color: #333;
            }
            .example-btn {
                display: inline-block;
                margin: 5px;
                padding: 8px 15px;
                background: white;
                color: #667eea;
                border: 2px solid #667eea;
                border-radius: 20px;
                cursor: pointer;
                font-size: 0.9em;
                transition: all 0.2s;
            }
            .example-btn:hover {
                background: #667eea;
                color: white;
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
                <div class="input-section">
                    <div class="input-group">
                        <input type="text" id="queryInput" placeholder="Describe what you need... (e.g., 'sort a list in descending order and remove duplicates')" />
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
                </div>
                
                <div class="examples">
                    <h3>Try these examples:</h3>
                    <button class="example-btn" data-query="sort a list in descending order and remove duplicates">Sort & Remove Duplicates</button>
                    <button class="example-btn" data-query="merge two dictionaries">Merge Dictionaries</button>
                    <button class="example-btn" data-query="find the upper case">Find Uppercase</button>
                    <button class="example-btn" data-query="calculate the minimum">Find Minimum</button>
                    <button class="example-btn" data-query="reverse a string">Reverse String</button>
                    <button class="example-btn" data-query="count words in text">Count Words</button>
                </div>
                
                <div id="results" class="results"></div>
            </div>
        </div>
        
        <script>
            // CRITICAL: First thing - verify script is executing
            console.log('=== SCRIPT STARTED ===');
            console.log('JavaScript is executing!');
            
            // CRITICAL: Define functions FIRST and assign to window IMMEDIATELY
            // This ensures functions are available even if there are errors later
            
            // Declare functions
            var searchFunction, displayResults, escapeHtml, copyToClipboard, setExample;
            console.log('Variables declared');
            
            // Define searchFunction
            console.log('Defining searchFunction...');
            searchFunction = async function() {
                console.log('searchFunction called');
                const query = document.getElementById('queryInput').value.trim();
                const topK = parseInt(document.getElementById('topKSelect').value);
                const language = document.getElementById('languageSelect').value;
                const resultsDiv = document.getElementById('results');
                
                console.log('Query:', query, 'TopK:', topK, 'Language:', language);
                
                if (!query) {
                    resultsDiv.innerHTML = '<div class="error">Please enter a query</div>';
                    return;
                }
                
                resultsDiv.innerHTML = '<div class="loading">Searching for functions...</div>';
                
                try {
                    const requestBody = { query: query, top_k: topK };
                    if (language) {
                        requestBody.language = language;
                    }
                    
                    const response = await fetch('/api/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(requestBody)
                    });
                    
                    if (!response.ok) {
                        throw new Error('Search failed');
                    }
                    
                    const data = await response.json();
                    console.log('API response received:', data);
                    displayResults(data);
                } catch (error) {
                    console.error('Search error:', error);
                    resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                }
            };
            
            displayResults = function(data) {
                const resultsDiv = document.getElementById('results');
                
                if (!data || (Array.isArray(data) && data.length === 0)) {
                    resultsDiv.innerHTML = '<div class="error">No functions found. Try rephrasing your query.</div>';
                    return;
                }
                
                const results = Array.isArray(data) ? data : [data];
                let html = '';
                
                // Store code in a global array for copy function
                if (!window.functionCodes) {
                    window.functionCodes = [];
                }
                window.functionCodes = results.map(func => func.code);
                
                results.forEach((func, index) => {
                    const relevance = (func.relevance_score * 100).toFixed(1);
                    html += `
                        <div class="result-card">
                            <div class="result-header">
                                <div class="result-title">${index + 1}. ${func.name} <span style="font-size: 0.7em; color: #888; font-weight: normal;">(${func.language || 'python'})</span></div>
                                <div class="relevance-badge">${relevance}% Match</div>
                            </div>
                            <div class="description">${escapeHtml(func.description)}</div>
                            <div class="code-block">${escapeHtml(func.code)}</div>
                            ${func.usage ? `<div class="code-block" style="background: #e9ecef; color: #333;">${escapeHtml(func.usage)}</div>` : ''}
                            <div class="metadata">
                                ${func.complexity ? `<span>Complexity: ${func.complexity}</span>` : ''}
                                ${func.popularity ? `<span>Popularity: ${func.popularity}/10</span>` : ''}
                            </div>
                            <button class="copy-btn" onclick="copyToClipboard(${index})">Copy Code</button>
                        </div>
                    `;
                });
                
                resultsDiv.innerHTML = html;
            };
            
            escapeHtml = function(text) {
                if (!text) return '';
                const div = document.createElement('div');
                div.textContent = text;
                let escaped = div.innerHTML;
                // Replace newlines with <br> tags - use simple string replacement
                while (escaped.indexOf('\n') !== -1) {
                    escaped = escaped.replace('\n', '<br>');
                }
                while (escaped.indexOf('\r\n') !== -1) {
                    escaped = escaped.replace('\r\n', '<br>');
                }
                while (escaped.indexOf('\r') !== -1) {
                    escaped = escaped.replace('\r', '<br>');
                }
                return escaped;
            };
            
            copyToClipboard = function(index) {
                // Get code from stored array
                const codeToCopy = window.functionCodes && window.functionCodes[index] ? window.functionCodes[index] : '';
                
                if (!codeToCopy) {
                    console.error('Code not found for index:', index);
                    alert('Error: Code not found');
                    return;
                }
                
                navigator.clipboard.writeText(codeToCopy).then(() => {
                    alert('Code copied to clipboard!');
                }).catch(err => {
                    console.error('Failed to copy:', err);
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = codeToCopy;
                    document.body.appendChild(textArea);
                    textArea.select();
                    try {
                        document.execCommand('copy');
                        alert('Code copied to clipboard!');
                    } catch (e) {
                        alert('Failed to copy. Please select and copy manually.');
                    }
                    document.body.removeChild(textArea);
                });
            };
            
            setExample = function(query) {
                if (document.getElementById('queryInput')) {
                    document.getElementById('queryInput').value = query;
                    if (typeof window.searchFunction === 'function') {
                        window.searchFunction();
                    } else if (typeof searchFunction === 'function') {
                        searchFunction();
                    }
                }
            };
            
            // CRITICAL: Assign to window IMMEDIATELY after each function is defined
            // Do this RIGHT AFTER each function definition to ensure availability
            console.log('Assigning functions to window...');
            try {
                window.searchFunction = searchFunction;
                window.setExample = setExample;
                window.displayResults = displayResults;
                window.escapeHtml = escapeHtml;
                window.copyToClipboard = copyToClipboard;
                
                console.log('Functions assigned to window object');
                
                // Verify assignment worked
                if (typeof window.searchFunction !== 'function') {
                    console.error('CRITICAL: Failed to assign searchFunction to window');
                    console.error('Type:', typeof window.searchFunction);
                    console.error('Value:', window.searchFunction);
                } else {
                    console.log('SUCCESS: Function assigned to window successfully');
                    console.log('searchFunction type:', typeof window.searchFunction);
                }
            } catch (e) {
                console.error('ERROR: Error assigning functions to window:', e);
                console.error('Error details:', e.message, e.stack);
            }
            
            // Debug: Log that functions are available
            console.log('=== SMART FUNCTION RECOMMENDER INITIALIZED ===');
            console.log('Functions initialized:', {
                searchFunction: typeof window.searchFunction,
                displayResults: typeof window.displayResults,
                escapeHtml: typeof window.escapeHtml,
                copyToClipboard: typeof window.copyToClipboard
            });
            console.log('All initialization complete!');
            
            // Immediate test - verify functions are available
            if (typeof window.searchFunction !== 'function') {
                console.error('ERROR: searchFunction is not a function!');
                console.error('searchFunction type:', typeof window.searchFunction);
                console.error('searchFunction value:', window.searchFunction);
                console.error('This is a critical error. Please refresh the page.');
            } else {
                console.log('SUCCESS: searchFunction is available and ready');
                console.log('Function test:', window.searchFunction.toString().substring(0, 50) + '...');
            }
            
            // Create a safe wrapper function that always works
            // This is a fallback that will work even if main assignment fails
            try {
                window.safeSearchFunction = function() {
                    console.log('safeSearchFunction called');
                    if (typeof window.searchFunction === 'function') {
                        return window.searchFunction();
                    } else if (typeof searchFunction === 'function') {
                        return searchFunction();
                    } else {
                        console.error('CRITICAL: searchFunction is not available');
                        console.error('window.searchFunction:', window.searchFunction);
                        console.error('searchFunction:', searchFunction);
                        alert('Error: Search function not loaded. Please refresh the page (Ctrl+Shift+R).');
                    }
                };
                console.log('safeSearchFunction created successfully');
            } catch (e) {
                console.error('Failed to create safeSearchFunction:', e);
            }
            
            // Initialize event listeners when DOM is ready
            function initializeEventListeners() {
                console.log('Initializing event listeners...');
                
                // Search button - use direct function reference
                const searchBtn = document.getElementById('searchBtn');
                if (searchBtn) {
                    // Remove any existing listeners
                    searchBtn.onclick = null;
                    
                    // Add new click handler - use safe wrapper
                    searchBtn.onclick = function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        console.log('Search button clicked via onclick handler');
                        console.log('Checking function availability...');
                        console.log('window.searchFunction type:', typeof window.searchFunction);
                        console.log('searchFunction type:', typeof searchFunction);
                        console.log('window.safeSearchFunction type:', typeof window.safeSearchFunction);
                        
                        // Try multiple ways to call the function
                        if (typeof window.safeSearchFunction === 'function') {
                            console.log('Using safeSearchFunction');
                            window.safeSearchFunction();
                        } else if (typeof window.searchFunction === 'function') {
                            console.log('Using window.searchFunction');
                            window.searchFunction();
                        } else if (typeof searchFunction === 'function') {
                            console.log('Using searchFunction');
                            searchFunction();
                        } else {
                            console.error('CRITICAL: All function checks failed');
                            console.error('window.searchFunction:', window.searchFunction);
                            console.error('searchFunction:', searchFunction);
                            alert('Error: Search function not loaded. Please refresh the page (Ctrl+Shift+R).');
                        }
                    };
                    
                    // Also add event listener as backup
                    searchBtn.addEventListener('click', function(e) {
                        console.log('Search button clicked via addEventListener');
                        if (typeof window.safeSearchFunction === 'function') {
                            window.safeSearchFunction();
                        } else if (typeof window.searchFunction === 'function') {
                            window.searchFunction();
                        } else {
                            console.error('Function not available in addEventListener');
                        }
                    });
                    
                    console.log('Search button handlers attached successfully');
                } else {
                    console.error('ERROR: Search button not found!');
                }
                
                // Enter key in input
                const queryInput = document.getElementById('queryInput');
                if (queryInput) {
                    queryInput.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            if (typeof searchFunction === 'function') {
                                searchFunction();
                            }
                        }
                    });
                }
                
                // Example buttons
                const exampleBtns = document.querySelectorAll('.example-btn');
                exampleBtns.forEach(function(btn) {
                    btn.addEventListener('click', function() {
                        const query = this.getAttribute('data-query');
                        if (query) {
                            document.getElementById('queryInput').value = query;
                            if (typeof searchFunction === 'function') {
                                searchFunction();
                            }
                        }
                    });
                });
                
                console.log('All event listeners initialized');
            }
            
            // Initialize when DOM is ready
            console.log('Setting up DOM ready handler...');
            console.log('Document readyState:', document.readyState);
            
            if (document.readyState === 'loading') {
                console.log('Document still loading, waiting for DOMContentLoaded...');
                document.addEventListener('DOMContentLoaded', function() {
                    console.log('DOMContentLoaded fired!');
                    initializeEventListeners();
                });
            } else {
                // DOM already loaded
                console.log('DOM already loaded, initializing immediately...');
                initializeEventListeners();
            }
            
            console.log('=== SCRIPT END ===');
            console.log('If you see this message, JavaScript is working!');
        </script>
    </body>
    </html>
    """
        # Ensure proper encoding
        return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)


@app.post("/api/search", response_model=List[FunctionResponse])
async def search_functions_api(request: QueryRequest):
    """API endpoint to search for functions."""
    try:
        if request.top_k == 1:
            result = get_function(request.query, top_k=1, language=request.language)
            if result is None:
                raise HTTPException(status_code=404, detail="No matching function found")
            return [FunctionResponse(**result)]
        else:
            results = recommend_functions(request.query, top_k=request.top_k, language=request.language)
            if not results:
                raise HTTPException(status_code=404, detail="No matching functions found")
            return [FunctionResponse(**func) for func in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Smart Function Recommender"}


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time
    
    def open_browser():
        time.sleep(1.5)  # Wait for server to start
        webbrowser.open('http://localhost:8000')
    
    # Open browser automatically
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Set UTF-8 encoding for Windows console
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    print("\n" + "="*60)
    print("Smart Function Recommender Web Interface")
    print("="*60)
    print("\nServer starting...")
    print("Web Interface: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("\nTip: If browser doesn't open automatically, visit http://localhost:8000")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
