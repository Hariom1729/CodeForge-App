from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid

from database import get_db
import models, schemas
from auth import get_current_user
from execution_manager import execution_manager

router = APIRouter(prefix="/api/v1/execute", tags=["execute"])

class ExecutionRequest(BaseModel):
    language: str
    code: str
    project_id: uuid.UUID | None = None
    problem_id: uuid.UUID | None = None
    action: str = "run"

class ExecutionResponse(BaseModel):
    output: str
    execution_time: float
    status: str
    test_results: list | None = None

@router.post("/", response_model=ExecutionResponse)
async def execute_code(
    req: ExecutionRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Enforce user limits here if necessary (e.g. check plan limits)
    
    test_cases = []
    if req.problem_id:
        prob_res = await db.execute(select(models.Problem).filter(models.Problem.id == req.problem_id))
        problem = prob_res.scalars().first()
        if problem and problem.test_cases:
            test_cases = problem.test_cases
            
            # If action is 'submit', simulate a massive test suite by duplicating the test cases to total 100+
            if req.action == "submit" and len(test_cases) > 0:
                multiplier = (105 // len(test_cases)) + 1
                test_cases = (test_cases * multiplier)[:105]

    result = await execution_manager.execute_code(req.language, req.code, test_cases)

    # Log the execution
    db_execution = models.Execution(
        user_id=current_user.id,
        project_id=req.project_id,
        language=req.language,
        execution_time=result["execution_time"],
        status=result["status"],
        output=result["output"]
    )
    db.add(db_execution)
    await db.commit()

    return ExecutionResponse(
        output=result["output"],
        execution_time=result["execution_time"],
        status=result["status"],
        test_results=result.get("test_results")
    )
