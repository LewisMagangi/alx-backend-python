#!/usr/bin/env python3
"""
Test script for the Python generators project
"""

from itertools import islice
import sys
import os

# Import SQLite versions for testing
import seed_sqlite as seed
sys.modules['seed'] = seed  # Replace seed module with SQLite version

# Now import the generator modules
from importlib import import_module

print("Testing Python Generators Project")
print("=" * 50)

# Test 1: Stream users generator
print("\n1. Testing stream_users generator...")
try:
    stream_users_module = import_module('0-stream_users')
    stream_users = stream_users_module.stream_users
    
    # Test streaming first 3 users
    users = list(islice(stream_users(), 3))
    print(f"✓ Streamed {len(users)} users successfully")
    for i, user in enumerate(users, 1):
        print(f"  User {i}: {user['name']} (age: {user['age']})")
except Exception as e:
    print(f"✗ Error testing stream_users: {e}")

# Test 2: Batch processing
print("\n2. Testing batch processing...")
try:
    batch_module = import_module('1-batch_processing')
    stream_users_in_batches = batch_module.stream_users_in_batches
    
    # Test one batch
    batches = list(islice(stream_users_in_batches(5), 1))
    print(f"✓ Fetched batch of {len(batches[0])} users")
    
    # Test filtering users over 25
    over_25_count = 0
    for batch in islice(stream_users_in_batches(10), 3):
        for user in batch:
            if user['age'] > 25:
                over_25_count += 1
    print(f"✓ Found {over_25_count} users over age 25 in first 3 batches")
    
except Exception as e:
    print(f"✗ Error testing batch processing: {e}")

# Test 3: Lazy pagination
print("\n3. Testing lazy pagination...")
try:
    paginate_module = import_module('2-lazy_paginate')
    lazy_pagination = paginate_module.lazy_pagination
    
    # Test pagination
    pages = list(islice(lazy_pagination(10), 2))
    print(f"✓ Fetched {len(pages)} pages with {len(pages[0])} and {len(pages[1])} users respectively")
    
except Exception as e:
    print(f"✗ Error testing lazy pagination: {e}")

# Test 4: Memory-efficient aggregation
print("\n4. Testing memory-efficient aggregation...")
try:
    ages_module = import_module('4-stream_ages')
    calculate_average_age = ages_module.calculate_average_age
    
    # Calculate average age
    avg_age = calculate_average_age()
    print(f"✓ Average age calculated: {avg_age:.2f}")
    
except Exception as e:
    print(f"✗ Error testing average age calculation: {e}")

print("\n" + "=" * 50)
print("Testing completed!")
print("\nTo test with MySQL:")
print("1. Ensure MySQL server is running")
print("2. Update connection parameters in seed.py if needed")
print("3. Run the individual test files (0-main.py, 1-main.py, etc.)")
