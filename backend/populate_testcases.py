import asyncio
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Problem

async def populate_testcases():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Problem))
        problems = result.scalars().all()
        
        for problem in problems:
            if problem.title == "Reverse the array":
                # Already explicitly set up earlier, keep it
                continue
                
            test_cases = []
            if problem.examples:
                for ex in problem.examples:
                    test_cases.append({
                        "input": ex.get("input", ""),
                        "expected_output": ex.get("output", "Executed successfully!")
                    })
            else:
                test_cases.append({
                    "input": "Generic input",
                    "expected_output": "Executed successfully!"
                })
                
            problem.test_cases = test_cases
                
        await session.commit()
        print(f"Successfully populated test_cases for {len(problems)} problems!")

if __name__ == "__main__":
    asyncio.run(populate_testcases())
