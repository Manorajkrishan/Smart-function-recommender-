# Production Deployment Guide

## ✅ Implemented Features

### 1. Comprehensive Logging ✅
- **Structured logging** with rotation
- **File logging** with automatic rotation (10MB files, 5 backups)
- **Console logging** for development
- **Request/response logging** with timing
- **Error logging** with stack traces
- **Log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### 2. Monitoring & Metrics ✅
- **Request tracking**: Total requests, requests per second
- **Performance metrics**: Response times (avg, P50, P95, P99, min, max)
- **Error tracking**: Error counts, error rates, recent errors
- **Cache statistics**: Hit rate, hits/misses
- **Endpoint analytics**: Requests by endpoint, errors by endpoint
- **Language analytics**: Requests by programming language
- **Uptime tracking**: Server uptime in seconds/hours

### 3. API Endpoints ✅
- `/api/health` - Basic health check
- `/api/metrics` - Comprehensive metrics (JSON)
- `/api/stats` - Simplified stats for dashboards

### 4. Production Configuration ✅
- **Gunicorn config** for multi-worker deployment
- **Docker support** with Dockerfile and docker-compose.yml
- **Environment variables** for configuration
- **CORS middleware** for cross-origin requests
- **Request middleware** for logging and metrics

## 🚀 Deployment Options

### Option 1: Gunicorn (Recommended for Production)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -c gunicorn_config.py app_new:app

# Or with custom settings
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app_new:app --bind 0.0.0.0:8000
```

### Option 2: Docker

```bash
# Build image
docker build -t smart-func-recommender .

# Run container
docker run -p 8000:8000 smart-func-recommender

# Or use docker-compose
docker-compose up -d
```

### Option 3: Deployment Scripts

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Windows:**
```cmd
deploy.bat
```

## 📊 Monitoring Endpoints

### Health Check
```bash
curl http://localhost:8000/api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Smart Function Recommender",
  "version": "2.0.0",
  "timestamp": 1234567890.123
}
```

### Metrics (Full)
```bash
curl http://localhost:8000/api/metrics
```

Response includes:
- Uptime
- Request statistics
- Error statistics
- Performance metrics
- Cache statistics
- Recent errors

### Stats (Simplified)
```bash
curl http://localhost:8000/api/stats
```

Response:
```json
{
  "uptime_hours": 24.5,
  "total_requests": 10000,
  "requests_per_second": 0.12,
  "error_rate_percent": 0.5,
  "avg_response_time_ms": 45.2,
  "p95_response_time_ms": 120.5,
  "cache_hit_rate_percent": 85.3,
  "status": "healthy"
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (or set environment variables):

```bash
# Server
BIND=0.0.0.0:8000
WORKERS=4
LOG_LEVEL=INFO

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Logging
ACCESS_LOG=logs/access.log
ERROR_LOG=logs/error.log
LOG_DIR=logs

# Database
SMART_FUNC_DB_BACKEND=sqlite
SMART_FUNC_DB_PATH=./smart_func/functions.db

# Cache
SMART_FUNC_CACHE_TTL=300
```

### Log Files

Logs are stored in the `logs/` directory:
- `app_YYYY-MM-DD.log` - Application logs (rotated)
- `access.log` - Gunicorn access logs
- `error.log` - Gunicorn error logs

## 📈 Monitoring Dashboard Integration

### Prometheus Metrics (Future)
The metrics endpoint can be easily adapted for Prometheus:

```python
# Add to app_new.py
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
```

### Grafana Dashboard
Use the `/api/stats` endpoint to create Grafana dashboards:
- Uptime graph
- Request rate graph
- Error rate graph
- Response time percentiles
- Cache hit rate

## 🔍 Log Analysis

### View Recent Logs
```bash
# Last 100 lines
tail -n 100 logs/app_$(date +%Y-%m-%d).log

# Search for errors
grep ERROR logs/app_*.log

# Count requests
grep "Request:" logs/app_*.log | wc -l
```

### Log Rotation
Logs automatically rotate when they reach 10MB. Old logs are kept as:
- `app_2024-01-26.log`
- `app_2024-01-26.log.1`
- `app_2024-01-26.log.2`
- etc. (up to 5 backups)

## ✅ Production Checklist

- [x] Structured logging with rotation
- [x] Request/response logging
- [x] Error tracking
- [x] Performance metrics
- [x] Health check endpoint
- [x] Metrics endpoint
- [x] Gunicorn configuration
- [x] Docker support
- [x] Environment variable configuration
- [x] CORS middleware
- [x] Request middleware
- [ ] Set up log aggregation (ELK, Splunk, etc.)
- [ ] Set up monitoring alerts (Prometheus, Datadog, etc.)
- [ ] Configure SSL/TLS certificates
- [ ] Set up reverse proxy (Nginx, Traefik)
- [ ] Configure auto-scaling
- [ ] Set up backup strategy

## 🎯 Success Metrics

Monitor these key metrics:
- **Uptime**: Should be > 99.9%
- **Error Rate**: Should be < 1%
- **Response Time (P95)**: Should be < 100ms
- **Cache Hit Rate**: Should be > 80%
- **Requests/Second**: Monitor for capacity planning

## 🚨 Alerting

Set up alerts for:
- Error rate > 5%
- Response time (P95) > 500ms
- Uptime < 99%
- Cache hit rate < 50%
- Disk space for logs > 80%

The system is now production-ready with comprehensive monitoring and logging! 🎉
