#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries

This module demonstrates running multiple database queries concurrently 
using asyncio.gather() and aiosqlite for asynchronous SQLite operations.

Key features:
- Asynchronous database operations with aiosqlite
- Concurrent query execution using asyncio.gather()
- Performance comparison between sequential and concurrent execution
- Proper async context management
"""

import asyncio
import aiosqlite
import time
import os
from typing import List, Tuple, Any


async def setup_database(database_name: str = "async_users.db") -> None:
    """
    Set up the database with sample data for testing.
    
    Args:
        database_name (str): Name of the SQLite database file
    """
    async with aiosqlite.connect(database_name) as db:
        # Create users table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                department TEXT,
                salary REAL,
                join_date TEXT
            )
        ''')
        
        # Check if data already exists
        async with db.execute('SELECT COUNT(*) FROM users') as cursor:
            count = await cursor.fetchone()
            
        if count[0] == 0:
            # Insert comprehensive sample data
            sample_users = [
                ('Alice Johnson', 'alice@company.com', 28, 'Engineering', 75000, '2020-01-15'),
                ('Bob Smith', 'bob@company.com', 35, 'Marketing', 65000, '2019-03-20'),
                ('Charlie Brown', 'charlie@company.com', 42, 'Engineering', 85000, '2018-07-10'),
                ('Diana Prince', 'diana@company.com', 30, 'HR', 60000, '2021-02-14'),
                ('Eve Wilson', 'eve@company.com', 25, 'Sales', 55000, '2022-05-18'),
                ('Frank Miller', 'frank@company.com', 45, 'Engineering', 95000, '2017-09-05'),
                ('Grace Kelly', 'grace@company.com', 38, 'Finance', 70000, '2019-11-12'),
                ('Henry Ford', 'henry@company.com', 52, 'Operations', 80000, '2016-04-22'),
                ('Ivy Chen', 'ivy@company.com', 29, 'Engineering', 78000, '2020-08-30'),
                ('Jack Black', 'jack@company.com', 41, 'Marketing', 68000, '2018-12-03'),
                ('Kelly Green', 'kelly@company.com', 33, 'Sales', 58000, '2021-06-25'),
                ('Liam Davis', 'liam@company.com', 27, 'Engineering', 72000, '2022-01-10'),
                ('Maya Patel', 'maya@company.com', 39, 'Finance', 75000, '2019-08-15'),
                ('Noah Wilson', 'noah@company.com', 44, 'Operations', 82000, '2017-11-28'),
                ('Olivia Brown', 'olivia@company.com', 31, 'HR', 62000, '2020-12-07')
            ]
            
            await db.executemany(
                '''INSERT INTO users 
                   (name, email, age, department, salary, join_date) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                sample_users
            )
            await db.commit()
            print(f"Database '{database_name}' created with {len(sample_users)} sample users.")


async def asyncfetchusers(database_name: str = "async_users.db") -> List[Tuple[Any, ...]]:
    """
    Asynchronously fetch all users from the database.
    
    Args:
        database_name (str): Name of the SQLite database file
        
    Returns:
        List[Tuple]: List of all user records
    """
    print(">> Starting asyncfetchusers...")
    start_time = time.time()
    
    try:
        async with aiosqlite.connect(database_name) as db:
            async with db.execute("SELECT * FROM users ORDER BY name") as cursor:
                users = await cursor.fetchall()
                
        execution_time = time.time() - start_time
        print(f"[✓] asyncfetchusers completed in {execution_time:.3f}s - Found {len(users)} users")
        return users
        
    except Exception as e:
        print(f"[!] Error in asyncfetchusers: {e}")
        return []


async def asyncfetcholder_users(database_name: str = "async_users.db", min_age: int = 40) -> List[Tuple[Any, ...]]:
    """
    Asynchronously fetch users older than the specified age.
    
    Args:
        database_name (str): Name of the SQLite database file
        min_age (int): Minimum age for filtering users
        
    Returns:
        List[Tuple]: List of user records older than min_age
    """
    print(f">> Starting asyncfetcholder_users (age > {min_age})...")
    start_time = time.time()
    
    try:
        async with aiosqlite.connect(database_name) as db:
            async with db.execute(
                "SELECT * FROM users WHERE age > ? ORDER BY age DESC", 
                (min_age,)
            ) as cursor:
                older_users = await cursor.fetchall()
                
        execution_time = time.time() - start_time
        print(f"[✓] asyncfetcholder_users completed in {execution_time:.3f}s - Found {len(older_users)} users")
        return older_users
        
    except Exception as e:
        print(f"[!] Error in asyncfetcholder_users: {e}")
        return []


async def async_fetch_by_department(database_name: str = "async_users.db", department: str = "Engineering") -> List[Tuple[Any, ...]]:
    """
    Asynchronously fetch users from a specific department.
    
    Args:
        database_name (str): Name of the SQLite database file
        department (str): Department to filter by
        
    Returns:
        List[Tuple]: List of users in the specified department
    """
    print(f">> Starting async_fetch_by_department ({department})...")
    start_time = time.time()
    
    try:
        async with aiosqlite.connect(database_name) as db:
            async with db.execute(
                "SELECT * FROM users WHERE department = ? ORDER BY salary DESC", 
                (department,)
            ) as cursor:
                dept_users = await cursor.fetchall()
                
        execution_time = time.time() - start_time
        print(f"[✓] async_fetch_by_department completed in {execution_time:.3f}s - Found {len(dept_users)} users")
        return dept_users
        
    except Exception as e:
        print(f"[!] Error in async_fetch_by_department: {e}")
        return []


async def async_fetch_salary_stats(database_name: str = "async_users.db") -> List[Tuple[Any, ...]]:
    """
    Asynchronously fetch salary statistics.
    
    Args:
        database_name (str): Name of the SQLite database file
        
    Returns:
        List[Tuple]: Salary statistics
    """
    print(">> Starting async_fetch_salary_stats...")
    start_time = time.time()
    
    try:
        async with aiosqlite.connect(database_name) as db:
            async with db.execute(
                """SELECT 
                   AVG(salary) as avg_salary,
                   MIN(salary) as min_salary,
                   MAX(salary) as max_salary,
                   COUNT(*) as total_employees
                   FROM users"""
            ) as cursor:
                stats = await cursor.fetchall()
                
        execution_time = time.time() - start_time
        print(f"[✓] async_fetch_salary_stats completed in {execution_time:.3f}s")
        return stats
        
    except Exception as e:
        print(f"[!] Error in async_fetch_salary_stats: {e}")
        return []


async def fetch_concurrently(database_name: str = "async_users.db") -> Tuple[List, List]:
    """
    Execute multiple queries concurrently using asyncio.gather().
    
    This function demonstrates the main requirement: running asyncfetchusers()
    and asyncfetcholder_users() concurrently.
    
    Args:
        database_name (str): Name of the SQLite database file
        
    Returns:
        Tuple[List, List]: Results from both queries
    """
    print("\n" + "=" * 80)
    print(">> CONCURRENT EXECUTION USING asyncio.gather()")
    print("=" * 80)
    
    start_time = time.time()
    
    try:
        # Execute the required queries concurrently
        all_users, older_users = await asyncio.gather(
            asyncfetchusers(database_name),
            asyncfetcholder_users(database_name)
        )
        
        total_time = time.time() - start_time
        
        print(f"\n>> Total concurrent execution time: {total_time:.3f}s")
        print(f"[Stats] Results summary:")
        print(f"   • Total users: {len(all_users)}")
        print(f"   • Users older than 40: {len(older_users)}")
        
        return all_users, older_users
        
    except Exception as e:
        print(f"[!] Error in concurrent execution: {e}")
        return [], []


async def fetch_advanced_concurrently(database_name: str = "async_users.db") -> Tuple[List, List, List, List]:
    """
    Execute multiple advanced queries concurrently for demonstration.
    
    Args:
        database_name (str): Name of the SQLite database file
        
    Returns:
        Tuple: Results from all queries
    """
    print("\n" + "=" * 80)
    print(">> ADVANCED CONCURRENT EXECUTION (4 Queries)")
    print("=" * 80)
    
    start_time = time.time()
    
    try:
        # Execute multiple queries concurrently
        results = await asyncio.gather(
            asyncfetchusers(database_name),
            asyncfetcholder_users(database_name),
            async_fetch_by_department(database_name, "Engineering"),
            async_fetch_salary_stats(database_name)
        )
        
        total_time = time.time() - start_time
        
        all_users, older_users, engineering_users, salary_stats = results
        
        print(f"\n>> Total concurrent execution time: {total_time:.3f}s")
        print(f"[Stats] Advanced results summary:")
        print(f"   • Total users: {len(all_users)}")
        print(f"   • Users older than 40: {len(older_users)}")
        print(f"   • Engineering department: {len(engineering_users)}")
        
        if salary_stats:
            stats = salary_stats[0]
            print(f"   • Salary stats: Avg=${stats[0]:.2f}, Min=${stats[1]:.2f}, Max=${stats[2]:.2f}")
        
        return results
        
    except Exception as e:
        print(f"[!] Error in advanced concurrent execution: {e}")
        return [], [], [], []


async def compare_sequential_vs_concurrent(database_name: str = "async_users.db") -> None:
    """
    Compare performance between sequential and concurrent execution.
    
    Args:
        database_name (str): Name of the SQLite database file
    """
    print("\n" + "=" * 80)
    print(">> PERFORMANCE COMPARISON: Sequential vs Concurrent")
    print("=" * 80)
    
    # Sequential execution
    print("\n1. Sequential execution:")
    sequential_start = time.time()
    
    users_seq = await asyncfetchusers(database_name)
    older_users_seq = await asyncfetcholder_users(database_name)
    
    sequential_time = time.time() - sequential_start
    print(f"   [Time] Sequential total time: {sequential_time:.3f}s")
    
    # Small delay to separate the tests
    await asyncio.sleep(0.1)
    
    # Concurrent execution
    print("\n2. Concurrent execution:")
    concurrent_start = time.time()
    
    users_conc, older_users_conc = await asyncio.gather(
        asyncfetchusers(database_name),
        asyncfetcholder_users(database_name)
    )
    
    concurrent_time = time.time() - concurrent_start
    print(f"   [Time] Concurrent total time: {concurrent_time:.3f}s")
    
    # Performance analysis
    print(f"\n[Stats] Performance Analysis:")
    print(f"   • Sequential time: {sequential_time:.3f}s")
    print(f"   • Concurrent time: {concurrent_time:.3f}s")
    
    if concurrent_time > 0:
        improvement = ((sequential_time - concurrent_time) / sequential_time) * 100
        speedup = sequential_time / concurrent_time
        print(f"   • Performance improvement: {improvement:.1f}%")
        print(f"   • Speedup factor: {speedup:.2f}x")
    else:
        print(f"   • Performance improvement: Concurrent execution too fast to measure precisely")
        print(f"   • Result: Concurrent execution completed in under 1ms")


def display_results(all_users: List[Tuple], older_users: List[Tuple]) -> None:
    """
    Display query results in a formatted way.
    
    Args:
        all_users (List[Tuple]): All users data
        older_users (List[Tuple]): Older users data
    """
    print("\n" + "=" * 80)
    print("[Results] QUERY RESULTS")
    print("=" * 80)
    
    # Display all users (first 10)
    print(f"\n1. All Users (showing first 10 of {len(all_users)}):")
    print("-" * 80)
    if all_users:
        print(f"{'ID':<4} {'Name':<15} {'Email':<25} {'Age':<4} {'Department':<12} {'Salary':<8}")
        print("-" * 80)
        for user in all_users[:10]:
            print(f"{user[0]:<4} {user[1]:<15} {user[2]:<25} {user[3]:<4} {user[4]:<12} ${user[5]:<7.0f}")
    
    # Display older users
    print(f"\n2. Users Older Than 40 (all {len(older_users)} results):")
    print("-" * 80)
    if older_users:
        print(f"{'ID':<4} {'Name':<15} {'Email':<25} {'Age':<4} {'Department':<12} {'Salary':<8}")
        print("-" * 80)
        for user in older_users:
            print(f"{user[0]:<4} {user[1]:<15} {user[2]:<25} {user[3]:<4} {user[4]:<12} ${user[5]:<7.0f}")
    else:
        print("No users found older than 40.")


async def main():
    """
    Main function to demonstrate concurrent asynchronous database operations.
    """
    print("=" * 80)
    print("TASK 2: Concurrent Asynchronous Database Queries")
    print("=" * 80)
    
    database_name = "async_users.db"
    
    # Setup database
    print(">> Setting up database...")
    await setup_database(database_name)
    
    # Required implementation: Run fetch_concurrently()
    all_users, older_users = await fetch_concurrently(database_name)
    
    # Display results
    display_results(all_users, older_users)
    
    # Performance comparison
    await compare_sequential_vs_concurrent(database_name)
    
    # Advanced concurrent operations (bonus)
    await fetch_advanced_concurrently(database_name)
    
    print("\n" + "=" * 80)
    print("[✓] Task 2 completed successfully!")
    print("=" * 80)
    print("Demonstrated features:")
    print("[✓] aiosqlite for asynchronous SQLite operations")
    print("[✓] asyncfetchusers() and asyncfetcholder_users() functions")
    print("[✓] asyncio.gather() for concurrent execution")
    print("[✓] asyncio.run() for running concurrent operations")
    print("[✓] Performance comparison between sequential and concurrent")
    print("[✓] Proper async context management")
    print("[✓] Error handling in async operations")
    print("=" * 80)


if __name__ == "__main__":
    # Run the main async function using asyncio.run()
    print(">> Starting asynchronous database operations...")
    
    try:
        # This demonstrates the required asyncio.run(fetch_concurrently()) pattern
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user.")
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
    
    print("\n>> Async operations demonstration completed!")
