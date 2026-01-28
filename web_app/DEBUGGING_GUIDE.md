# Debugging Guide - Search Button Not Working

## Quick Checks

### 1. Check Browser Console (F12)
Open browser console and look for:
- ✅ "Search button event listener attached" - Event listener is working
- ✅ "searchFunction called" - Function is being called
- ✅ "Query: ..." - Query is being processed
- ✅ "API response received: ..." - API call succeeded
- ❌ Any red error messages

### 2. Test API Directly
Open browser and go to: http://localhost:8000/api/health
Should show: `{"status":"healthy","service":"Smart Function Recommender"}`

### 3. Check Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Click Search button
4. Look for `/api/search` request
5. Check if it's:
   - ✅ 200 (Success) - API is working
   - ❌ 404/500 (Error) - Check error details

## Common Issues

### Issue: No console messages at all
**Problem**: JavaScript not loading or syntax error preventing execution

**Solution**:
1. Hard refresh: Ctrl+Shift+R
2. Check console for syntax errors
3. Verify server is running

### Issue: "searchFunction is not defined"
**Problem**: Function not available when button is clicked

**Solution**:
1. Check if `window.searchFunction` exists in console: `typeof window.searchFunction`
2. Should return "function"
3. If not, hard refresh the page

### Issue: API returns error
**Problem**: Backend issue

**Solution**:
1. Check server logs in terminal
2. Test API directly: `curl -X POST http://localhost:8000/api/search -H "Content-Type: application/json" -d '{"query":"test","top_k":1}'`
3. Check if smart_func module is imported correctly

### Issue: Button click does nothing
**Problem**: Event listener not attached

**Solution**:
1. Check console for "Search button event listener attached"
2. If missing, check for JavaScript errors
3. Try inline onclick handler (already added as fallback)

## Manual Test in Browser Console

Open browser console (F12) and run:

```javascript
// Check if function exists
typeof window.searchFunction

// Check if button exists
document.getElementById('searchBtn')

// Manually call the function
searchFunction()

// Check if API works
fetch('/api/search', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query: 'sort list', top_k: 1})
}).then(r => r.json()).then(console.log)
```

## Expected Behavior

1. **Page Load**: Console shows "Search button event listener attached"
2. **Button Click**: Console shows "searchFunction called"
3. **Query Processing**: Console shows "Query: ..."
4. **API Call**: Network tab shows POST to /api/search
5. **Results Display**: Page shows function results

If any step fails, check the error message and report it.
