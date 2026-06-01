from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from pydantic import BaseModel
import uuid
from typing import List, Optional

from database import get_db
from models import Problem

router = APIRouter(prefix="/api/v1/problems", tags=["problems"])

class ProblemListResponse(BaseModel):
    id: uuid.UUID
    topic: str
    title: str
    difficulty: str
    likes: int
    dislikes: int

class ProblemDetailResponse(ProblemListResponse):
    description: str
    examples: list
    constraints: list
    time_limit_ms: int
    starter_code: dict

@router.get("", response_model=List[ProblemListResponse])
async def list_problems(skip: int = 0, limit: int = 1000, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Problem).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{problem_id}", response_model=ProblemDetailResponse)
async def get_problem(problem_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Problem).filter(Problem.id == problem_id))
    problem = result.scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem
