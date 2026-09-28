from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.ingestion import router as ingestion_router
from app.api.repositories import router as repositories_router
from app.api.repository_chunks import (
    router as repository_chunks_router,
)
from app.api.repository_files import router as repositories_files_router
from app.api.search import router as search_router
from app.api.qa import router as qa_router
from app.db.session import engine

app = FastAPI(
    title="AI Code Intelligence API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repositories_router)
app.include_router(ingestion_router)
app.include_router(repositories_files_router)
app.include_router(repository_chunks_router)
app.include_router(search_router)
app.include_router(qa_router)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
async def database_health_check() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "ok"}