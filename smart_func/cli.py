"""
CLI interface for Smart Function Recommender.
"""

import argparse
import sys
from smart_func.generator import get_function, recommend_functions, format_recommendation


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Smart Function Recommender - Get code snippets from natural language descriptions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smart-func "sort a list in descending order and remove duplicates"
  smart-func "merge two dictionaries" --top 3
  smart-func "find maximum value in list" --code-only
        """
    )
    
    parser.add_argument(
        'query',
        type=str,
        help='Natural language description of the function you need'
    )
    
    parser.add_argument(
        '--top',
        type=int,
        default=1,
        help='Number of recommendations to return (default: 1)'
    )
    
    parser.add_argument(
        '--code-only',
        action='store_true',
        help='Output only the code snippet without metadata'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    parser.add_argument(
        '--lang',
        type=str,
        default=None,
        choices=['python', 'javascript', 'java', 'csharp', 'go', 'rust'],
        help='Filter by programming language (default: all languages)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.top == 1:
            # Single recommendation
            result = get_function(args.query, top_k=1, language=args.lang)
            
            if result is None:
                print("No matching function found. Try rephrasing your query.", file=sys.stderr)
                sys.exit(1)
            
            # Warn if relevance is very low (might be a poor match)
            relevance = result.get('relevance_score', 0)
            if relevance < 0.4 and not args.code_only:
                print(f"\n⚠️  Warning: Low relevance score ({relevance:.1%}). This might not be the best match.", file=sys.stderr)
                print("Consider rephrasing your query or checking if the function exists in the database.\n", file=sys.stderr)
            
            if args.json:
                import json
                print(json.dumps(result, indent=2))
            elif args.code_only:
                print(result.get('code', ''))
            else:
                print(format_recommendation(result))
        else:
            # Multiple recommendations
            results = recommend_functions(args.query, top_k=args.top, language=args.lang)
            
            if not results:
                print("No matching functions found. Try rephrasing your query.", file=sys.stderr)
                sys.exit(1)
            
            if args.json:
                import json
                print(json.dumps(results, indent=2))
            elif args.code_only:
                for i, func in enumerate(results, 1):
                    print(f"# Option {i}")
                    print(func.get('code', ''))
                    print()
            else:
                for i, func in enumerate(results, 1):
                    print(f"\n{'='*60}")
                    print(f"RECOMMENDATION {i} of {len(results)}")
                    print(f"{'='*60}\n")
                    print(format_recommendation(func))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
