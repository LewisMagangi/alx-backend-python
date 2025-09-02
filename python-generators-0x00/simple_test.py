#!/usr/bin/env python3
"""
Simple test for individual functions
"""

import sys
import seed_sqlite as seed
sys.modules['seed'] = seed

# Test the stream_users function
print("Testing stream_users:")
from itertools import islice
stream_users_module = __import__('0-stream_users')

for i, user in enumerate(islice(stream_users_module.stream_users(), 3)):
    print(f"User {i+1}: {user}")

print("\nTesting batch processing:")
batch_module = __import__('1-batch_processing')

print("Users over 25 (first 10):")
count = 0
for batch in islice(batch_module.stream_users_in_batches(5), 2):
    for user in batch:
        if user.get('age', 0) > 25:
            print(f"  {user.get('name', 'Unknown')} (age: {user.get('age', 0)})")
            count += 1
            if count >= 10:
                break
    if count >= 10:
        break

print(f"\nFound {count} users over 25")
