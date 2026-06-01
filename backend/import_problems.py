import asyncio
import pandas as pd
from database import AsyncSessionLocal, engine, Base
from models import Problem

async def import_problems():
    # Ensure tables are created
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # Read the file
    print("Reading Excel file...")
    df = pd.read_excel('/Users/mac2/Downloads/FINAL450.xlsx', skiprows=4)
    
    # Ensure it has enough columns
    if len(df.columns) < 2:
        print("Excel format unexpected!")
        return
        
    # the columns are something like ['Unnamed: 0', 'Unnamed: 1', '<->']
    df.columns = ['Topic', 'ProblemName'] + list(df.columns[2:])
    
    # drop rows where ProblemName is NaN or unhelpful
    df = df.dropna(subset=['ProblemName'])
    
    # In Love Babbar's sheet, topics span multiple rows but only show in the first row.
    # We should forward-fill the Topic column
    df['Topic'] = df['Topic'].ffill()
    
    async with AsyncSessionLocal() as session:
        # Clear existing problems for idempotency
        await session.execute(Problem.__table__.delete())
        
        problems_to_add = []
        for index, row in df.iterrows():
            topic = str(row['Topic']).strip()
            title = str(row['ProblemName']).strip()
            
            # Simple heuristic for difficulty (all Medium for now since sheet doesn't say)
            difficulty = "Medium"
            
            p = Problem(
                topic=topic,
                title=title,
                difficulty=difficulty,
                description=f"### {title}\n\nThis is a classic problem from the **{topic}** topic.\n\nWrite an efficient algorithm to solve this problem.\n\n#### Examples:\n\n*Examples are currently unavailable. Consider the standard edge cases.*",
                likes=0,
                dislikes=0
            )
            problems_to_add.append(p)
            
        session.add_all(problems_to_add)
        await session.commit()
        
    print(f"Successfully imported {len(problems_to_add)} problems.")

if __name__ == "__main__":
    asyncio.run(import_problems())
