"""
Run evaluation on test cases and analyze results.
"""

import json
import os
import sys
from typing import List, Dict, Tuple
from collections import defaultdict
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_func.generator import get_function, load_database


def load_test_cases(filename: str = 'test_cases_1000.json') -> List[Dict]:
    """Load test cases from JSON file."""
    # Try current directory first, then tests directory
    if not os.path.exists(filename):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(test_dir, filename)
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate_test_case(test_case: Dict, database: List[Dict]) -> Dict:
    """
    Evaluate a single test case.
    
    Returns:
        Dictionary with evaluation results
    """
    query = test_case['query']
    expected_id = test_case['expected_function']
    
    # Get prediction
    result = get_function(query, top_k=1)
    
    if result is None:
        return {
            'query': query,
            'expected': expected_id,
            'predicted': None,
            'correct': False,
            'relevance_score': 0.0,
            'category': test_case.get('category', 'unknown')
        }
    
    predicted_id = result.get('id')
    is_correct = (predicted_id == expected_id)
    
    # Get top 3 to see if expected is in top results
    top_3_results = get_function(query, top_k=3)
    if isinstance(top_3_results, list):
        top_3_ids = [r.get('id') for r in top_3_results]
        rank = top_3_ids.index(expected_id) + 1 if expected_id in top_3_ids else None
    else:
        rank = 1 if is_correct else None
    
    return {
        'query': query,
        'expected': expected_id,
        'predicted': predicted_id,
        'correct': is_correct,
        'relevance_score': result.get('relevance_score', 0.0),
        'rank': rank,
        'category': test_case.get('category', 'unknown'),
        'predicted_name': result.get('name', ''),
        'expected_name': next((f['name'] for f in database if f['id'] == expected_id), 'unknown')
    }


def run_evaluation(test_cases: List[Dict], database: List[Dict]) -> Dict:
    """Run evaluation on all test cases."""
    results = []
    correct = 0
    total = len(test_cases)
    
    print(f"Evaluating {total} test cases...")
    
    for i, test_case in enumerate(test_cases):
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{total} ({100 * (i + 1) / total:.1f}%)")
        
        result = evaluate_test_case(test_case, database)
        results.append(result)
        if result['correct']:
            correct += 1
    
    accuracy = correct / total if total > 0 else 0.0
    
    return {
        'total': total,
        'correct': correct,
        'incorrect': total - correct,
        'accuracy': accuracy,
        'results': results,
        'timestamp': datetime.now().isoformat()
    }


def analyze_results(evaluation: Dict) -> Dict:
    """Analyze evaluation results to find patterns."""
    results = evaluation['results']
    
    # Group by category
    by_category = defaultdict(lambda: {'correct': 0, 'total': 0})
    for result in results:
        cat = result['category']
        by_category[cat]['total'] += 1
        if result['correct']:
            by_category[cat]['correct'] += 1
    
    # Find common failure patterns
    failures = [r for r in results if not r['correct']]
    
    # Group failures by expected function
    failures_by_function = defaultdict(int)
    for failure in failures:
        failures_by_function[failure['expected']] += 1
    
    # Find queries with low relevance scores
    low_relevance = [r for r in results if r['relevance_score'] < 0.3]
    
    # Find cases where expected is in top 3 but not #1
    top3_but_not_first = [r for r in results if not r['correct'] and r.get('rank') is not None]
    
    return {
        'by_category': dict(by_category),
        'top_failure_functions': dict(sorted(failures_by_function.items(), 
                                            key=lambda x: x[1], reverse=True)[:10]),
        'low_relevance_count': len(low_relevance),
        'top3_but_not_first_count': len(top3_but_not_first),
        'sample_failures': failures[:20]  # First 20 failures
    }


def save_results(evaluation: Dict, analysis: Dict, filename: str = 'evaluation_results.json'):
    """Save evaluation results to JSON file."""
    output = {
        'evaluation': {
            'total': evaluation['total'],
            'correct': evaluation['correct'],
            'incorrect': evaluation['incorrect'],
            'accuracy': evaluation['accuracy'],
            'timestamp': evaluation['timestamp']
        },
        'analysis': analysis,
        'all_results': evaluation['results']  # Include all results for detailed analysis
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {filename}")


def print_summary(evaluation: Dict, analysis: Dict):
    """Print evaluation summary."""
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    print(f"Total Test Cases: {evaluation['total']}")
    print(f"Correct: {evaluation['correct']}")
    print(f"Incorrect: {evaluation['incorrect']}")
    print(f"Accuracy: {evaluation['accuracy']:.2%}")
    
    print("\n" + "-"*60)
    print("ACCURACY BY CATEGORY")
    print("-"*60)
    for cat, stats in sorted(analysis['by_category'].items()):
        acc = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        print(f"  {cat:25s}: {stats['correct']:3d}/{stats['total']:3d} ({acc:.2%})")
    
    if analysis['top_failure_functions']:
        print("\n" + "-"*60)
        print("TOP FAILING FUNCTIONS")
        print("-"*60)
        for func_id, count in list(analysis['top_failure_functions'].items())[:5]:
            print(f"  {func_id:30s}: {count} failures")
    
    print(f"\nLow relevance scores (<0.3): {analysis['low_relevance_count']}")
    print(f"Expected in top 3 but not #1: {analysis['top3_but_not_first_count']}")


if __name__ == '__main__':
    # Get project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    # Load test cases and database
    print("Loading test cases and database...")
    test_cases = load_test_cases()
    database = load_database()
    
    # Run evaluation
    evaluation = run_evaluation(test_cases, database)
    
    # Analyze results
    print("\nAnalyzing results...")
    analysis = analyze_results(evaluation)
    
    # Print summary
    print_summary(evaluation, analysis)
    
    # Save results
    save_results(evaluation, analysis)
    
    print("\n" + "="*60)
    print("Evaluation complete!")
