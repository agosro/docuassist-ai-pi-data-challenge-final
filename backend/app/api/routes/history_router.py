from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.history_service import HistoryService

# ------------------ ROUTER DE HISTORIAL ------------------ #
router = APIRouter(prefix="/history", tags=["History"])

history_service = HistoryService()

# Endpoint para obtener el historial de interacciones
@router.get("/")
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    return history_service.get_recent(db, limit)
