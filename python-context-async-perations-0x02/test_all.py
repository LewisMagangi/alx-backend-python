#!/usr/bin/env python3
"""
Test runner for all Context Managers and Async Programming tasks.

This script runs all three task files in sequence and provides
a comprehensive overview of the project functionality.
"""

import subprocess
import sys
import os
import time


def run_task(task_file, task_name):
    """
    Run a specific task file and capture its output.
    
    Args:
        task_file (str): Path to the task file
        task_name (str): Name of the task for display
    """
    print("\n" + "=" * 80)
    print(f">> RUNNING {task_name}")
    print("=" * 80)
    
    try:
        # Run the task file
        result = subprocess.run(
            [sys.executable, task_file],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # Display output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"[✓] {task_name} completed successfully!")
        else:
            print(f"[!] {task_name} failed with return code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"[!] {task_name} timed out after 30 seconds")
    except Exception as e:
        print(f"[!] Error running {task_name}: {e}")


def check_requirements():
    """Check if all required packages are installed."""
    print(">> Checking requirements...")
    
    try:
        import sqlite3
        print("[✓] sqlite3 (standard library) - OK")
    except ImportError:
        print("[!] sqlite3 not available")
        return False
    
    try:
        import aiosqlite
        print("[✓] aiosqlite - OK")
    except ImportError:
        print("[!] aiosqlite not installed. Run: pip install aiosqlite")
        return False
    
    try:
        import asyncio
        print("[✓] asyncio (standard library) - OK")
    except ImportError:
        print("[!] asyncio not available")
        return False
    
    return True


def main():
    """Main test runner function."""
    print("=" * 80)
    print(">> CONTEXT MANAGERS & ASYNC PROGRAMMING - TEST RUNNER")
    print("=" * 80)
    print("Project: ALX Backend Python")
    print("Directory: python-context-async-perations-0x02")
    print("Date:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Check if we're in the right directory
    if not os.path.exists("0-databaseconnection.py"):
        print("\n[!] Error: Task files not found!")
        print("Make sure you're in the python-context-async-perations-0x02 directory")
        return
    
    # Check requirements
    if not check_requirements():
        print("\n[!] Requirements check failed. Please install missing packages.")
        return
    
    print("\n>> All requirements satisfied. Starting tests...")
    
    # Define tasks to run
    tasks = [
        ("0-databaseconnection.py", "TASK 0: Custom Class-Based Context Manager"),
        ("1-execute.py", "TASK 1: Reusable Query Context Manager"),
        ("3-concurrent.py", "TASK 2: Concurrent Asynchronous Database Queries")
    ]
    
    # Run each task
    for task_file, task_name in tasks:
        if os.path.exists(task_file):
            run_task(task_file, task_name)
            time.sleep(1)  # Small delay between tasks
        else:
            print(f"\n[!] {task_file} not found!")
    
    # Summary
    print("\n" + "=" * 80)
    print("[Stats] TEST SUMMARY")
    print("=" * 80)
    print("All tasks have been executed. Check the output above for:")
    print("[✓] Database connection management")
    print("[✓] Context manager implementations")
    print("[✓] Asynchronous query execution")
    print("[✓] Concurrent operation performance")
    print("[✓] Error handling and resource cleanup")
    
    print("\n[Files] Generated files:")
    for db_file in ["users.db", "async_users.db"]:
        if os.path.exists(db_file):
            print(f"   • {db_file} (SQLite database)")
    
    print("\n>> Test run completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
