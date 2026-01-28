"""
Core function recommender logic.
"""

import os
from typing import List, Dict, Optional, Tuple
from smart_func.nlp import parse_intent, calculate_relevance_score
from smart_func.database import get_backend
from smart_func.cache import cached, get_cache

# Get database backend (auto-detects JSON or SQLite)
_db_backend = None

def get_database_backend():
    """Get the database backend instance."""
    global _db_backend
    if _db_backend is None:
        _db_backend = get_backend('auto')
    return _db_backend

def load_database() -> List[Dict]:
    """
    Load the function database (from JSON or SQLite).
    
    Returns:
        List of function dictionaries
    """
    backend = get_database_backend()
    return backend.get_functions()


@cached(ttl=300, key_prefix='search')
@cached(ttl=300, key_prefix='search')
def search_functions(query: str, database: Optional[List[Dict]] = None, top_k: int = 5, language: Optional[str] = None) -> List[Dict]:
    """
    Search for relevant functions based on user query.
    Results are cached for 5 minutes.
    
    Args:
        query: Natural language description of the task
        database: Optional database to search (defaults to loading from file)
        top_k: Number of top results to return
        language: Optional language filter (e.g., 'python', 'javascript', 'java', 'csharp', 'go', 'rust')
        
    Returns:
        List of function dictionaries with relevance scores, sorted by relevance
    """
    if database is None:
        database = load_database()
    
    # Filter by language if specified
    if language:
        language = language.lower()
        database = [func for func in database if func.get('language', 'python').lower() == language]
    
    # Parse user intent
    intent = parse_intent(query)
    
    # If language detected in query, filter database first
    detected_lang = intent.get('detected_language')
    if detected_lang:
        database = [func for func in database if func.get('language', 'python').lower() == detected_lang]
    
    # Calculate relevance scores for all functions
    scored_functions = []
    for func in database:
        score = calculate_relevance_score(intent, func)
        scored_functions.append({
            **func,
            'relevance_score': score
        })
    
    # Sort by relevance score (descending), then by popularity (descending)
    # But for very close scores, apply tie-breaking logic
    def sort_key(func):
        score = func['relevance_score']
        popularity = func.get('popularity', 0)
        
        # Special tie-breaking for sort_unique functions when scores are close
        # Check if query has hints for descending order
        query_lower = query.lower()
        desc_hints = ['rank', 'top', 'best', 'highest', 'largest', 'biggest']
        has_desc_hint = any(hint in query_lower for hint in desc_hints)
        
        if func.get('id') == 'sort_desc_unique' and has_desc_hint:
            # Small boost for descending when hints present
            score += 0.02
        elif func.get('id') == 'sort_asc_unique' and has_desc_hint:
            # Small penalty for ascending when descending hints present
            score -= 0.02
        
        return (score, popularity)
    
    scored_functions.sort(key=sort_key, reverse=True)
    
    # Return top k results
    return scored_functions[:top_k]


def get_function(query: str, top_k: int = 1, min_relevance: float = 0.0, language: Optional[str] = None) -> Optional[Dict]:
    """
    Get the most relevant function for a given query.
    
    Args:
        query: Natural language description of the task
        top_k: Number of results to return (default: 1 for single result)
        min_relevance: Minimum relevance score threshold (default: 0.0, no threshold)
        language: Optional language filter (e.g., 'python', 'javascript', 'java', 'csharp', 'go', 'rust')
        
    Returns:
        Dictionary containing function code and metadata, or None if no match
    """
    results = search_functions(query, top_k=top_k, language=language)
    
    if not results:
        return None
    
    # Filter by minimum relevance if specified
    if min_relevance > 0:
        results = [r for r in results if r.get('relevance_score', 0) >= min_relevance]
        if not results:
            return None
    
    if top_k == 1:
        return results[0]
    
    return results


def recommend_functions(query: str, top_k: int = 5, language: Optional[str] = None) -> List[Dict]:
    """
    Get multiple function recommendations for a given query.
    
    Args:
        query: Natural language description of the task
        top_k: Number of recommendations to return
        language: Optional language filter (e.g., 'python', 'javascript', 'java', 'csharp', 'go', 'rust')
        
    Returns:
        List of function dictionaries with relevance scores
    """
    return search_functions(query, top_k=top_k, language=language)


def format_recommendation(func: Dict, include_metadata: bool = True) -> str:
    """
    Format a function recommendation for display.
    
    Args:
        func: Function dictionary from database
        include_metadata: Whether to include metadata (usage, complexity, etc.)
        
    Returns:
        Formatted string representation
    """
    output = []
    
    # Function code
    output.append("=" * 60)
    output.append(f"Function: {func.get('name', 'Unknown')}")
    output.append("=" * 60)
    output.append("")
    output.append(func.get('code', ''))
    output.append("")
    
    if include_metadata:
        # Description
        if func.get('description'):
            output.append(f"Description: {func['description']}")
            output.append("")
        
        # Usage example
        if func.get('usage'):
            output.append("Usage Example:")
            output.append(func['usage'])
            output.append("")
        
        # Metadata
        metadata_parts = []
        if func.get('complexity'):
            metadata_parts.append(f"Complexity: {func['complexity']}")
        if func.get('relevance_score') is not None:
            metadata_parts.append(f"Relevance: {func['relevance_score']:.2%}")
        if func.get('popularity'):
            metadata_parts.append(f"Popularity: {func['popularity']}/10")
        
        if metadata_parts:
            output.append(" | ".join(metadata_parts))
            output.append("")
    
    return "\n".join(output)
