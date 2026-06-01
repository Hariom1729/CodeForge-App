import asyncio
from sqlalchemy.future import select
from sqlalchemy import update
from database import AsyncSessionLocal
from models import Problem

async def clear_examples():
    async with AsyncSessionLocal() as session:
        # Update all problems to have an empty examples array
        await session.execute(
            update(Problem).values(examples=[])
        )
        await session.commit()
        print("Successfully cleared all generic examples from the database!")

if __name__ == "__main__":
    asyncio.run(clear_examples())
