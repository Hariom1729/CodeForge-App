import asyncio
from database import AsyncSessionLocal
import models
from seed_judge import SEED_DATA

async def seed_direct():
    async with AsyncSessionLocal() as db:
        created_count = 0
        for p_data in SEED_DATA["problems"]:
            new_prob = models.Problem(
                title=p_data["title"],
                topic=p_data["topic"],
                difficulty=p_data["difficulty"],
                description=p_data["description"],
                constraints=p_data["constraints"],
                examples=p_data["examples"],
                time_limit_ms=p_data["time_limit_ms"],
                memory_limit_mb=p_data["memory_limit_mb"],
                starter_code=p_data["starter_code"]
            )
            db.add(new_prob)
            await db.flush() # get the ID

            # Add visible test cases
            for tc in p_data["visible_test_cases"]:
                db_tc = models.TestCase(
                    problem_id=new_prob.id,
                    input=tc["input"],
                    expected_output=tc["expected_output"],
                    is_hidden=False
                )
                db.add(db_tc)
                
            # Add hidden test cases
            for tc in p_data["hidden_test_cases"]:
                db_tc = models.TestCase(
                    problem_id=new_prob.id,
                    input=tc["input"],
                    expected_output=tc["expected_output"],
                    is_hidden=True
                )
                db.add(db_tc)
            
            created_count += 1

        await db.commit()
        print(f"Successfully imported {created_count} problems directly.")

if __name__ == "__main__":
    asyncio.run(seed_direct())
