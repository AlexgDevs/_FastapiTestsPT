from server import db_manager
import asyncio

async def main():
    await db_manager.drop()
    await db_manager.up()

asyncio.run(main())