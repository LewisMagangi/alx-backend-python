#!/usr/bin/env python3
"""
Test script for the SQLite version of the project
"""

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Testing SQLite version of the Python Generators project...")
print("=" * 60)

# Test 1: Database setup
print("\n1. Testing database setup...")
try:
    import seed_sqlite as seed
    
    connection = seed.connect_db()
    if connection:
        seed.create_database(connection)
        connection.close()
        print("✓ Database connection successful")
        
        connection = seed.connect_to_prodev()
        if connection:
            seed.create_table(connection)
            seed.insert_data(connection, 'user_data.csv')
            
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM user_data")
            count = cursor.fetchone()[0]
            print(f"✓ Data inserted: {count} rows")
            
            cursor.execute("SELECT * FROM user_data LIMIT 3")
            rows = cursor.fetchall()
            print("✓ Sample data:", rows[:3])
            
            cursor.close()
            connection.close()
        
except Exception as e:
    print(f"✗ Database setup failed: {e}")

print("\n" + "=" * 60)
print("Setup complete! You can now test individual tasks.")
print("Note: Use the original MySQL files for production deployment.")
