from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid

from database import get_db
import models
from auth import get_current_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

class TestCaseCreate(BaseModel):
    input: str
    expected_output: str
    is_hidden: bool = False

class ProblemBulkImport(BaseModel):
    title: str
    topic: str
    difficulty: str
    description: str
    constraints: List[str]
    time_limit_ms: int = 2000
    memory_limit_mb: int = 256
    examples: List[Dict[str, str]]
    starter_code: Dict[str, str]
    visible_test_cases: List[TestCaseCreate]
    hidden_test_cases: List[TestCaseCreate]

class BulkImportRequest(BaseModel):
    problems: List[ProblemBulkImport]

@router.post("/bulk-import")
async def bulk_import_problems(
    req: BulkImportRequest,
    # current_user: models.User = Depends(get_current_user), # In a real app, verify admin role
    db: AsyncSession = Depends(get_db)
):
    try:
        created_count = 0
        for p_data in req.problems:
            new_prob = models.Problem(
                title=p_data.title,
                topic=p_data.topic,
                difficulty=p_data.difficulty,
                description=p_data.description,
                constraints=p_data.constraints,
                examples=p_data.examples,
                time_limit_ms=p_data.time_limit_ms,
                memory_limit_mb=p_data.memory_limit_mb,
                starter_code=p_data.starter_code
            )
            db.add(new_prob)
            await db.flush() # get the ID

            # Add visible test cases
            for tc in p_data.visible_test_cases:
                db_tc = models.TestCase(
                    problem_id=new_prob.id,
                    input=tc.input,
                    expected_output=tc.expected_output,
                    is_hidden=False
                )
                db.add(db_tc)
                
            # Add hidden test cases
            for tc in p_data.hidden_test_cases:
                db_tc = models.TestCase(
                    problem_id=new_prob.id,
                    input=tc.input,
                    expected_output=tc.expected_output,
                    is_hidden=True
                )
                db.add(db_tc)
            
            created_count += 1

        await db.commit()
        return {"status": "success", "message": f"Successfully imported {created_count} problems."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
