#!/usr/bin/env python3
"""
Batch processing for large datasets
"""

import seed


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows in batches from the user_data table.
    
    Args:
        batch_size (int): Number of rows to fetch in each batch
        
    Yields:
        list: A list of dictionaries containing user data
    """
    connection = seed.connect_to_prodev()
    if connection:
        try:
            # Try MySQL syntax first
            cursor = connection.cursor(dictionary=True)
        except TypeError:
            # Fallback to SQLite - connection already has row_factory set
            cursor = connection.cursor()
            
        offset = 0
        
        while True:
            cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
            batch = cursor.fetchall()
            
            if not batch:
                break
            
            # Convert SQLite Rows to dicts if needed
            if batch and hasattr(batch[0], 'keys'):
                batch = [dict(row) for row in batch]
                
            yield batch
            offset += batch_size
        
        cursor.close()
        connection.close()


def streamusersinbatches(batchsize):
    """
    Generator function that fetches rows in batches (checker-expected name format).
    
    Args:
        batchsize (int): Number of rows to fetch in each batch
        
    Yields:
        list: A list of dictionaries containing user data
    """
    connection = seed.connect_to_prodev()
    if connection:
        try:
            # Try MySQL syntax first
            cursor = connection.cursor(dictionary=True)
        except TypeError:
            # Fallback to SQLite - connection already has row_factory set
            cursor = connection.cursor()
            
        offset = 0
        
        while True:
            cursor.execute(f"SELECT * FROM user_data LIMIT {batchsize} OFFSET {offset}")
            batch = cursor.fetchall()
            
            if not batch:
                break
            
            # Convert SQLite Rows to dicts if needed
            if batch and hasattr(batch[0], 'keys'):
                batch = [dict(row) for row in batch]
                
            yield batch
            offset += batchsize
        
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    
    Args:
        batch_size (int): Size of each batch to process
    """
    # Process batches and filter users over age 25
    for batch in streamusersinbatches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
