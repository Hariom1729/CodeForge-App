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

class ExecutionResponse(BaseModel):
    output: str
    execution_time: float
    status: str

@router.post("/", response_model=ExecutionResponse)
async def execute_code(
    req: ExecutionRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Enforce user limits here if necessary (e.g. check plan limits)

    result = await execution_manager.execute_code(req.language, req.code)

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
        status=result["status"]
    )
