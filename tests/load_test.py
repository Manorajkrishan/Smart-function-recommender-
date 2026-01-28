"""
Load testing for 1000 concurrent users.
"""

import asyncio
import aiohttp
import time
import json
from typing import List, Dict
from collections import defaultdict

BASE_URL = "http://localhost:8000"
CONCURRENT_USERS = 1000
REQUESTS_PER_USER = 10
TOTAL_REQUESTS = CONCURRENT_USERS * REQUESTS_PER_USER

# Test queries
TEST_QUERIES = [
    "sort list descending",
    "merge dictionaries",
    "find maximum",
    "reverse string",
    "filter array",
    "sum numbers",
    "remove duplicates",
    "capitalize string",
    "short list",
    "average numbers"
]


async def make_request(session: aiohttp.ClientSession, query: str, user_id: int) -> Dict:
    """Make a single API request."""
    start_time = time.time()
    
    try:
        async with session.post(
            f"{BASE_URL}/api/search",
            json={"query": query, "top_k": 1},
            timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            elapsed = time.time() - start_time
            status = response.status
            data = await response.json() if status == 200 else None
            
            return {
                'user_id': user_id,
                'query': query,
                'status': status,
                'elapsed': elapsed,
                'success': status == 200,
                'has_results': bool(data and len(data) > 0) if data else False
            }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            'user_id': user_id,
            'query': query,
            'status': 0,
            'elapsed': elapsed,
            'success': False,
            'error': str(e),
            'has_results': False
        }


async def simulate_user(session: aiohttp.ClientSession, user_id: int) -> List[Dict]:
    """Simulate a single user making multiple requests."""
    results = []
    
    for i in range(REQUESTS_PER_USER):
        query = TEST_QUERIES[i % len(TEST_QUERIES)]
        result = await make_request(session, query, user_id)
        results.append(result)
        
        # Small delay between requests
        await asyncio.sleep(0.1)
    
    return results


async def run_load_test():
    """Run load test with concurrent users."""
    print(f"Starting load test...")
    print(f"Concurrent Users: {CONCURRENT_USERS}")
    print(f"Requests per User: {REQUESTS_PER_USER}")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Target: {BASE_URL}\n")
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Create tasks for all users
        tasks = [
            simulate_user(session, user_id)
            for user_id in range(1, CONCURRENT_USERS + 1)
        ]
        
        # Run all tasks concurrently
        print("Executing requests...")
        all_results = await asyncio.gather(*tasks)
    
    total_time = time.time() - start_time
    
    # Flatten results
    results = []
    for user_results in all_results:
        results.extend(user_results)
    
    # Calculate statistics
    stats = calculate_load_stats(results, total_time)
    
    # Print report
    print_load_report(stats)
    
    # Save results
    save_load_results(results, stats)
    
    return stats


def calculate_load_stats(results: List[Dict], total_time: float) -> Dict:
    """Calculate load test statistics."""
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    failed = total - successful
    has_results = sum(1 for r in results if r.get('has_results', False))
    
    # Response times
    elapsed_times = [r['elapsed'] for r in results]
    avg_time = sum(elapsed_times) / len(elapsed_times) if elapsed_times else 0
    min_time = min(elapsed_times) if elapsed_times else 0
    max_time = max(elapsed_times) if elapsed_times else 0
    
    # Percentiles
    sorted_times = sorted(elapsed_times)
    p50 = sorted_times[int(len(sorted_times) * 0.5)] if sorted_times else 0
    p95 = sorted_times[int(len(sorted_times) * 0.95)] if sorted_times else 0
    p99 = sorted_times[int(len(sorted_times) * 0.99)] if sorted_times else 0
    
    # Status codes
    status_codes = defaultdict(int)
    for r in results:
        status_codes[r['status']] += 1
    
    # Errors
    errors = [r for r in results if not r['success']]
    error_types = defaultdict(int)
    for r in errors:
        error = r.get('error', 'Unknown')
        error_types[error] += 1
    
    return {
        'total_requests': total,
        'successful_requests': successful,
        'failed_requests': failed,
        'success_rate': (successful / total * 100) if total > 0 else 0,
        'requests_with_results': has_results,
        'result_rate': (has_results / total * 100) if total > 0 else 0,
        'total_time_seconds': total_time,
        'requests_per_second': total / total_time if total_time > 0 else 0,
        'average_response_time': avg_time,
        'min_response_time': min_time,
        'max_response_time': max_time,
        'p50_response_time': p50,
        'p95_response_time': p95,
        'p99_response_time': p99,
        'status_codes': dict(status_codes),
        'error_types': dict(error_types),
        'concurrent_users': CONCURRENT_USERS,
        'requests_per_user': REQUESTS_PER_USER
    }


def print_load_report(stats: Dict):
    """Print load test report."""
    print("\n" + "="*60)
    print("LOAD TEST REPORT - 1000 CONCURRENT USERS")
    print("="*60)
    print(f"\nTotal Requests: {stats['total_requests']}")
    print(f"Successful: {stats['successful_requests']} ({stats['success_rate']:.2f}%)")
    print(f"Failed: {stats['failed_requests']}")
    print(f"Requests with Results: {stats['requests_with_results']} ({stats['result_rate']:.2f}%)")
    
    print(f"\nPerformance:")
    print(f"  Total Time: {stats['total_time_seconds']:.2f} seconds")
    print(f"  Requests/Second: {stats['requests_per_second']:.2f}")
    print(f"  Average Response Time: {stats['average_response_time']*1000:.2f} ms")
    print(f"  Min Response Time: {stats['min_response_time']*1000:.2f} ms")
    print(f"  Max Response Time: {stats['max_response_time']*1000:.2f} ms")
    print(f"  P50 (Median): {stats['p50_response_time']*1000:.2f} ms")
    print(f"  P95: {stats['p95_response_time']*1000:.2f} ms")
    print(f"  P99: {stats['p99_response_time']*1000:.2f} ms")
    
    if stats['status_codes']:
        print(f"\nStatus Codes:")
        for code, count in sorted(stats['status_codes'].items()):
            print(f"  {code}: {count}")
    
    if stats['error_types']:
        print(f"\nErrors:")
        for error, count in stats['error_types'].items():
            print(f"  {error}: {count}")
    
    print("\n" + "="*60)
    
    # Performance assessment
    print("\nPerformance Assessment:")
    if stats['success_rate'] >= 99:
        print("✅ Excellent: Success rate >= 99%")
    elif stats['success_rate'] >= 95:
        print("✅ Good: Success rate >= 95%")
    elif stats['success_rate'] >= 90:
        print("⚠️  Acceptable: Success rate >= 90%")
    else:
        print("❌ Poor: Success rate < 90%")
    
    if stats['p95_response_time'] < 1.0:
        print("✅ Excellent: P95 response time < 1 second")
    elif stats['p95_response_time'] < 2.0:
        print("✅ Good: P95 response time < 2 seconds")
    elif stats['p95_response_time'] < 5.0:
        print("⚠️  Acceptable: P95 response time < 5 seconds")
    else:
        print("❌ Poor: P95 response time >= 5 seconds")
    
    if stats['requests_per_second'] >= 100:
        print("✅ Excellent: Throughput >= 100 req/s")
    elif stats['requests_per_second'] >= 50:
        print("✅ Good: Throughput >= 50 req/s")
    elif stats['requests_per_second'] >= 20:
        print("⚠️  Acceptable: Throughput >= 20 req/s")
    else:
        print("❌ Poor: Throughput < 20 req/s")


def save_load_results(results: List[Dict], stats: Dict):
    """Save load test results."""
    output_path = os.path.join(os.path.dirname(__file__), 'load_test_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'statistics': stats,
            'sample_results': results[:100]  # Save first 100 for analysis
        }, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {output_path}")


def main():
    """Run load test."""
    print("="*60)
    print("SMART FUNCTION RECOMMENDER - LOAD TEST")
    print("="*60)
    print("\n⚠️  Make sure the server is running on http://localhost:8000")
    print("Press Enter to start load test, or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    try:
        asyncio.run(run_load_test())
        print("\n✅ Load test complete!")
    except Exception as e:
        print(f"\n❌ Load test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
