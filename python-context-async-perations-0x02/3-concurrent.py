#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries - Minimal Version
Meeting exact requirements only.
"""

import asyncio
import aiosqlite
from typing import List, Tuple, Any


async def setup_database(db_name: str = "users.db") -> None:
    """Setup database with sample data."""
    async with aiosqlite.connect(db_name) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        
        # Insert sample data if table is empty
        async with db.execute('SELECT COUNT(*) FROM users') as cursor:
            count = await cursor.fetchone()
            
        if count[0] == 0:
            users = [
                ('Alice', 25), ('Bob', 35), ('Charlie', 45),
                ('Diana', 30), ('Eve', 42), ('Frank', 38)
            ]
            await db.executemany(
                'INSERT INTO users (name, age) VALUES (?, ?)', users
            )
            await db.commit()


async def async_fetch_users() -> List[Tuple[Any, ...]]:
    """Fetch all users from database."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users() -> List[Tuple[Any, ...]]:
    """Fetch users older than 40."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather()."""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print(f"All users: {len(all_users)}")
    print(f"Users older than 40: {len(older_users)}")
    
    return all_users, older_users


async def main():
    """Main function."""
    await setup_database()
    await fetch_concurrently()


if __name__ == "__main__":
    # Use asyncio.run() to run fetch_concurrently()
    asyncio.run(main())
    