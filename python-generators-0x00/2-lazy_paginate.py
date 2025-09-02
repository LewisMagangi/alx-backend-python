#!/usr/bin/env python3
"""
Lazy loading paginated data from the users database
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database.
    
    Args:
        page_size (int): Number of users per page
        offset (int): Number of rows to skip
        
    Returns:
        list: List of user dictionaries
    """
    connection = seed.connect_to_prodev()
    try:
        # Try MySQL syntax first
        cursor = connection.cursor(dictionary=True)
    except TypeError:
        # Fallback to SQLite - connection already has row_factory set
        cursor = connection.cursor()
        
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    
    # Convert SQLite Rows to dicts if needed
    if rows and hasattr(rows[0], 'keys'):
        rows = [dict(row) for row in rows]
    
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator function that implements lazy loading of paginated data.
    Only fetches the next page when needed.
    
    Args:
        page_size (int): Number of users per page
        
    Yields:
        list: A page of user data
    """
    offset = 0
    
    while True:
        page = paginate_users(page_size, offset)
        
        if not page:
            break
            
        yield page
        offset += page_size
