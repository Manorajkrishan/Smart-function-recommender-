"""
Analyze test failures to improve accuracy.
"""

import json
import os
from collections import defaultdict

def load_results():
    """Load test results."""
    results_path = os.path.join(os.path.dirname(__file__), 'test_results_10000.json')
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_failures():
    """Analyze why tests failed."""
    data = load_results()
    results = data['results']
    
    # Get incorrect predictions
    incorrect = [r for r in results if not r['correct']]
    
    print(f"Total Tests: {len(results)}")
    print(f"Incorrect: {len(incorrect)} ({len(incorrect)/len(results)*100:.2f}%)")
    print(f"\nAnalyzing {len(incorrect)} failures...\n")
    
    # Group by expected language
    by_language = defaultdict(list)
    for r in incorrect:
        lang = r.get('expected_language', 'unknown')
        by_language[lang].append(r)
    
    print("Failures by Language:")
    for lang, failures in sorted(by_language.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {lang}: {len(failures)} failures")
    
    # Common failure patterns
    print("\nCommon Failure Patterns:")
    
    # Low relevance scores
    low_relevance = [r for r in incorrect if r.get('relevance_score', 0) < 0.3]
    print(f"  Low relevance (<30%): {len(low_relevance)}")
    
    # Wrong language returned
    wrong_language = [
        r for r in incorrect 
        if r.get('result_language') and r.get('expected_language') and 
        r['result_language'] != r['expected_language']
    ]
    print(f"  Wrong language: {len(wrong_language)}")
    
    # No results
    no_results = [r for r in incorrect if not r.get('result_id')]
    print(f"  No results: {len(no_results)}")
    
    # Sample failures
    print("\nSample Failures (first 10):")
    for i, r in enumerate(incorrect[:10], 1):
        print(f"\n{i}. Query: '{r['query']}'")
        print(f"   Expected: {r.get('expected_name', 'N/A')} ({r.get('expected_language', 'N/A')})")
        print(f"   Got: {r.get('result_name', 'N/A')} ({r.get('result_language', 'N/A')})")
        print(f"   Relevance: {r.get('relevance_score', 0)*100:.1f}%")
    
    # Save analysis
    analysis = {
        'total_tests': len(results),
        'incorrect_count': len(incorrect),
        'accuracy': (len(results) - len(incorrect)) / len(results) * 100,
        'failures_by_language': {lang: len(failures) for lang, failures in by_language.items()},
        'failure_patterns': {
            'low_relevance': len(low_relevance),
            'wrong_language': len(wrong_language),
            'no_results': len(no_results)
        },
        'sample_failures': incorrect[:20]
    }
    
    output_path = os.path.join(os.path.dirname(__file__), 'failure_analysis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\nAnalysis saved to {output_path}")

if __name__ == '__main__':
    analyze_failures()
