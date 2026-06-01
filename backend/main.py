from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models

app = FastAPI(title="CodeForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # For development, we create tables directly
        # In production, use Alembic
        await conn.run_sync(Base.metadata.create_all)

import auth, projects, files, execution_router, problems
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(files.router)
app.include_router(execution_router.router)
app.include_router(problems.router)

@app.get("/")
async def root():
    return {"message": "Welcome to CodeForge API"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}
