#!/usr/bin/env python3
"""
Task 0: Custom Class-Based Context Manager for Database Connection

This module demonstrates a class-based context manager that handles 
database connections automatically using __enter__ and __exit__ methods.

The context manager ensures proper resource management by:
- Opening database connection on entry
- Automatically closing connection on exit
- Handling exceptions gracefully
"""

import sqlite3
import os


class DatabaseConnection:
    """
    A custom context manager for handling SQLite database connections.
    
    This class implements the context manager protocol using __enter__ 
    and __exit__ methods to ensure automatic connection cleanup.
    """
    
    def __init__(self, database_name="users.db"):
        """
        Initialize the DatabaseConnection context manager.
        
        Args:
            database_name (str): Name of the SQLite database file
        """
        self.database_name = database_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Enter the context manager - establish database connection.
        
        Returns:
            sqlite3.Cursor: Database cursor for executing queries
        """
        try:
            # Create connection to SQLite database
            self.connection = sqlite3.connect(self.database_name)
            self.cursor = self.connection.cursor()
            
            # Create users table if it doesn't exist (for demonstration)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    age INTEGER
                )
            ''')
            
            # Insert sample data if table is empty
            self.cursor.execute('SELECT COUNT(*) FROM users')
            if self.cursor.fetchone()[0] == 0:
                sample_users = [
                    ('Alice Johnson', 'alice@example.com', 28),
                    ('Bob Smith', 'bob@example.com', 35),
                    ('Charlie Brown', 'charlie@example.com', 42),
                    ('Diana Prince', 'diana@example.com', 30),
                    ('Eve Wilson', 'eve@example.com', 25)
                ]
                
                self.cursor.executemany(
                    'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                    sample_users
                )
                self.connection.commit()
                print("Sample data inserted into users table.")
            
            print(f"Database connection established to '{self.database_name}'")
            return self.cursor
            
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            if self.connection:
                self.connection.close()
            raise
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            if self.connection:
                self.connection.close()
            raise
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - cleanup database resources.
        
        Args:
            exc_type: Exception type (if any)
            exc_value: Exception value (if any)
            traceback: Exception traceback (if any)
            
        Returns:
            bool: False to propagate exceptions, True to suppress them
        """
        try:
            if self.cursor:
                self.cursor.close()
                print("Database cursor closed.")
            
            if self.connection:
                # Commit any pending transactions before closing
                self.connection.commit()
                self.connection.close()
                print("Database connection closed successfully.")
                
        except sqlite3.Error as e:
            print(f"Error during database cleanup: {e}")
        
        # Handle exceptions that occurred within the context
        if exc_type:
            print(f"Exception occurred in context: {exc_type.__name__}: {exc_value}")
            # Return False to propagate the exception
            return False
        
        return True


def demonstrate_context_manager():
    """
    Demonstrate the usage of DatabaseConnection context manager.
    
    This function shows how to use the context manager with the 'with' 
    statement to perform database queries safely.
    """
    print("=" * 60)
    print("TASK 0: Custom Class-Based Context Manager Demo")
    print("=" * 60)
    
    try:
        # Use the context manager with 'with' statement
        with DatabaseConnection() as cursor:
            print("\nExecuting query: SELECT * FROM users")
            print("-" * 40)
            
            # Execute the required query
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            
            # Print results in a formatted way
            if results:
                print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
                print("-" * 50)
                for row in results:
                    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
                print(f"\nTotal users found: {len(results)}")
            else:
                print("No users found in the database.")
        
        print("\n" + "=" * 60)
        print("Context manager demonstration completed successfully!")
        print("Connection was automatically closed when exiting the 'with' block.")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during demonstration: {e}")


def demonstrate_exception_handling():
    """
    Demonstrate exception handling within the context manager.
    
    This shows how the context manager properly cleans up resources
    even when exceptions occur within the 'with' block.
    """
    print("\n" + "=" * 60)
    print("EXCEPTION HANDLING DEMONSTRATION")
    print("=" * 60)
    
    try:
        with DatabaseConnection() as cursor:
            print("Attempting to execute an invalid query...")
            # This will raise an exception
            cursor.execute("SELECT * FROM non_existent_table")
            
    except sqlite3.OperationalError as e:
        print(f"Caught expected exception: {e}")
        print("Notice: Connection was still properly closed despite the exception!")
    
    print("=" * 60)


if __name__ == "__main__":
    # Run the main demonstration
    demonstrate_context_manager()
    
    # Demonstrate exception handling
    demonstrate_exception_handling()
    
    print("\nTask 0 completed successfully! [✓]")
    print("The DatabaseConnection context manager properly handles:")
    print("[✓] Automatic connection establishment")
    print("[✓] Resource cleanup on exit")
    print("[✓] Exception handling and propagation")
    print("[✓] Sample data creation for testing")
