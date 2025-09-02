#!/usr/bin/env python3
"""
Alternative seed module using SQLite for local development
"""

import sqlite3
import csv
import uuid
import os


def connect_db():
    """
    Connects to the SQLite database
    
    Returns:
        connection object or None if connection fails
    """
    try:
        # Create database in the current directory
        db_path = os.path.join(os.path.dirname(__file__), 'ALX_prodev.db')
        connection = sqlite3.connect(db_path)
        return connection
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return None


def create_database(connection):
    """
    Creates the database (already handled by SQLite connection)
    
    Args:
        connection: SQLite connection object
    """
    print("Database ALX_prodev.db created successfully or already exists")


def connect_to_prodev():
    """
    Connects to the ALX_prodev SQLite database
    
    Returns:
        connection object or None if connection fails
    """
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'ALX_prodev.db')
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row  # This allows dict-like access
        return connection
    except Exception as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields
    
    Args:
        connection: SQLite connection object
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
        cursor.close()
    except Exception as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data in the database if it does not exist
    
    Args:
        connection: SQLite connection object
        csv_file: path to CSV file containing data
    """
    try:
        cursor = connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("Data already exists in the table")
            cursor.close()
            return
        
        # Read and insert data from CSV
        csv_path = os.path.join(os.path.dirname(__file__), csv_file)
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = int(row['age'])
                
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (?, ?, ?, ?)
                """
                cursor.execute(insert_query, (user_id, name, email, age))
        
        connection.commit()
        print(f"Data inserted successfully from {csv_file}")
        cursor.close()
        
    except Exception as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
