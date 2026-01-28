# Quick Fix: Web Interface Not Opening

## ✅ Server is Running!

The server is running on port 8000. Here's how to access it:

### Step 1: Open Your Browser

**Manually open your web browser** and navigate to:

```
http://localhost:8000
```

OR

```
http://127.0.0.1:8000
```

### Step 2: If Browser Doesn't Open Automatically

The server should automatically open your browser, but if it doesn't:

1. **Open any web browser** (Chrome, Firefox, Edge, etc.)
2. **Type in the address bar**: `localhost:8000`
3. **Press Enter**

### Step 3: Verify Server is Running

Check the terminal where you ran `python app.py`. You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

If you see this, the server IS running and ready!

### Common Issues

#### Issue: "This site can't be reached"
- **Solution**: Make sure the server is actually running
- Check the terminal for the "Uvicorn running" message
- Try restarting: Press CTRL+C, then run `python app.py` again

#### Issue: Port Already in Use
- **Solution**: Kill existing processes:
  ```powershell
  Get-Process -Name python | Where-Object {$_.Id -eq <PID>} | Stop-Process -Force
  ```

#### Issue: Browser Opens But Shows Error
- **Solution**: Check browser console (F12) for errors
- Try the API directly: http://localhost:8000/api/health

### Test the API Directly

Open these URLs in your browser to test:

1. **Health Check**: http://localhost:8000/api/health
   - Should show: `{"status":"healthy","service":"Smart Function Recommender"}`

2. **API Docs**: http://localhost:8000/docs
   - Should show interactive API documentation

3. **Main Interface**: http://localhost:8000
   - Should show the search interface

### Still Not Working?

1. **Check firewall**: Windows Firewall might be blocking port 8000
2. **Try different port**: Edit `web_app/app.py` and change `port=8000` to `port=8080`
3. **Check browser**: Try a different browser
4. **Check terminal**: Look for error messages in the server output

### Alternative: Use CLI

If web interface doesn't work, use the CLI:

```bash
smart-func "your query here"
```

---

**The server is running - just open http://localhost:8000 in your browser!** 🌐
