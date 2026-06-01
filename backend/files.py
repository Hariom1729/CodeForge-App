from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(prefix="/api/v1/projects/{project_id}/files", tags=["files"])

async def verify_project_ownership(project_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession):
    stmt = select(models.Project).where(
        models.Project.id == project_id,
        models.Project.user_id == user_id
    )
    result = await db.execute(stmt)
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found or unauthorized")

@router.post("/", response_model=schemas.FileResponse)
async def create_file(
    project_id: uuid.UUID,
    file: schemas.FileCreate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await verify_project_ownership(project_id, current_user.id, db)
    
    db_file = models.File(
        project_id=project_id,
        filename=file.filename,
        content=file.content
    )
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file

@router.get("/", response_model=List[schemas.FileResponse])
async def read_files(
    project_id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await verify_project_ownership(project_id, current_user.id, db)
    
    stmt = select(models.File).where(models.File.project_id == project_id)
    result = await db.execute(stmt)
    files = result.scalars().all()
    return files

@router.put("/{file_id}", response_model=schemas.FileResponse)
async def update_file(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    file_update: schemas.FileCreate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await verify_project_ownership(project_id, current_user.id, db)
    
    stmt = select(models.File).where(
        models.File.id == file_id,
        models.File.project_id == project_id
    )
    result = await db.execute(stmt)
    db_file = result.scalars().first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
        
    db_file.filename = file_update.filename
    db_file.content = file_update.content
    await db.commit()
    await db.refresh(db_file)
    return db_file

@router.delete("/{file_id}", status_code=204)
async def delete_file(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await verify_project_ownership(project_id, current_user.id, db)
    
    stmt = select(models.File).where(
        models.File.id == file_id,
        models.File.project_id == project_id
    )
    result = await db.execute(stmt)
    db_file = result.scalars().first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
        
    await db.delete(db_file)
    await db.commit()
    return None
