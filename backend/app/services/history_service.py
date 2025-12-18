from sqlalchemy.orm import Session
from app.repository.history_repository import HistoryRepository
from typing import Optional

class HistoryService:

    def __init__(self):
        self.repo = HistoryRepository()

    def save_interaction(
        self, 
        db: Session, 
        question: str, 
        answer: str,
        tipo_documentacion: Optional[str] = None,
        sistema: Optional[str] = None,
        subtipo: Optional[str] = None,
        marca: Optional[str] = None,
        modelo: Optional[str] = None
    ):
        return self.repo.save(
            db, 
            question, 
            answer,
            tipo_documentacion=tipo_documentacion,
            sistema=sistema,
            subtipo=subtipo,
            marca=marca,
            modelo=modelo
        )

    def get_recent(self, db: Session, limit: int = 10):
        return self.repo.get_last(db, limit)
