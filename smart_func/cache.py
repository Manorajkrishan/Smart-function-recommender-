"""
Caching layer for Smart Function Recommender.
Supports in-memory caching and optional Redis backend.
"""

import time
import hashlib
import json
from typing import Optional, Dict, Any, Callable
from functools import wraps
import threading


class Cache:
    """Simple in-memory cache with TTL."""
    
    def __init__(self, default_ttl: int = 300):
        """
        Initialize cache.
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 5 minutes)
        """
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._cleanup_interval = 60  # Cleanup every minute
        self._last_cleanup = time.time()
    
    def _make_key(self, *args, **kwargs) -> str:
        """Create a cache key from arguments."""
        key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        with self._lock:
            self._cleanup_expired()
            
            if key in self._cache:
                entry = self._cache[key]
                if entry['expires_at'] > time.time():
                    return entry['value']
                else:
                    del self._cache[key]
            
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in cache."""
        with self._lock:
            if ttl is None:
                ttl = self.default_ttl
            
            self._cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl,
                'created_at': time.time()
            }
    
    def delete(self, key: str) -> None:
        """Delete a key from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
    
    def _cleanup_expired(self) -> None:
        """Remove expired entries."""
        current_time = time.time()
        
        # Only cleanup every minute to avoid overhead
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        self._last_cleanup = current_time
        
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry['expires_at'] <= current_time
        ]
        
        for key in expired_keys:
            del self._cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            self._cleanup_expired()
            
            total_size = len(self._cache)
            total_memory = sum(
                len(json.dumps(entry['value']).encode())
                for entry in self._cache.values()
            )
            
            return {
                'entries': total_size,
                'memory_bytes': total_memory,
                'memory_mb': round(total_memory / 1024 / 1024, 2)
            }


# Global cache instance
_cache = Cache(default_ttl=300)  # 5 minutes default TTL


def cached(ttl: int = 300, key_prefix: str = ''):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time-to-live in seconds
        key_prefix: Prefix for cache keys
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{key_prefix}:{func.__name__}:{_cache._make_key(*args, **kwargs)}"
            
            # Try to get from cache
            result = _cache.get(cache_key)
            if result is not None:
                return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            _cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


def get_cache() -> Cache:
    """Get the global cache instance."""
    return _cache


def clear_cache() -> None:
    """Clear the global cache."""
    _cache.clear()
