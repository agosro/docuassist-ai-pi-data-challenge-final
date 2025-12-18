# Inicializar la base de datos creando todas las tablas definidas en los modelos
from app.db.session import engine
from app.db.base import Base
from app.models.history_model import History


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
