from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

@router.post("/", response_model=schemas.ProjectResponse)
async def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    db_project = models.Project(
        user_id=current_user.id,
        name=project.name,
        language=project.language,
        description=project.description
    )
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[schemas.ProjectResponse])
async def read_projects(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(models.Project).where(models.Project.user_id == current_user.id)
    result = await db.execute(stmt)
    projects = result.scalars().all()
    return projects

@router.get("/{project_id}", response_model=schemas.ProjectResponse)
async def read_project(
    project_id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(models.Project).where(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    )
    result = await db.execute(stmt)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(models.Project).where(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    )
    result = await db.execute(stmt)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.delete(project)
    await db.commit()
    return None
