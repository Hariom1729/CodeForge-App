import asyncio
from database import engine, Base
import models

async def wipe_and_recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("Database wiped and schema recreated successfully!")

if __name__ == "__main__":
    asyncio.run(wipe_and_recreate())
