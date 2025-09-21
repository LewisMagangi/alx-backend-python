# Context Managers and Asynchronous Programming in Python

A demonstration of advanced Python techniques for database connection management and asynchronous operations.

## Overview

This project showcases three key Python programming concepts:

- **Custom Context Managers**: Automatic resource management with proper cleanup
- **Reusable Query Executors**: Parameterized database operations
- **Asynchronous Programming**: Concurrent database queries for improved performance

## Features

- Class-based context managers using `__enter__` and `__exit__` methods
- SQLite database operations with automatic connection handling
- Asynchronous database queries using `aiosqlite`
- Concurrent execution with `asyncio.gather()`
- Comprehensive error handling and resource cleanup

## Tasks Completed

- [x] **0. Custom class based context manager for Database connection**
  - Implemented `DatabaseConnection` class with proper resource management
  - Automatic database connection opening and closing
  - Exception handling with guaranteed cleanup

- [x] **1. Reusable Query Context Manager**
  - Created `ExecuteQuery` class for parameterized database operations
  - Supports reusable query execution with parameters
  - Proper resource management and error handling

- [ ] **2. Concurrent Asynchronous Database Queries**
  - Implemented `async_fetch_users()` and `async_fetch_older_users()` functions
  - Used `asyncio.gather()` for concurrent query execution
  - Performance comparison between sequential and concurrent operations

## Requirements

- Python 3.7+
- `aiosqlite` library

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run individual demonstrations:

```bash
python 0-databaseconnection.py   # Basic context manager
python 1-execute.py              # Reusable query executor
python 3-concurrent.py           # Async concurrent operations
```

Or run all tests:

```bash
python test_all.py
```

## Project Structure

```text
├── 0-databaseconnection.py    # Context manager implementation
├── 1-execute.py               # Query executor with parameters
├── 3-concurrent.py            # Async concurrent operations
├── test_all.py                # Comprehensive test runner
└── README.md                  # Project documentation
```

## Key Concepts Demonstrated

### Context Managers

Automatic resource acquisition and cleanup using the `with` statement pattern.

### Database Connection Management

Proper handling of SQLite connections with automatic cleanup to prevent resource leaks.

### Asynchronous Programming

Non-blocking database operations that can run concurrently for improved performance.

## Example Output

The demonstrations create sample databases and show:

- Database connection lifecycle management
- Query execution with parameterized inputs
- Performance comparisons between sequential and concurrent operations
- Error handling and recovery mechanisms

## License

This project is for educational purposes.
