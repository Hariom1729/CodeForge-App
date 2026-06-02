from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid

from database import get_db
import models, schemas
from auth import get_current_user
from execution_manager import execution_manager
from fastapi import Header

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
    time_limit_ms = 2000
    memory_limit_mb = 256
    
    if req.problem_id:
        prob_res = await db.execute(select(models.Problem).filter(models.Problem.id == req.problem_id))
        problem = prob_res.scalars().first()
        if problem:
            time_limit_ms = problem.time_limit_ms
            memory_limit_mb = problem.memory_limit_mb
            
            tc_query = select(models.TestCase).filter(models.TestCase.problem_id == req.problem_id)
            if req.action == "run":
                tc_query = tc_query.filter(models.TestCase.is_hidden == False)
            
            tc_res = await db.execute(tc_query)
            test_cases = [
                {"input": tc.input, "expected_output": tc.expected_output, "is_hidden": tc.is_hidden}
                for tc in tc_res.scalars().all()
            ]

    result = await execution_manager.execute_code(req.language, req.code, test_cases, time_limit_ms, memory_limit_mb)

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

@router.post("/external", response_model=ExecutionResponse)
async def execute_code_external(
    req: ExecutionRequest,
    x_api_key: str = Header(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Dedicated endpoint for external projects (like Axiora) to execute code.
    Secured by a static API Key.
    """
    # Replace this with a secure key or load from config/env
    VALID_API_KEY = "axiora_secret_live_key_2026"
    
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
        
    time_limit_ms = 2000
    memory_limit_mb = 256
    
    result = await execution_manager.execute_code(
        req.language, 
        req.code, 
        [], 
        time_limit_ms, 
        memory_limit_mb
    )

    # Optional: Log the execution without a user_id for analytics
    db_execution = models.Execution(
        user_id=None,
        project_id=None,
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
        status=result["status"]
    )

