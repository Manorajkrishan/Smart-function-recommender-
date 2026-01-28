# Troubleshooting Web Interface

## Common Issues and Solutions

### Issue 1: Browser Not Opening

**Problem**: Server starts but browser doesn't open automatically.

**Solutions**:
1. **Manually open browser**: Navigate to `http://localhost:8000`
2. **Check if server is running**: Look for "Uvicorn running on http://..." message
3. **Try different browser**: Chrome, Firefox, Edge, etc.

### Issue 2: Connection Refused / Can't Connect

**Problem**: Browser shows "This site can't be reached" or connection error.

**Solutions**:
1. **Check server is running**: Make sure you see "Uvicorn running on..."
2. **Use correct URL**: 
   - ✅ `http://localhost:8000`
   - ✅ `http://127.0.0.1:8000`
   - ❌ `http://0.0.0.0:8000` (won't work in browser)
3. **Check firewall**: Windows Firewall might be blocking the connection
4. **Check port**: Make sure port 8000 is not used by another application

### Issue 3: Import Errors

**Problem**: Server crashes with "ModuleNotFoundError: No module named 'smart_func'"

**Solutions**:
1. **Install the package**: 
   ```bash
   cd e:\Recomender
   pip install -e .
   ```
2. **Run from project root**: Make sure you're in the correct directory
3. **Check Python path**: The app should automatically add the parent directory

### Issue 4: Port Already in Use

**Problem**: Error "Address already in use" or port 8000 is busy.

**Solutions**:
1. **Find and kill the process**:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```
2. **Use a different port**: Edit `web_app/app.py` and change port 8000 to 8080

### Issue 5: Page Loads But Shows Error

**Problem**: Page opens but shows error message or blank page.

**Solutions**:
1. **Check browser console**: Press F12 and check for JavaScript errors
2. **Check server logs**: Look for error messages in the terminal
3. **Test API directly**: Visit `http://localhost:8000/api/health`

## Quick Diagnostic Steps

### Step 1: Verify Server is Running
```bash
# In the terminal where you ran python app.py, you should see:
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 2: Test API Endpoint
Open browser and go to: `http://localhost:8000/api/health`

You should see:
```json
{"status": "healthy", "service": "Smart Function Recommender"}
```

### Step 3: Test Main Page
Open browser and go to: `http://localhost:8000`

You should see the web interface with search box.

### Step 4: Check Browser Console
1. Open browser (F12 or Right-click → Inspect)
2. Go to Console tab
3. Look for any red error messages

## Manual Testing

### Test with curl (if available)
```bash
# Health check
curl http://localhost:8000/api/health

# Search API
curl -X POST "http://localhost:8000/api/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "sort list", "top_k": 1}'
```

### Test with Python requests
```python
import requests

# Health check
response = requests.get('http://localhost:8000/api/health')
print(response.json())

# Search
response = requests.post('http://localhost:8000/api/search', 
                        json={'query': 'sort list', 'top_k': 1})
print(response.json())
```

## Still Not Working?

1. **Check server logs** for specific error messages
2. **Try restarting** the server (CTRL+C, then run again)
3. **Check Python version**: Requires Python 3.7+
4. **Reinstall dependencies**: 
   ```bash
   pip install --upgrade fastapi uvicorn pydantic
   ```

## Alternative: Use CLI Instead

If web interface doesn't work, you can always use the CLI:

```bash
smart-func "your query here"
```

Or use as a Python library:
```python
from smart_func import get_function
result = get_function("your query")
print(result['code'])
```
