import asyncio
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Problem, TestCase

async def populate_testcases():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Problem))
        problems = result.scalars().all()
        
        for problem in problems:
            if problem.examples:
                for ex in problem.examples:
                    # visible case
                    session.add(TestCase(
                        problem_id=problem.id,
                        input=ex.get("input", ""),
                        expected_output=ex.get("output", "Executed successfully!"),
                        is_hidden=False
                    ))
                    # hidden case (dummy)
                    session.add(TestCase(
                        problem_id=problem.id,
                        input="Hidden " + ex.get("input", ""),
                        expected_output=ex.get("output", "Executed successfully!"),
                        is_hidden=True
                    ))
            else:
                session.add(TestCase(
                    problem_id=problem.id,
                    input="Generic input",
                    expected_output="Executed successfully!",
                    is_hidden=False
                ))
                session.add(TestCase(
                    problem_id=problem.id,
                    input="Hidden Generic input",
                    expected_output="Executed successfully!",
                    is_hidden=True
                ))
                
        await session.commit()
        print(f"Successfully populated test_cases for {len(problems)} problems!")

if __name__ == "__main__":
    asyncio.run(populate_testcases())
