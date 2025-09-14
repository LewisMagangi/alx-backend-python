import sqlite3

def create_test_database():
    """
    Create a test database with sample users data
    """
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect('c:/Users/User/Documents/GitHub/alx-backend-python/python-decorators-0x01/users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER
        )
    ''')
    
    # Insert sample data
    sample_users = [
        ('Alice Johnson', 'alice.johnson@email.com', 28),
        ('Bob Smith', 'bob.smith@email.com', 35),
        ('Carol Williams', 'carol.williams@email.com', 24),
        ('David Brown', 'david.brown@email.com', 42),
        ('Eve Davis', 'eve.davis@email.com', 31)
    ]
    
    # Clear existing data first
    cursor.execute('DELETE FROM users')
    
    # Insert sample users
    cursor.executemany(
        'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
        sample_users
    )
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Test database 'users.db' created successfully with sample data!")

if __name__ == "__main__":
    create_test_database()