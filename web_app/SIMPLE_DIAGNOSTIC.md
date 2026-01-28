# Simple Diagnostic Guide

## If NOTHING shows in console:

### Step 1: Check Console Filter
1. Open http://localhost:8000
2. Press **F12**
3. Click **Console** tab
4. Look at the top - there's a filter dropdown
5. Make sure it says **"All levels"** or **"Verbose"**
6. If it says "Errors" or "Warnings", click it and select "All levels"

### Step 2: Clear Console and Refresh
1. In Console tab, click the **trash icon** (clear console)
2. Press **Ctrl + Shift + R** (hard refresh)
3. Look for: `=== SCRIPT STARTED ===`

### Step 3: Check View Source
1. Right-click page → **View Page Source**
2. Press **Ctrl + F**
3. Search for: `=== SCRIPT STARTED ===`
   - **If FOUND**: Code is there, check console filter
   - **If NOT FOUND**: Server needs restart

### Step 4: Test Minimal Page
1. Open: `e:\Recomender\web_app\minimal_test.html` (double-click it)
2. Press **F12** → Console
3. Do you see: `MINIMAL TEST: Script is executing!`?
   - **YES**: JavaScript works, main page has issue
   - **NO**: JavaScript might be disabled

### Step 5: Check Browser Settings
- **Chrome/Edge**: Settings → Privacy → Site Settings → JavaScript → Allowed
- Try **Incognito/Private** window (disables extensions)
- Try a **different browser**

## Common Issues:

1. **Console filter set to "Errors only"** → Change to "All levels"
2. **JavaScript disabled** → Enable in browser settings
3. **Browser extension blocking scripts** → Try incognito mode
4. **Old cached page** → Hard refresh (Ctrl+Shift+R)

## What to Report:

Please tell me:
1. Do you see `=== SCRIPT STARTED ===` in View Page Source? (Yes/No)
2. What filter is selected in Console? (All levels / Errors / Warnings)
3. Does minimal_test.html work? (Yes/No)
4. Any red errors in console? (Yes/No - what do they say?)
