"""
Monitoring and Metrics Collection for Smart Function Recommender
"""

import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class MetricsCollector:
    """Collects and aggregates application metrics."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self._request_count = 0
        self._error_count = 0
        self._total_response_time = 0.0
        self._response_times = deque(maxlen=1000)  # Keep last 1000 response times
        self._requests_by_endpoint = defaultdict(int)
        self._errors_by_endpoint = defaultdict(int)
        self._requests_by_language = defaultdict(int)
        self._cache_hits = 0
        self._cache_misses = 0
        self._start_time = time.time()
        self._recent_errors = deque(maxlen=100)  # Keep last 100 errors
        
    def record_request(self, endpoint: str, response_time: float, language: Optional[str] = None):
        """Record a successful request."""
        with self._lock:
            self._request_count += 1
            self._total_response_time += response_time
            self._response_times.append(response_time)
            self._requests_by_endpoint[endpoint] += 1
            if language:
                self._requests_by_language[language] += 1
    
    def record_error(self, endpoint: str, error_type: str, error_message: str):
        """Record an error."""
        with self._lock:
            self._error_count += 1
            self._errors_by_endpoint[endpoint] += 1
            self._recent_errors.append({
                'timestamp': datetime.utcnow().isoformat(),
                'endpoint': endpoint,
                'error_type': error_type,
                'message': error_message
            })
    
    def record_cache_hit(self):
        """Record a cache hit."""
        with self._lock:
            self._cache_hits += 1
    
    def record_cache_miss(self):
        """Record a cache miss."""
        with self._lock:
            self._cache_misses += 1
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics."""
        with self._lock:
            uptime_seconds = time.time() - self._start_time
            uptime_hours = uptime_seconds / 3600
            
            response_times_list = list(self._response_times)
            avg_response_time = self._total_response_time / max(self._request_count, 1)
            
            # Calculate percentiles
            if response_times_list:
                sorted_times = sorted(response_times_list)
                p50 = sorted_times[int(len(sorted_times) * 0.5)]
                p95 = sorted_times[int(len(sorted_times) * 0.95)]
                p99 = sorted_times[int(len(sorted_times) * 0.99)]
                min_time = min(sorted_times)
                max_time = max(sorted_times)
            else:
                p50 = p95 = p99 = min_time = max_time = 0.0
            
            total_cache_requests = self._cache_hits + self._cache_misses
            cache_hit_rate = (self._cache_hits / max(total_cache_requests, 1)) * 100
            
            requests_per_second = self._request_count / max(uptime_seconds, 1)
            error_rate = (self._error_count / max(self._request_count, 1)) * 100
            
            return {
                'uptime': {
                    'seconds': uptime_seconds,
                    'hours': uptime_hours,
                    'formatted': str(timedelta(seconds=int(uptime_seconds)))
                },
                'requests': {
                    'total': self._request_count,
                    'per_second': round(requests_per_second, 2),
                    'by_endpoint': dict(self._requests_by_endpoint),
                    'by_language': dict(self._requests_by_language)
                },
                'errors': {
                    'total': self._error_count,
                    'rate_percent': round(error_rate, 2),
                    'by_endpoint': dict(self._errors_by_endpoint),
                    'recent': list(self._recent_errors)[-10]  # Last 10 errors
                },
                'performance': {
                    'avg_response_time_ms': round(avg_response_time * 1000, 2),
                    'p50_ms': round(p50 * 1000, 2),
                    'p95_ms': round(p95 * 1000, 2),
                    'p99_ms': round(p99 * 1000, 2),
                    'min_ms': round(min_time * 1000, 2),
                    'max_ms': round(max_time * 1000, 2)
                },
                'cache': {
                    'hits': self._cache_hits,
                    'misses': self._cache_misses,
                    'hit_rate_percent': round(cache_hit_rate, 2),
                    'total_requests': total_cache_requests
                },
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def reset(self):
        """Reset all metrics (use with caution)."""
        with self._lock:
            self._request_count = 0
            self._error_count = 0
            self._total_response_time = 0.0
            self._response_times.clear()
            self._requests_by_endpoint.clear()
            self._errors_by_endpoint.clear()
            self._requests_by_language.clear()
            self._cache_hits = 0
            self._cache_misses = 0
            self._recent_errors.clear()
            self._start_time = time.time()


# Global metrics collector instance
_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return _metrics
