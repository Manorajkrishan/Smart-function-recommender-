"""
Tests for the function generator module.
"""

import unittest
from smart_func.generator import (
    get_function,
    recommend_functions,
    search_functions,
    format_recommendation,
    load_database
)
from smart_func.nlp import parse_intent, extract_keywords, calculate_relevance_score


class TestNLP(unittest.TestCase):
    """Test NLP parsing functionality."""
    
    def test_extract_keywords(self):
        """Test keyword extraction."""
        text = "Sort a list of numbers in descending order"
        keywords = extract_keywords(text)
        self.assertIn("sort", keywords)
        self.assertIn("list", keywords)
        self.assertIn("numbers", keywords)
        self.assertIn("descending", keywords)
        self.assertNotIn("a", keywords)  # Stop word should be filtered
        self.assertNotIn("of", keywords)  # Stop word should be filtered
    
    def test_parse_intent(self):
        """Test intent parsing."""
        text = "Sort a list of numbers in descending order and remove duplicates"
        intent = parse_intent(text)
        
        self.assertEqual(intent['action'], 'sort')
        self.assertEqual(intent['data_type'], 'list')
        self.assertEqual(intent['order'], 'descending')
        self.assertIsInstance(intent['keywords'], list)
        self.assertGreater(len(intent['keywords']), 0)
    
    def test_parse_intent_merge(self):
        """Test parsing merge intent."""
        text = "merge two dictionaries"
        intent = parse_intent(text)
        self.assertEqual(intent['action'], 'merge')
        self.assertEqual(intent['data_type'], 'dictionary')


class TestGenerator(unittest.TestCase):
    """Test function generator functionality."""
    
    def test_load_database(self):
        """Test database loading."""
        database = load_database()
        self.assertIsInstance(database, list)
        self.assertGreater(len(database), 0)
        
        # Check structure of first function
        func = database[0]
        self.assertIn('id', func)
        self.assertIn('name', func)
        self.assertIn('code', func)
        self.assertIn('description', func)
    
    def test_get_function(self):
        """Test getting a single function."""
        result = get_function("sort a list in descending order and remove duplicates")
        
        self.assertIsNotNone(result)
        self.assertIn('code', result)
        self.assertIn('name', result)
        self.assertIn('relevance_score', result)
        self.assertGreater(result['relevance_score'], 0)
    
    def test_get_function_no_match(self):
        """Test getting function with no match."""
        # Very unlikely query
        result = get_function("quantum computing neural network optimization")
        # Should return something (even if low relevance) or None
        # The current implementation should return the best match even if low score
        self.assertIsNotNone(result)  # Should return best available match
    
    def test_recommend_functions(self):
        """Test getting multiple recommendations."""
        results = recommend_functions("sort list", top_k=3)
        
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 3)
        self.assertGreater(len(results), 0)
        
        # Check that results are sorted by relevance
        if len(results) > 1:
            scores = [r['relevance_score'] for r in results]
            self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_search_functions(self):
        """Test function search."""
        results = search_functions("merge dictionaries", top_k=5)
        
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 5)
        
        # Check all results have relevance scores
        for result in results:
            self.assertIn('relevance_score', result)
            self.assertGreaterEqual(result['relevance_score'], 0)
            self.assertLessEqual(result['relevance_score'], 1)
    
    def test_format_recommendation(self):
        """Test recommendation formatting."""
        func = {
            'name': 'test_func',
            'code': 'def test_func(): pass',
            'description': 'Test function',
            'usage': 'test_func()',
            'complexity': 'O(1)',
            'relevance_score': 0.95,
            'popularity': 8
        }
        
        formatted = format_recommendation(func)
        self.assertIn('test_func', formatted)
        self.assertIn('def test_func(): pass', formatted)
        self.assertIn('Test function', formatted)
        self.assertIn('O(1)', formatted)
    
    def test_format_recommendation_code_only(self):
        """Test recommendation formatting without metadata."""
        func = {
            'name': 'test_func',
            'code': 'def test_func(): pass',
        }
        
        formatted = format_recommendation(func, include_metadata=False)
        self.assertIn('def test_func(): pass', formatted)


class TestRelevanceScoring(unittest.TestCase):
    """Test relevance scoring functionality."""
    
    def test_calculate_relevance_score(self):
        """Test relevance score calculation."""
        intent = {
            'action': 'sort',
            'data_type': 'list',
            'order': 'descending',
            'keywords': ['sort', 'list', 'descending', 'numbers']
        }
        
        function_metadata = {
            'action': 'sort',
            'data_type': 'list',
            'order': 'descending',
            'keywords': ['sort', 'descending', 'unique', 'list', 'numbers']
        }
        
        score = calculate_relevance_score(intent, function_metadata)
        self.assertGreater(score, 0.5)  # Should have good match
        self.assertLessEqual(score, 1.0)
    
    def test_calculate_relevance_score_no_match(self):
        """Test relevance score with poor match."""
        intent = {
            'action': 'sort',
            'data_type': 'list',
            'keywords': ['sort', 'list'],
            'original_text': 'sort a list'
        }
        
        function_metadata = {
            'action': 'validate',
            'data_type': 'string',
            'keywords': ['validate', 'email', 'string'],
            'name': 'validate_email',
            'id': 'validate_email',
            'popularity': 5
        }
        
        score = calculate_relevance_score(intent, function_metadata)
        self.assertLess(score, 0.5)  # Should have poor match


if __name__ == '__main__':
    unittest.main()
