#!/usr/bin/env python3
"""
Memory-efficient aggregation with generators to compute average age
"""

import seed


def stream_user_ages():
    """
    Generator function that yields user ages one by one.
    
    Yields:
        int: User age
    """
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # Fetch and yield ages one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]  # row[0] contains the age value
        
        cursor.close()
        connection.close()


def calculate_average_age():
    """
    Calculate the average age using the generator without loading 
    the entire dataset into memory.
    
    Returns:
        float: Average age of users
    """
    total_age = 0
    count = 0
    
    # Use the generator to process ages one by one
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count


if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")
