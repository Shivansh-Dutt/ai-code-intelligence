from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.code_qa_service import (
    answer_code_question
)

router = APIRouter(
    prefix="/api",
    tags=["qa"]
)

class CodeQuestion(BaseModel):
    question: str
    limit: int = 8
    
@router.post(
    "/repositories/{repository_id}/ask",
)

def ask_repository(
    repository_id: UUID,
    request: CodeQuestion,
    db: Session = Depends(get_db),
):
    res = answer_code_question(
        db = db,
        repository_id= repository_id,
        question=request.question,
        limit=min(request.limit, 20),
    )
    
    return {
        "answer": res.answer,
        "sources": res.sources
    }
    