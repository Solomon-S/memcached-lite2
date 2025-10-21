#!/usr/bin/env python3
from pymemcache.client.base import Client

def main():
    # Connect to your server
    client = Client(('127.0.0.1', 9889))

    # Test 1: Store a key
    client.set('user1', 'solomon_siang')
    result1 = client.get('user1')
    print("user1:", result1.decode() if result1 else None)

    # Test 2: Store another key
    client.set('bday1', '11/21/03')
    result2 = client.get('bday1')
    print("bday1:", result2.decode() if result2 else None)

    # Test 3: Missing key
    result3 = client.get('does_not_exist')
    print("does_not_exist:", result3)

if __name__ == "__main__":
    main()
