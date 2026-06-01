import asyncio
import pandas as pd
from database import AsyncSessionLocal, engine, Base
from models import Problem
import re

def to_camel_case(s):
    s = re.sub(r'[^a-zA-Z0-9 ]', '', s)
    parts = s.split()
    if not parts:
        return "solve"
    return parts[0].lower() + ''.join(x.capitalize() for x in parts[1:])

async def import_problems():
    # Ensure tables are created (we will drop the table first)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    print("Reading Excel file...")
    df = pd.read_excel('/Users/mac2/Downloads/FINAL450.xlsx', skiprows=4)
    
    if len(df.columns) < 2:
        print("Excel format unexpected!")
        return
        
    df.columns = ['Topic', 'ProblemName'] + list(df.columns[2:])
    df = df.dropna(subset=['ProblemName'])
    df['Topic'] = df['Topic'].ffill()
    
    async with AsyncSessionLocal() as session:
        problems_to_add = []
        for index, row in df.iterrows():
            topic = str(row['Topic']).strip()
            title = str(row['ProblemName']).strip()
            difficulty = "Medium"
            
            func_name = to_camel_case(title)
            if len(func_name) > 30:
                func_name = func_name[:30] # Keep it reasonable
                
            starter_code = {
                'cpp': f'class Solution {{\npublic:\n    void {func_name}() {{\n        // Write your logic here\n    }}\n}};',
                'python': f'class Solution:\n    def {func_name}(self):\n        pass',
                'go': f'func {func_name}() {{\n    \n}}',
                'rust': f'impl Solution {{\n    pub fn {func_name}() {{\n        \n    }}\n}}'
            }
            
            examples = [
                {
                    "input": "Example Input 1",
                    "output": "Example Output 1",
                    "explanation": "This is a generic mock explanation for example 1."
                },
                {
                    "input": "Example Input 2",
                    "output": "Example Output 2",
                    "explanation": "This is a generic mock explanation for example 2."
                }
            ]
            
            constraints = [
                "1 <= N <= 10^5",
                "0 <= arr[i] <= 10^9"
            ]
            
            test_cases = [
                {"input": "1\n2\n", "expected_output": "3\n"}
            ]
            
            p = Problem(
                topic=topic,
                title=title,
                difficulty=difficulty,
                description=f"### {title}\n\nThis is a classic problem from the **{topic}** topic.\n\nWrite an efficient algorithm to solve this problem.",
                likes=0,
                dislikes=0,
                examples=examples,
                constraints=constraints,
                time_limit_ms=2000,
                test_cases=test_cases,
                starter_code=starter_code
            )
            problems_to_add.append(p)
            
        session.add_all(problems_to_add)
        await session.commit()
        
    print(f"Successfully generated and imported {len(problems_to_add)} problems with mock data.")

if __name__ == "__main__":
    asyncio.run(import_problems())
