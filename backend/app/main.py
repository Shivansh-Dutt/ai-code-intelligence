from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

app = FastAPI(
    title="AI Code Intelligence API",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
async def database_health_check() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"status": "ok"}