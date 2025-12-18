from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.schemas.response import ChatResponse
from app.services.chat_service import ChatService
from app.metadata.model_inference import infer_model_from_question
from app.metadata.filter_resolution import merge_filters
from app.guardrails.pre_llm import detect_forbidden_intent



router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

chat_service = ChatService()

# ------------------ ROUTER DE CHAT ------------------ #
@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Endpoint de chat.
    Recibe la pregunta + filtros y delega la lógica al ChatService.
    """

    # PRE-LLM GUARDRAIL
    reason = detect_forbidden_intent(request.question)
    if reason:
        return ChatResponse(
            answer="La consulta no puede ser respondida porque viola las reglas de uso de la documentación.",
            sources=[],
            images=[],
            used_rag=False
        )
    
    # --- DEBUG LOGGING -----
    print("\n" + "="*50)
    print(">>> DEBUG: DATOS RECIBIDOS EN EL ROUTER")
    print(f"REQUEST COMPLETO: {request.model_dump()}")
    print(f"VALOR DE SISTEMA: '{request.sistema}'")
    print("="*50 + "\n")
    # -------------------

    # 1. Filtros explícitos (frontend)
    explicit_filters = {
        "categoria_equipo": request.categoria_equipo,
        "tipo_documentacion": request.tipo_documentacion,
        "sistema": request.sistema,
        "subtipo": request.subtipo,
        "marca": request.marca,
        "modelo": request.modelo
    }

    # 2. Inferencia controlada desde la pregunta
    inferred_filters = infer_model_from_question(request.question)

    # 3. Merge (frontend tiene prioridad)
    final_filters = merge_filters(explicit_filters, inferred_filters)

    print(">>> FILTROS EXPLÍCITOS:", explicit_filters)
    print(">>> FILTROS INFERIDOS:", inferred_filters)
    print(">>> FILTROS FINALES:", final_filters)

    # 4. Llamada al servicio con filtros RESUELTOS
    result = chat_service.handle_question(
        question=request.question,
        filters=final_filters
    )

    # 5. Respuesta
    return ChatResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        images=result.get("images", []),
        used_rag=result.get("used_rag", False)
    )