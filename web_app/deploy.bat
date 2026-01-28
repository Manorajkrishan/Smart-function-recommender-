@echo off
REM Production deployment script for Windows

echo 🚀 Starting production deployment...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

REM Create logs directory
if not exist "logs" mkdir logs

REM Migrate to SQLite if needed
if exist "..\smart_func\database.json" (
    if not exist "..\smart_func\functions.db" (
        echo 🔄 Migrating to SQLite database...
        python ..\smart_func\migrate_to_db.py
    )
)

REM Set environment variables
set LOG_LEVEL=%LOG_LEVEL%
if "%LOG_LEVEL%"=="" set LOG_LEVEL=INFO

set WORKERS=%WORKERS%
if "%WORKERS%"=="" set WORKERS=4

set BIND=%BIND%
if "%BIND%"=="" set BIND=0.0.0.0:8000

REM Start Gunicorn
echo ✅ Starting Gunicorn server...
echo    Workers: %WORKERS%
echo    Bind: %BIND%
echo    Log Level: %LOG_LEVEL%
echo.
echo 🌐 Server will be available at http://%BIND%
echo 📊 Metrics: http://%BIND%/api/metrics
echo ❤️  Health: http://%BIND%/api/health
echo.

gunicorn -c gunicorn_config.py app_new:app
