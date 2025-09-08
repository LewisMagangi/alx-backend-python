#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager

This module demonstrates a reusable context manager that takes a query 
as input and executes it, managing both connection and query execution.

The ExecuteQuery context manager provides:
- Parameterized query execution
- Automatic connection management
- Result fetching and cleanup
- Exception handling
"""

import sqlite3
import os


class ExecuteQuery:
    """
    A reusable context manager for executing parameterized database queries.
    
    This class implements the context manager protocol to handle:
    - Database connection establishment
    - Query execution with parameters
    - Result fetching
    - Automatic resource cleanup
    """
    
    def __init__(self, database_name="users.db", query=None, parameters=None):
        """
        Initialize the ExecuteQuery context manager.
        
        Args:
            database_name (str): Name of the SQLite database file
            query (str): SQL query to execute
            parameters (tuple): Parameters for the SQL query
        """
        self.database_name = database_name
        self.query = query
        self.parameters = parameters or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Enter the context manager - establish connection and execute query.
        
        Returns:
            list: Query results or empty list if no results
        """
        try:
            # Establish database connection
            self.connection = sqlite3.connect(self.database_name)
            self.cursor = self.connection.cursor()
            
            print(f"Connected to database: {self.database_name}")
            
            # Setup sample data if needed
            self._ensure_sample_data()
            
            # Execute the query if provided
            if self.query:
                print(f"Executing query: {self.query}")
                print(f"Parameters: {self.parameters}")
                
                self.cursor.execute(self.query, self.parameters)
                
                # Fetch results for SELECT queries
                if self.query.strip().upper().startswith('SELECT'):
                    self.results = self.cursor.fetchall()
                    print(f"Query executed successfully. Found {len(self.results)} records.")
                else:
                    # For non-SELECT queries, commit the transaction
                    self.connection.commit()
                    print(f"Query executed successfully. Affected rows: {self.cursor.rowcount}")
                    self.results = []
            else:
                self.results = []
                print("No query provided. Connection established for manual operations.")
            
            return self.results
            
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            self._cleanup()
            raise
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            self._cleanup()
            raise
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - cleanup resources.
        
        Args:
            exc_type: Exception type (if any)
            exc_value: Exception value (if any)
            traceback: Exception traceback (if any)
            
        Returns:
            bool: False to propagate exceptions
        """
        self._cleanup()
        
        # Handle exceptions that occurred within the context
        if exc_type:
            print(f"Exception in context: {exc_type.__name__}: {exc_value}")
            return False  # Propagate the exception
        
        print("Query execution context closed successfully.")
        return True
    
    def _cleanup(self):
        """Clean up database resources."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                print("Database connection closed.")
        except sqlite3.Error as e:
            print(f"Error during cleanup: {e}")
    
    def _ensure_sample_data(self):
        """Ensure sample data exists in the database."""
        try:
            # Create users table if it doesn't exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    age INTEGER
                )
            ''')
            
            # Check if sample data exists
            self.cursor.execute('SELECT COUNT(*) FROM users')
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                # Insert comprehensive sample data
                sample_users = [
                    ('Alice Johnson', 'alice@example.com', 28),
                    ('Bob Smith', 'bob@example.com', 35),
                    ('Charlie Brown', 'charlie@example.com', 42),
                    ('Diana Prince', 'diana@example.com', 30),
                    ('Eve Wilson', 'eve@example.com', 25),
                    ('Frank Miller', 'frank@example.com', 45),
                    ('Grace Kelly', 'grace@example.com', 38),
                    ('Henry Ford', 'henry@example.com', 52),
                    ('Ivy Chen', 'ivy@example.com', 29),
                    ('Jack Black', 'jack@example.com', 41)
                ]
                
                self.cursor.executemany(
                    'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                    sample_users
                )
                self.connection.commit()
                print("Sample data created for demonstration.")
                
        except sqlite3.Error as e:
            print(f"Error setting up sample data: {e}")


def demonstrate_reusable_context_manager():
    """
    Demonstrate the usage of ExecuteQuery context manager.
    
    This function shows how to use the reusable context manager 
    with different queries and parameters.
    """
    print("=" * 70)
    print("TASK 1: Reusable Query Context Manager Demo")
    print("=" * 70)
    
    # Required query: SELECT * FROM users WHERE age > ? with parameter 25
    print("\n1. Required Query: Users older than 25")
    print("-" * 50)
    
    query = "SELECT * FROM users WHERE age > ?"
    parameters = (25,)
    
    try:
        with ExecuteQuery("users.db", query, parameters) as results:
            if results:
                print(f"\n{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
                print("-" * 50)
                for row in results:
                    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
                print(f"\nTotal users older than 25: {len(results)}")
            else:
                print("No users found matching the criteria.")
    
    except Exception as e:
        print(f"Error executing required query: {e}")
    
    # Additional demonstration queries
    print("\n2. Additional Query: Users older than 40")
    print("-" * 50)
    
    try:
        with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (40,)) as results:
            if results:
                print(f"\n{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
                print("-" * 50)
                for row in results:
                    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
                print(f"\nTotal users older than 40: {len(results)}")
            else:
                print("No users found older than 40.")
                
    except Exception as e:
        print(f"Error executing additional query: {e}")
    
    # Demonstrate query with specific name search
    print("\n3. Query with LIKE operator: Names containing 'a'")
    print("-" * 50)
    
    try:
        with ExecuteQuery("users.db", 
                         "SELECT * FROM users WHERE name LIKE ?", 
                         ('%a%',)) as results:
            if results:
                print(f"\n{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
                print("-" * 50)
                for row in results:
                    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
                print(f"\nTotal users with 'a' in name: {len(results)}")
            else:
                print("No users found with 'a' in their name.")
                
    except Exception as e:
        print(f"Error executing name search query: {e}")


def demonstrate_error_handling():
    """
    Demonstrate error handling in the ExecuteQuery context manager.
    """
    print("\n" + "=" * 70)
    print("ERROR HANDLING DEMONSTRATION")
    print("=" * 70)
    
    # Test with invalid query
    print("\nTesting with invalid SQL query...")
    try:
        with ExecuteQuery("users.db", 
                         "SELECT * FROM non_existent_table", 
                         ()) as results:
            print("This should not print due to the error above.")
            
    except sqlite3.OperationalError as e:
        print(f"Caught expected SQL error: {e}")
        print("* Context manager properly handled the exception and cleaned up resources.")
    
    # Test with invalid parameters
    print("\nTesting with mismatched parameters...")
    try:
        with ExecuteQuery("users.db", 
                         "SELECT * FROM users WHERE age > ? AND name = ?", 
                         (25,)) as results:  # Missing second parameter
            print("This should not print due to the error above.")
            
    except sqlite3.Error as e:
        print(f"Caught expected parameter error: {e}")
        print("* Context manager properly handled parameter mismatch.")


def demonstrate_statistics():
    """
    Demonstrate statistical queries using the reusable context manager.
    """
    print("\n" + "=" * 70)
    print("STATISTICAL QUERIES DEMONSTRATION")
    print("=" * 70)
    
    # Average age query
    print("\n1. Average age of all users:")
    try:
        with ExecuteQuery("users.db", "SELECT AVG(age) as avg_age FROM users") as results:
            if results and results[0][0] is not None:
                avg_age = round(results[0][0], 2)
                print(f"   Average age: {avg_age} years")
            else:
                print("   No data available for average calculation.")
    except Exception as e:
        print(f"   Error calculating average: {e}")
    
    # Count by age groups
    print("\n2. Age group distribution:")
    try:
        age_groups = [
            ("Young adults (18-30)", "age BETWEEN 18 AND 30"),
            ("Middle age (31-45)", "age BETWEEN 31 AND 45"),
            ("Older adults (46+)", "age >= 46")
        ]
        
        for group_name, condition in age_groups:
            query = f"SELECT COUNT(*) FROM users WHERE {condition}"
            with ExecuteQuery("users.db", query) as results:
                count = results[0][0] if results else 0
                print(f"   {group_name}: {count} users")
                
    except Exception as e:
        print(f"   Error calculating age groups: {e}")


if __name__ == "__main__":
    # Run the main demonstration
    demonstrate_reusable_context_manager()
    
    # Demonstrate error handling
    demonstrate_error_handling()
    
    # Demonstrate statistical queries
    demonstrate_statistics()
    
    print("\n" + "=" * 70)
    print("Task 1 completed successfully! [✓]")
    print("=" * 70)
    print("The ExecuteQuery context manager demonstrates:")
    print("[✓] Reusable query execution with parameters")
    print("[✓] Automatic connection and resource management")
    print("[✓] Proper exception handling and cleanup")
    print("[✓] Support for various SQL query types")
    print("[✓] Parameterized queries for security")
    print("=" * 70)
