from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    plan: str
    created_at: datetime
    class Config:
        orm_mode = True
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Project Schemas
class ProjectCreate(BaseModel):
    name: str
    language: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    language: str
    description: Optional[str] = None
    created_at: datetime
    class Config:
        orm_mode = True
        from_attributes = True

# File Schemas
class FileCreate(BaseModel):
    filename: str
    content: str

class FileResponse(BaseModel):
    id: UUID
    project_id: UUID
    filename: str
    content: str
    class Config:
        orm_mode = True
        from_attributes = True
