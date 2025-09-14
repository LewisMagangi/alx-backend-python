# Python Decorators Project

This project implements five custom Python decorators for enhancing database operations in Python applications.

## Project Overview

The project focuses on mastering Python decorators to create reusable, efficient, and clean code for database management. Each decorator addresses a specific aspect of database operations:

1. **Query Logging** - Log all SQL queries for observability
2. **Connection Management** - Automatic database connection handling
3. **Transaction Management** - Robust transaction handling with commit/rollback
4. **Retry Mechanism** - Resilience against transient database errors
5. **Query Caching** - Performance optimization through result caching

## Files Description

### Task 0: `0-log_queries.py`

- **Decorator**: `@log_queries`
- **Purpose**: Logs SQL queries before execution
- **Features**: Intercepts function calls to enhance observability

### Task 1: `1-with_db_connection.py`

- **Decorator**: `@with_db_connection`
- **Purpose**: Automates database connection handling
- **Features**: Opens connection, passes it to function, ensures cleanup

### Task 2: `2-transactional.py`

- **Decorator**: `@transactional`
- **Purpose**: Manages database transactions
- **Features**: Automatic commit on success, rollback on error

### Task 3: `3-retry_on_failure.py`

- **Decorator**: `@retry_on_failure(retries=3, delay=2)`
- **Purpose**: Retries database operations on failure
- **Features**: Configurable retry attempts and delay intervals

### Task 4: `4-cache_query.py`

- **Decorator**: `@cache_query`
- **Purpose**: Caches query results to avoid redundant calls
- **Features**: Query string-based caching mechanism

## Setup and Testing

### Prerequisites

- Python 3.8 or higher
- SQLite3 (included with Python)

### Database Setup

```bash
python setup_test_db.py
```

This creates a `users.db` SQLite database with sample data.

### Running Individual Tests

```bash
# Test logging decorator
python 0-log_queries.py

# Test connection decorator
python 1-with_db_connection.py

# Test transaction decorator
python 2-transactional.py

# Test retry decorator
python 3-retry_on_failure.py

# Test caching decorator
python 4-cache_query.py
```

## Key Features Demonstrated

### 1. Function Wrapping

All decorators use `functools.wraps()` to preserve function metadata.

### 2. Error Handling

- Transaction decorator implements try/except with rollback
- Retry decorator handles exceptions with configurable attempts

### 3. Resource Management

- Connection decorator ensures proper cleanup with try/finally
- Automatic connection opening and closing

### 4. Performance Optimization

- Caching decorator reduces redundant database calls
- Query result storage and retrieval

### 5. Observability

- Query logging for debugging and monitoring
- Cache hit/miss reporting

## Database Schema

The test database contains a `users` table with the following structure:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER
);
```

## Sample Data

The database includes 5 sample users:

- Alice Johnson (age 28)
- Bob Smith (age 35)
- Carol Williams (age 24)
- David Brown (age 42)
- Eve Davis (age 31)

## Learning Outcomes

By implementing these decorators, you will gain:

- Deep understanding of Python decorator patterns
- Best practices for database connection management
- Transaction handling and error recovery techniques
- Performance optimization through caching
- Robust error handling and retry mechanisms

## Best Practices Demonstrated

1. **Decorator Composition**: Multiple decorators can be stacked
2. **Resource Cleanup**: Always ensure database connections are closed
3. **Error Propagation**: Re-raise exceptions after handling
4. **Configurable Behavior**: Parameterized decorators for flexibility
5. **Function Preservation**: Use `functools.wraps()` to maintain metadata

## Usage Examples

### Basic Query with Logging

```python
@log_queries
def fetch_users(query):
    # Implementation
    pass
```

### Transaction Management

```python
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    # Implementation with automatic transaction handling
    pass
```

### Retry with Custom Parameters

```python
@with_db_connection
@retry_on_failure(retries=5, delay=3)
def critical_operation(conn):
    # Implementation with enhanced retry logic
    pass
```

## Project Status

✅ All tasks completed successfully
✅ Database setup functional
✅ All decorators tested and verified
✅ Comprehensive documentation provided
