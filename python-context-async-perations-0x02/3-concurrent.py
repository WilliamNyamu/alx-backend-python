# Run multiple database queries concurrently using asyncio.gather.
# Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() 
# that fetches all users and users older than 40 respectively.
import aiosqlite
from aiosqlite import Error
import time
import asyncio
import functools

def timer(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"Time taken: {elapsed:.2f} seconds")
        return value
    return wrapper

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        try:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users")
            results = await cursor.fetchall()
            return results
        except Error as e:
            print(f"Error occured: {e}")


async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        try:
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM users WHERE age > 100")
            results = await cursor.fetchall()
            return results
        except Error as e:
            print(f"Error occured: {e}")
        
@timer
async def main():
    users = await async_fetch_users()
    for user in users:
        print(user)

asyncio.run(main())