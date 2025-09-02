#!/usr/bin/env python3
"""
SQLite version - Generator that streams rows from an SQL database one by one
"""

import seed_sqlite as seed


def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    
    Yields:
        dict: A dictionary containing user data with keys: user_id, name, email, age
    """
    connection = seed.connect_to_prodev()
    if connection:
        # Configure row factory to return dictionaries
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        
        # Use fetchone() in a loop to get one row at a time
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            # Convert sqlite3.Row to dict
            yield dict(row)
        
        cursor.close()
        connection.close()


import sqlite3
