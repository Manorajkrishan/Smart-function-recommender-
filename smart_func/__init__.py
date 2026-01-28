"""
Smart Function Recommender for Developers

A tool that converts natural language descriptions of programming tasks
into reusable code snippets or functions.
"""

from smart_func.generator import get_function, recommend_functions
from smart_func.nlp import parse_intent, extract_keywords

__version__ = "0.1.0"
__all__ = ["get_function", "recommend_functions", "parse_intent", "extract_keywords"]
