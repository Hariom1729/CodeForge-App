import asyncio
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Problem

def get_examples_for_topic(topic: str):
    topic = str(topic).lower()
    
    if "array" in topic or "two pointers" in topic or "sliding window" in topic:
        return [
            {
                "input": "arr = [1, 2, 3, 4, 5], n = 5",
                "output": "Depends on the specific problem logic",
                "explanation": "This is a sample array input."
            },
            {
                "input": "arr = [7, 1, 5, 3, 6, 4], n = 6",
                "output": "Depends on the specific problem logic",
                "explanation": "Another sample array input to test edge cases."
            }
        ]
    elif "string" in topic:
        return [
            {
                "input": "s = \"codeforge\"",
                "output": "Depends on the specific problem logic",
                "explanation": "A sample string input."
            }
        ]
    elif "math" in topic or "bit manipulation" in topic:
        return [
            {
                "input": "n = 10",
                "output": "Depends on the specific problem logic",
                "explanation": "A standard integer input."
            }
        ]
    elif "tree" in topic or "graph" in topic:
        return [
            {
                "input": "nodes = [1, 2, 3], edges = [[1, 2], [1, 3]]",
                "output": "Depends on the specific problem logic",
                "explanation": "A simple graph/tree structure representation."
            }
        ]
    else:
        return [
            {
                "input": "Standard input variables",
                "output": "Expected valid output",
                "explanation": "Review the problem description for exact logic."
            }
        ]

async def add_examples():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Problem))
        problems = result.scalars().all()
        
        for problem in problems:
            # specifically for "Reverse the array" we can set an exact one
            if problem.title == "Reverse the array":
                problem.examples = [
                    {
                        "input": "arr = [1, 2, 3], n = 3",
                        "output": "3 2 1",
                        "explanation": "The array is reversed such that the last element becomes the first."
                    },
                    {
                        "input": "arr = [4, 5], n = 2",
                        "output": "5 4",
                        "explanation": "Simple two element array reversed."
                    }
                ]
            else:
                problem.examples = get_examples_for_topic(problem.topic)
                
        await session.commit()
        print(f"Successfully added custom examples to {len(problems)} problems based on their topic!")

if __name__ == "__main__":
    asyncio.run(add_examples())
