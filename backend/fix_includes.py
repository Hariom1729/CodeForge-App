import asyncio
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Problem
import json

async def fix():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Problem))
        problems = result.scalars().all()
        for p in problems:
            sc = p.starter_code
            if "cpp" in sc:
                cpp_code = sc["cpp"]
                if "#include <algorithm>" not in cpp_code:
                    cpp_code = "#include <algorithm>\n" + cpp_code
                    sc["cpp"] = cpp_code
                    p.starter_code = dict(sc) # trigger SQLAlchemy update
        await session.commit()
        print("Updated starter code for all problems.")

if __name__ == "__main__":
    asyncio.run(fix())
