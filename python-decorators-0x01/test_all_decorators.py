#!/usr/bin/env python3
"""
Comprehensive test script for all Python decorators
Demonstrates the functionality of each decorator implemented
"""

import sqlite3
import os

def test_all_decorators():
    """Test all implemented decorators"""
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=" * 60)
    print("TESTING PYTHON DECORATORS PROJECT")
    print("=" * 60)
    
    # Test 1: Log Queries Decorator
    print("\n1. TESTING LOG QUERIES DECORATOR")
    print("-" * 40)
    exec(open('0-log_queries.py').read())
    
    print("\n2. TESTING DATABASE CONNECTION DECORATOR")
    print("-" * 40)
    exec(open('1-with_db_connection.py').read())
    
    print("\n3. TESTING TRANSACTION MANAGEMENT DECORATOR")
    print("-" * 40)
    exec(open('2-transactional.py').read())
    print("Transaction completed successfully!")
    
    print("\n4. TESTING RETRY DECORATOR")
    print("-" * 40)
    exec(open('3-retry_on_failure.py').read())
    
    print("\n5. TESTING CACHE DECORATOR")
    print("-" * 40)
    exec(open('4-cache_query.py').read())
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_all_decorators()