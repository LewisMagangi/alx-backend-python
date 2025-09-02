# Python Generators Project

This project demonstrates advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations.

## Learning Objectives

- Master Python Generators: Learn to create and utilize generators for iterative data processing
- Handle Large Datasets: Implement batch processing and lazy loading
- Simulate Real-world Scenarios: Develop solutions for live data updates
- Optimize Performance: Use generators for memory-efficient calculations
- Apply SQL Knowledge: Integrate Python with databases for data management

## Requirements

- Python 3.x
- MySQL database
- Understanding of `yield` and generator functions
- Familiarity with SQL and database operations

## Project Structure

- `seed.py`: Database setup and data seeding functionality
- `0-stream_users.py`: Generator that streams rows from SQL database
- `1-batch_processing.py`: Batch processing for large datasets
- `2-lazy_paginate.py`: Lazy loading with pagination
- `4-stream_ages.py`: Memory-efficient aggregation with generators
- `user_data.csv`: Sample data file

## Setup

1. Ensure MySQL is installed and running
2. Run the seeding script to set up the database and populate data
3. Execute individual task files to test functionality

## Tasks

### Task 0: Database Setup
Set up MySQL database with user_data table and populate with sample data.

### Task 1: Stream Users
Create a generator that streams rows from the database one by one.

### Task 2: Batch Processing
Process data in batches and filter users over age 25.

### Task 3: Lazy Pagination
Implement lazy loading with pagination for efficient data retrieval.

### Task 4: Memory-Efficient Aggregation
Calculate average age using generators without loading entire dataset into memory.
