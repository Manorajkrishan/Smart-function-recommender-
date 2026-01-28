"""
Quick test script to verify the web server is working.
"""

import requests
import sys

def test_server():
    """Test if the server is responding."""
    base_url = "http://localhost:8000"
    
    print("Testing web server...")
    print("=" * 60)
    
    # Test health endpoint
    try:
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Health check passed: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server. Is it running?")
        print("   💡 Start the server with: python web_app/app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test search endpoint
    try:
        print("\n2. Testing search endpoint...")
        response = requests.post(
            f"{base_url}/api/search",
            json={"query": "sort list", "top_k": 1},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Search works! Found: {data[0]['name']}")
        else:
            print(f"   ❌ Search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test main page
    try:
        print("\n3. Testing main page...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Main page loads! (Length: {len(response.text)} chars)")
        else:
            print(f"   ❌ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Server is working correctly.")
    print(f"\n🌐 Open your browser and visit: {base_url}")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
