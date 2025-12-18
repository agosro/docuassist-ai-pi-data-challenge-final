from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.db.base import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Metadata fields
    tipo_documentacion = Column(String, nullable=True)
    sistema = Column(String, nullable=True)
    subtipo = Column(String, nullable=True)
    marca = Column(String, nullable=True)
    modelo = Column(String, nullable=True)
