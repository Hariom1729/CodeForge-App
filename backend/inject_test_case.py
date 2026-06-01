import asyncio
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Problem

async def inject():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Problem).filter(Problem.title == "Reverse the array"))
        problem = result.scalars().first()
        if problem:
            problem.test_cases = [
                {"input": "arr = [1, 2, 3], n = 3", "expected_output": "Executed successfully!"},
                {"input": "arr = [4, 5], n = 2", "expected_output": "Executed successfully!"}
            ]
            await session.commit()
            print("Successfully injected test cases for 'Reverse the array'!")
        else:
            print("Problem not found.")

if __name__ == "__main__":
    asyncio.run(inject())
