from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.chat_router import router as chat_router
from app.api.routes.history_router import router as history_router
from app.db.init_db import init_db


# Crear instancia de FastAPI
app = FastAPI(
    title="DocuAssist AI",
    description="Asistente inteligente de documentación interna basado en RAG",
    version="0.1.0",
)

# Inicializar base de datos
@app.on_event("startup")
def startup_event():
    init_db()

# CORS (frontend futuro o pruebas locales)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod se restringe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar y registrar rutas
app.include_router(chat_router)
app.include_router(history_router)

# Endpoint de salud 
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "DocuAssist AI"
    }
