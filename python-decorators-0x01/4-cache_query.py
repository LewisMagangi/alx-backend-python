import time
import sqlite3 
import functools

def with_db_connection(func):
    """
    Decorator that automatically handles opening and closing database connections.
    Opens a connection, passes it to the function, and closes it afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass connection to the decorated function
            return func(conn, *args, **kwargs)
        finally:
            # Ensure connection is closed
            conn.close()
    return wrapper

query_cache = {}

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    Avoids redundant database calls by storing and retrieving cached results.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from the function arguments
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        
        if query:
            # Check if query result is already cached
            if query in query_cache:
                print(f"Cache hit for query: {query}")
                return query_cache[query]
            
            # Execute the function and cache the result
            print(f"Cache miss for query: {query}")
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result
        else:
            # If no query is found, just execute the function
            return func(*args, **kwargs)
    
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")