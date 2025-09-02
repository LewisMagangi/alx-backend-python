#!/usr/bin/env python3
"""
Generator that streams rows from an SQL database one by one
"""

import seed


def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    
    Yields:
        dict: A dictionary containing user data with keys: user_id, name, email, age
    """
    connection = seed.connect_to_prodev()
    if connection:
        try:
            # Try MySQL syntax first
            cursor = connection.cursor(dictionary=True)
        except TypeError:
            # Fallback to SQLite - connection already has row_factory set
            cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM user_data")
        
        # Use fetchone() in a loop to get one row at a time
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            
            # Convert SQLite Row to dict if needed
            if hasattr(row, 'keys'):
                yield dict(row)
            else:
                # For MySQL, row is already a dict
                yield row
        
        cursor.close()
        connection.close()
