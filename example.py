"""
Example usage of Smart Function Recommender as a Python library.
"""

from smart_func import get_function, recommend_functions

# Example 1: Get a single function recommendation
print("=" * 60)
print("Example 1: Single Function Recommendation")
print("=" * 60)
result = get_function("Sort a list of numbers in descending order and remove duplicates")
print(result['code'])
print(f"\nRelevance Score: {result['relevance_score']:.2%}")
print(f"Popularity: {result['popularity']}/10")
print()

# Example 2: Get multiple recommendations
print("=" * 60)
print("Example 2: Multiple Function Recommendations")
print("=" * 60)
results = recommend_functions("merge two dictionaries", top_k=3)
for i, func in enumerate(results, 1):
    print(f"\nOption {i}: {func['name']}")
    print(f"Relevance: {func['relevance_score']:.2%}")
    print(func['code'])
    print()

# Example 3: Search for calculation functions
print("=" * 60)
print("Example 3: Calculation Functions")
print("=" * 60)
results = recommend_functions("calculate sum of numbers", top_k=2)
for func in results:
    print(f"\n{func['name']}:")
    print(func['code'])
    print(f"Usage: {func.get('usage', 'N/A')}")
