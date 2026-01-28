#!/bin/bash
# Production deployment script for Smart Function Recommender

set -e

echo "🚀 Starting production deployment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create logs directory
mkdir -p logs

# Migrate to SQLite if needed
if [ -f "../smart_func/database.json" ] && [ ! -f "../smart_func/functions.db" ]; then
    echo "🔄 Migrating to SQLite database..."
    python ../smart_func/migrate_to_db.py
fi

# Set environment variables
export LOG_LEVEL=${LOG_LEVEL:-INFO}
export WORKERS=${WORKERS:-4}
export BIND=${BIND:-0.0.0.0:8000}

# Start Gunicorn
echo "✅ Starting Gunicorn server..."
echo "   Workers: $WORKERS"
echo "   Bind: $BIND"
echo "   Log Level: $LOG_LEVEL"
echo ""
echo "🌐 Server will be available at http://$BIND"
echo "📊 Metrics: http://$BIND/api/metrics"
echo "❤️  Health: http://$BIND/api/health"
echo ""

exec gunicorn -c gunicorn_config.py app_new:app
