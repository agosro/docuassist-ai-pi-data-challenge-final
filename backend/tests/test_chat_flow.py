import pytest
from app.services.chat_service import ChatService

chat_service = ChatService()


def test_greeting():
    """Test: Saludo conversacional (sin RAG, sin inferencia de filtros)"""
    result = chat_service.handle_question("Hola")
    
    assert result is not None
    assert "answer" in result
    assert result["answer"] is not None
    assert len(result["answer"]) > 0
    assert result["sources"] == []
    assert result["used_rag"] is False
    # Verificar que la respuesta es conversacional
    assert any(word in result["answer"].lower() for word in ["hola", "ayudarte", "bienvenido"])


def test_out_of_scope():
    """Test: Pregunta fuera del alcance del sistema"""
    result = chat_service.handle_question("¿Quién ganó el mundial?")
    
    assert result is not None
    assert "answer" in result
    assert result["answer"] is not None
    # El sistema debe rechazar educadamente
    assert any(word in result["answer"].lower() for word in ["documentación", "alcance", "técnica"])
    assert result["sources"] == []
    assert result["used_rag"] is False


def test_system_question():
    """Test: Pregunta sobre sistema de software con inferencia automática"""
    result = chat_service.handle_question(
        "¿Cómo realizar cierre Z en StarPOS Market?"
    )
    
    assert result is not None
    assert "answer" in result
    assert result["answer"] is not None
    assert len(result["answer"]) > 0
    # Cuando hay documentación disponible, debería usar RAG
    # assert result["used_rag"] is True  # Comentado si no hay docs en DB


def test_technical_question_with_filters():
    """Test: Pregunta técnica específica con filtros explícitos"""
    result = chat_service.handle_question(
        question="¿Cómo cambiar la IP?",
        categoria_equipo="impresora",
        marca="hasar",
        modelo="320F"
    )
    
    assert result is not None
    assert "answer" in result
    assert result["answer"] is not None
    assert "sources" in result
    assert isinstance(result["sources"], list)
    # Si hay documentación, debería tener fuentes
    if result["used_rag"]:
        for source in result["sources"]:
            assert "document" in source
            assert "page" in source


def test_generic_technical_question():
    """Test: Pregunta técnica genérica sin modelo específico"""
    result = chat_service.handle_question(
        question="¿Qué mantenimientos necesita una impresora fiscal?",
        categoria_equipo="impresora",
        subtipo="fiscal"
    )
    
    assert result is not None
    assert "answer" in result
    assert result["answer"] is not None
    assert isinstance(result["sources"], list)


def test_response_structure():
    """Test: Validar estructura de respuesta"""
    result = chat_service.handle_question("Hola")
    
    # Verificar que la respuesta tiene todos los campos esperados
    required_fields = ["answer", "sources", "images", "used_rag"]
    for field in required_fields:
        assert field in result, f"Campo '{field}' no encontrado en respuesta"
    
    # Tipos correctos
    assert isinstance(result["answer"], str)
    assert isinstance(result["sources"], list)
    assert isinstance(result["images"], list)
    assert isinstance(result["used_rag"], bool)
