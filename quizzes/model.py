from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class CompletedQuizz(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quizz_id: str
    quizz_name: str
    username: str
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    answers: str
    score: int
    max_score: int
    message: str