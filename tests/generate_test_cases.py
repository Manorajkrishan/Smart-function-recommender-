"""
Generate 10,000 test cases for Smart Function Recommender.
"""

import json
import random
import os
from typing import List, Dict

# Load the function database to generate realistic test cases
def load_functions():
    """Load functions from database."""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'smart_func', 'database.json')
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_test_cases(num_cases: int = 10000) -> List[Dict]:
    """Generate test cases."""
    functions = load_functions()
    
    # Common query patterns
    query_templates = [
        # Direct function name queries
        "{name}",
        "how to {name}",
        "{name} function",
        "code for {name}",
        
        # Description-based queries
        "{description}",
        "how to {description}",
        "function to {description}",
        
        # Keyword-based queries
        "{keyword1} {keyword2}",
        "{keyword1} and {keyword2}",
        "how to {keyword1} {keyword2}",
        
        # Action-based queries
        "{action} {data_type}",
        "{action} a {data_type}",
        "how to {action} {data_type}",
        
        # Natural language variations
        "I need to {description}",
        "show me {name}",
        "get {name}",
        "create {name}",
        "implement {name}",
        
        # Language-specific queries
        "{name} in {language}",
        "{description} {language}",
        "{language} {name}",
        
        # Complex queries
        "{action} {data_type} and {keyword1}",
        "{name} with {keyword1}",
        "{description} using {keyword1}",
    ]
    
    # Common variations and synonyms
    variations = {
        'sort': ['sort', 'order', 'arrange', 'organize'],
        'find': ['find', 'search', 'locate', 'get'],
        'merge': ['merge', 'combine', 'join', 'unite'],
        'reverse': ['reverse', 'flip', 'invert'],
        'filter': ['filter', 'select', 'choose'],
        'calculate': ['calculate', 'compute', 'get'],
        'list': ['list', 'array', 'collection'],
        'string': ['string', 'text'],
        'dictionary': ['dictionary', 'dict', 'object', 'map'],
    }
    
    test_cases = []
    
    for i in range(num_cases):
        # Pick a random function
        func = random.choice(functions)
        
        # Generate query based on template
        template = random.choice(query_templates)
        
        # Fill in template
        query = template.format(
            name=func.get('name', ''),
            description=func.get('description', ''),
            action=func.get('action', ''),
            data_type=func.get('data_type', ''),
            keyword1=random.choice(func.get('keywords', [''])[:3] or ['']),
            keyword2=random.choice(func.get('keywords', [''])[3:6] or ['']),
            language=func.get('language', 'python')
        )
        
        # Add variations
        for key, synonyms in variations.items():
            if key in query.lower():
                query = query.replace(key, random.choice(synonyms), 1)
        
        # Expected result
        expected_function_id = func.get('id')
        expected_language = func.get('language', 'python')
        
        test_case = {
            'id': f'test_{i+1:05d}',
            'query': query.strip(),
            'expected_function_id': expected_function_id,
            'expected_language': expected_language,
            'expected_name': func.get('name'),
            'language_filter': random.choice([None, expected_language, 'all']),
            'min_relevance': random.choice([0.0, 0.3, 0.5, 0.7]),
        }
        
        test_cases.append(test_case)
    
    return test_cases


def save_test_cases(test_cases: List[Dict], output_path: str = 'test_cases_10000.json'):
    """Save test cases to JSON file."""
    output_path = os.path.join(os.path.dirname(__file__), output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(test_cases)} test cases to {output_path}")


def main():
    """Generate and save test cases."""
    print("Generating 10,000 test cases...")
    test_cases = generate_test_cases(10000)
    save_test_cases(test_cases)
    
    # Print statistics
    languages = {}
    for case in test_cases:
        lang = case.get('expected_language', 'python')
        languages[lang] = languages.get(lang, 0) + 1
    
    print(f"\nTest case statistics:")
    print(f"Total: {len(test_cases)}")
    print(f"By language:")
    for lang, count in sorted(languages.items()):
        print(f"  {lang}: {count}")


if __name__ == '__main__':
    main()
