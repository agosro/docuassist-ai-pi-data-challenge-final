from app.graph.state import ChatState
from app.rag.retriever import Retriever
from app.rag.reranker import Reranker
from app.rag.generator import Generator
from app.rag.query_rewriter import build_retrieval_query
from app.utils.rag_validation import (
    filter_chunks_by_model,
    validate_single_model,
    filter_chunks_by_system
)
from app.metadata.infer_filters import infer_filters_from_question

retriever = Retriever()
reranker = Reranker()
generator = Generator()


def retrieve_with_fallback(retriever, query, filters, is_system_doc, has_model_filters):
    # Si hay modelo explícito, búsqueda estricta y corta
    if has_model_filters:
        return retriever.retrieve(
            query=query,
            filters=filters,
            top_k=15
        )

    # Caso normal (sin modelo)
    chunks = retriever.retrieve(
        query=query,
        filters=filters,
        top_k=10
    )

    # Si es doc de sistema y trajo poco, intentar ampliar
    if is_system_doc and (not chunks or len(chunks) < 5):
        chunks = retriever.retrieve(
            query=query,
            filters=filters,
            top_k=30
        )

    return chunks


def documentation_node(state: ChatState) -> ChatState:
    question = state["question"]
    explicit_filters = state.get("filters", {})

    # INFERIR filtros desde la pregunta (solo si falta info)
    inferred_filters = infer_filters_from_question(question)

    # MERGE: filtros explícitos del frontend tienen prioridad
    filters = {
        **inferred_filters,
        **explicit_filters
    }

    # Calcular is_generic
    is_generic = (
        filters.get("tipo_documentacion") == "tecnica"
        and "categoria_equipo" in filters
        and "marca" not in filters
        and "modelo" not in filters
    )

    tipo_doc = filters.get("tipo_documentacion")
    is_system_doc = tipo_doc == "sistema"
    
    # Extraer el sistema específico si existe
    sistema_target = filters.get("sistema")

    marca = filters.get("marca")
    modelo = filters.get("modelo")

    has_model_filters = bool(modelo)

    is_generic = not has_model_filters and not sistema_target

    # Retrieve (con query rewriting)
    # Regla: filtros explícitos pisan la semántica
    if has_model_filters:
        retrieval_query = f"{question} {marca or ''} {modelo}"
    elif is_system_doc and sistema_target:
        # Si es sistema, forzar el nombre del sistema en la query
        retrieval_query = f"{question} {sistema_target}"
    else:
        retrieval_query = build_retrieval_query(
            question=question,
            is_system_doc=is_system_doc
        )

    retrieved_chunks = retrieve_with_fallback(
        retriever=retriever,
        query=retrieval_query,
        filters=filters,
        is_system_doc=is_system_doc,
        has_model_filters=has_model_filters
    )

    # ---------------------------------------------------------
    # FILTRADO ESTRICTO (HARDWARE Y SOFTWARE)
    # ---------------------------------------------------------

    # CASO 1: Modelo explícito (Hardware)
    if has_model_filters:
        retrieved_chunks = filter_chunks_by_model(
            retrieved_chunks,
            modelo
        )

        if not retrieved_chunks:
            return {
                **state,
                "answer": "La documentación disponible no contiene información sobre este tema para el modelo consultado.",
                "sources": [],
                "images": [],
                "used_rag": True,
                "filters": filters,
                "is_generic": is_generic
            }

        if not validate_single_model(retrieved_chunks, modelo):
            return {
                **state,
                "answer": "No es posible responder de forma segura con la documentación disponible para el modelo seleccionado.",
                "sources": [],
                "images": [],
                "used_rag": True,
                "filters": filters,
                "is_generic": is_generic
            }

    # CASO 2: Sistema explícito (Software)
    elif is_system_doc and sistema_target:
        retrieved_chunks = filter_chunks_by_system(
            retrieved_chunks, 
            sistema_target
        )

        if not retrieved_chunks:
            return {
                **state,
                "answer": f"La documentación del sistema '{sistema_target}' no contiene información sobre este procedimiento.",
                "sources": [],
                "images": [],
                "used_rag": True,
                "filters": filters,
                "is_generic": is_generic
            }

    # ---------------------------------------------------------

    # Caso 3: Inferencia automática SEGURA
    # Solo inferimos si NO hay filtros previos y NO es un sistema
    if not has_model_filters and not sistema_target and retrieved_chunks and not is_system_doc and not is_generic:
        
        # Analizamos los modelos de los primeros 5 resultados
        top_chunks = retrieved_chunks[:5]
        found_models = {
            c.get("metadata", {}).get("modelo") 
            for c in top_chunks 
            if c.get("metadata", {}).get("modelo")
        }

        # LOGICA DE SEGURIDAD PARA PREGUNTAS GENÉRICAS:
        # Solo aplicamos inferencia si encontramos EXACTAMENTE UN modelo único.
        # Si hay >1 (mezcla de manuales), NO filtramos. Dejamos pasar todo.
        if len(found_models) == 1:
            inferred_model = list(found_models)[0]
            
            # Recuperamos marca del mismo chunk
            first_match = next(c for c in top_chunks if c.get("metadata", {}).get("modelo") == inferred_model)
            inferred_brand = first_match.get("metadata", {}).get("marca")

            # Aplicamos el filtro
            retrieved_chunks = filter_chunks_by_model(
                retrieved_chunks,
                inferred_model
            )

            modelo = modelo or inferred_model
            marca = marca or inferred_brand
            is_generic = False
        
        # Si len(found_models) > 1 (ambigüedad), pasamos de largo sin filtrar.
        # El generador recibirá contexto mixto y pedirá aclaración.

    # 🔁 Rerank
    reranked_chunks = reranker.rerank(
        query=question,
        documents=retrieved_chunks,
        top_n=5
    )

    # ---------------------------------------------------------
    # REFUERZO CRÍTICO POST-RERANK
    # ---------------------------------------------------------
    
    if modelo:
        # Filtrado final para hardware
        reranked_chunks = [
            c for c in reranked_chunks
            if c.get("metadata", {}).get("modelo") == modelo
        ]
    elif sistema_target:
        # Filtrado final para sistemas
        reranked_chunks = filter_chunks_by_system(reranked_chunks, sistema_target)

    # Verificación final de vacío tras rerank
    if not reranked_chunks:
        return {
            **state,
            "answer": "La documentación específica no detalla este procedimiento.",
            "sources": [],
            "images": [],
            "used_rag": True,
            "filters": filters,
            "is_generic": is_generic
        }

    # Generación
    result = generator.generate_answer(
        question=question,
        documents=reranked_chunks,
        is_generic=is_generic,
        marca=marca,
        modelo=modelo,
    )

    # Retornar con filtros finales para que el historial los pueda usar
    return {
        **state,
        "answer": result["answer"],
        "sources": result.get("sources", []),
        "images": result.get("images", []) or [],
        "used_rag": True,
        "filters": filters,  # Filtros finales después del merge
        "is_generic": is_generic
    }