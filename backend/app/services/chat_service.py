from app.schemas.response import ChatResponse
from app.db.session import SessionLocal
from app.services.history_service import HistoryService
from app.graph.chat_graph import build_chat_graph


class ChatService:
    def __init__(self):
        self.graph = build_chat_graph()
        self.history_service = HistoryService()

    def handle_question(
        self,
        question: str,
        filters: dict
    ) -> ChatResponse:

        # ✅ Solo pasamos filtros explícitos del frontend
        # La inferencia se hará SOLO si intent=documentation
        explicit_filters = {k: v for k, v in filters.items() if v}

        state = {
            "question": question,
            "filters": explicit_filters,
            "is_generic": False,  # Se calculará en documentation_node
            "intent": None,
            "answer": None,
            "sources": []
        }

        result = self.graph.invoke(state)

        # Guardar historial con los filtros finales (después del merge)
        final_filters = result.get("filters", explicit_filters)
        
        db = SessionLocal()
        try:
            self.history_service.save_interaction(
                db,
                question=question,
                answer=result["answer"],
                tipo_documentacion=final_filters.get("tipo_documentacion"),
                sistema=final_filters.get("sistema"),
                subtipo=final_filters.get("subtipo"),
                marca=final_filters.get("marca"),
                modelo=final_filters.get("modelo")
            )
        finally:
            db.close()

        return result
