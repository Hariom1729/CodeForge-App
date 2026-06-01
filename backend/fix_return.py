import asyncio
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Problem

async def fix():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Problem).filter(Problem.title == "Two Sum"))
        problems = result.scalars().all()
        for p in problems:
            sc = p.starter_code
            if "cpp" in sc:
                cpp_code = sc["cpp"]
                if "return {};" not in cpp_code:
                    cpp_code = cpp_code.replace("vector<int> twoSum(vector<int>& nums, int target) {\n        \n    }", "vector<int> twoSum(vector<int>& nums, int target) {\n        return {};\n    }")
                    sc["cpp"] = cpp_code
                    p.starter_code = dict(sc)
        await session.commit()
        print("Updated return statement for Two Sum.")

if __name__ == "__main__":
    asyncio.run(fix())
