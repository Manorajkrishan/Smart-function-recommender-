"""
Run 10,000 test cases and generate comprehensive report.
"""

import json
import os
import time
import sys
from typing import Dict, List
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from smart_func import get_function, recommend_functions
from smart_func.cache import clear_cache


def load_test_cases(test_file: str = 'test_cases_10000.json') -> List[Dict]:
    """Load test cases from file."""
    test_path = os.path.join(os.path.dirname(__file__), test_file)
    with open(test_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_test_case(test_case: Dict) -> Dict:
    """Run a single test case."""
    query = test_case['query']
    language = test_case.get('language_filter')
    if language == 'all':
        language = None
    
    start_time = time.time()
    
    try:
        result = get_function(query, language=language)
        elapsed = time.time() - start_time
        
        if result:
            # Check if result matches expected
            is_correct = (
                result.get('id') == test_case.get('expected_function_id') or
                result.get('name') == test_case.get('expected_name')
            )
            
            relevance = result.get('relevance_score', 0)
            min_relevance = test_case.get('min_relevance', 0.0)
            meets_threshold = relevance >= min_relevance
            
            return {
                'test_id': test_case['id'],
                'query': query,
                'success': True,
                'correct': is_correct,
                'meets_threshold': meets_threshold,
                'result_id': result.get('id'),
                'result_name': result.get('name'),
                'result_language': result.get('language'),
                'relevance_score': relevance,
                'expected_id': test_case.get('expected_function_id'),
                'expected_name': test_case.get('expected_name'),
                'elapsed_time': elapsed,
                'error': None
            }
        else:
            return {
                'test_id': test_case['id'],
                'query': query,
                'success': False,
                'correct': False,
                'meets_threshold': False,
                'result_id': None,
                'result_name': None,
                'result_language': None,
                'relevance_score': 0,
                'expected_id': test_case.get('expected_function_id'),
                'expected_name': test_case.get('expected_name'),
                'elapsed_time': elapsed,
                'error': 'No result returned'
            }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            'test_id': test_case['id'],
            'query': query,
            'success': False,
            'correct': False,
            'meets_threshold': False,
            'result_id': None,
            'result_name': None,
            'result_language': None,
            'relevance_score': 0,
            'expected_id': test_case.get('expected_function_id'),
            'expected_name': test_case.get('expected_name'),
            'elapsed_time': elapsed,
            'error': str(e)
        }


def run_all_tests(test_cases: List[Dict], batch_size: int = 100) -> Dict:
    """Run all test cases and collect statistics."""
    print(f"Running {len(test_cases)} test cases...")
    print(f"Batch size: {batch_size}")
    print()
    
    results = []
    start_time = time.time()
    
    for i, test_case in enumerate(test_cases, 1):
        result = run_test_case(test_case)
        results.append(result)
        
        if i % batch_size == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed
            print(f"Progress: {i}/{len(test_cases)} ({i/len(test_cases)*100:.1f}%) - "
                  f"Rate: {rate:.1f} tests/sec - "
                  f"Accuracy: {sum(r['correct'] for r in results)/len(results)*100:.1f}%")
    
    total_time = time.time() - start_time
    
    # Calculate statistics
    stats = calculate_statistics(results, total_time)
    
    return {
        'results': results,
        'statistics': stats,
        'total_time': total_time
    }


def calculate_statistics(results: List[Dict], total_time: float) -> Dict:
    """Calculate test statistics."""
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    correct = sum(1 for r in results if r['correct'])
    meets_threshold = sum(1 for r in results if r['meets_threshold'])
    
    errors = [r for r in results if r['error']]
    error_types = defaultdict(int)
    for r in errors:
        error_types[r['error']] += 1
    
    # By language
    by_language = defaultdict(lambda: {'total': 0, 'correct': 0, 'success': 0})
    for r in results:
        lang = r.get('result_language', 'unknown')
        by_language[lang]['total'] += 1
        if r['success']:
            by_language[lang]['success'] += 1
        if r['correct']:
            by_language[lang]['correct'] += 1
    
    # Performance metrics
    elapsed_times = [r['elapsed_time'] for r in results if r['elapsed_time']]
    avg_time = sum(elapsed_times) / len(elapsed_times) if elapsed_times else 0
    min_time = min(elapsed_times) if elapsed_times else 0
    max_time = max(elapsed_times) if elapsed_times else 0
    
    # Relevance scores
    relevance_scores = [r['relevance_score'] for r in results if r['relevance_score'] > 0]
    avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
    
    return {
        'total_tests': total,
        'successful_tests': successful,
        'failed_tests': total - successful,
        'correct_predictions': correct,
        'incorrect_predictions': total - correct,
        'meets_threshold': meets_threshold,
        'accuracy': (correct / total * 100) if total > 0 else 0,
        'success_rate': (successful / total * 100) if total > 0 else 0,
        'threshold_rate': (meets_threshold / total * 100) if total > 0 else 0,
        'total_time_seconds': total_time,
        'tests_per_second': total / total_time if total_time > 0 else 0,
        'average_time_per_test': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'average_relevance': avg_relevance,
        'error_types': dict(error_types),
        'by_language': {
            lang: {
                'total': stats['total'],
                'success_rate': (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0,
                'accuracy': (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            }
            for lang, stats in by_language.items()
        }
    }


def save_results(results_data: Dict, output_path: str = 'test_results_10000.json'):
    """Save test results to file."""
    output_path = os.path.join(os.path.dirname(__file__), output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {output_path}")


def print_report(stats: Dict):
    """Print test report."""
    print("\n" + "="*60)
    print("TEST EXECUTION REPORT")
    print("="*60)
    print(f"\nTotal Tests: {stats['total_tests']}")
    print(f"Successful: {stats['successful_tests']} ({stats['success_rate']:.2f}%)")
    print(f"Failed: {stats['failed_tests']}")
    print(f"\nCorrect Predictions: {stats['correct_predictions']} ({stats['accuracy']:.2f}%)")
    print(f"Incorrect Predictions: {stats['incorrect_predictions']}")
    print(f"Meets Threshold: {stats['meets_threshold']} ({stats['threshold_rate']:.2f}%)")
    print(f"\nPerformance:")
    print(f"  Total Time: {stats['total_time_seconds']:.2f} seconds")
    print(f"  Tests/Second: {stats['tests_per_second']:.2f}")
    print(f"  Avg Time/Test: {stats['average_time_per_test']*1000:.2f} ms")
    print(f"  Min Time: {stats['min_time']*1000:.2f} ms")
    print(f"  Max Time: {stats['max_time']*1000:.2f} ms")
    print(f"\nQuality:")
    print(f"  Average Relevance: {stats['average_relevance']:.2%}")
    
    if stats['error_types']:
        print(f"\nErrors:")
        for error, count in stats['error_types'].items():
            print(f"  {error}: {count}")
    
    if stats['by_language']:
        print(f"\nBy Language:")
        for lang, lang_stats in stats['by_language'].items():
            print(f"  {lang}:")
            print(f"    Total: {lang_stats['total']}")
            print(f"    Success Rate: {lang_stats['success_rate']:.2f}%")
            print(f"    Accuracy: {lang_stats['accuracy']:.2f}%")
    
    print("\n" + "="*60)


def main():
    """Main test execution."""
    # Clear cache before testing
    clear_cache()
    
    # Load test cases
    print("Loading test cases...")
    test_cases = load_test_cases()
    print(f"Loaded {len(test_cases)} test cases\n")
    
    # Run tests
    results_data = run_all_tests(test_cases)
    
    # Print report
    print_report(results_data['statistics'])
    
    # Save results
    save_results(results_data)
    
    print("\nSUCCESS: Test execution complete!")


if __name__ == '__main__':
    main()
