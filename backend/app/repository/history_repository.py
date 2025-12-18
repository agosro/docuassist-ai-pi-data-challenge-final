from sqlalchemy.orm import Session
from app.models.history_model import History
from typing import Optional

class HistoryRepository:

    def save(
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
        record = History(
            question=question,
            answer=answer,
            tipo_documentacion=tipo_documentacion,
            sistema=sistema,
            subtipo=subtipo,
            marca=marca,
            modelo=modelo
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def get_last(self, db: Session, limit: int = 10):
        return (
            db.query(History)
            .order_by(History.created_at.desc())
            .limit(limit)
            .all()
        )
