# Run multiple database queries concurrently using asyncio.gather.
# Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() 
# that fetches all users and users older than 40 respectively.
import aiosqlite
from aiosqlite import Error
import time
import asyncio

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
            await cursor.execute("SELECT * FROM users WHERE age > 40")
            results = await cursor.fetchall()
            return results
        except Error as e:
            print(f"Error occured: {e}")
        

async def fetchconcurrently():
    all_users, older_users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    return all_users, older_users

print(asyncio.run(fetchconcurrently()))
