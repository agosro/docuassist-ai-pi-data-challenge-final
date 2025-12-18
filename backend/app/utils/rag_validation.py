def filter_chunks_by_model(chunks: list, modelo: str) -> list:
    """Filtra chunks que coincidan estrictamente con el modelo de hardware."""
    return [
        c for c in chunks
        if c.get("metadata", {}).get("modelo") == modelo
    ]

def filter_chunks_by_system(chunks: list, sistema: str) -> list:
    """
    Filtra chunks que pertenezcan al sistema/software solicitado.
    Verifica si el metadato 'sistema' coincide O si el nombre del archivo contiene el sistema.
    """
    return [
        c for c in chunks
        if c.get("metadata", {}).get("sistema") == sistema
        or sistema in c.get("metadata", {}).get("document", "")
    ]

def validate_single_model(chunks: list, modelo: str) -> bool:
    """Verifica que todos los chunks pertenezcan al mismo modelo."""
    modelos = {
        c.get("metadata", {}).get("modelo")
        for c in chunks
    }
    # Debe haber 1 solo modelo y debe ser el solicitado
    return modelos == {modelo}

def validate_single_system(chunks: list, sistema: str) -> bool:
    """Verifica que, tras el filtrado, no hayan quedado sistemas mezclados."""
    if not chunks:
        return False
        
    # Recolectamos los sistemas encontrados en los chunks
    sistemas_encontrados = set()
    for c in chunks:
        meta = c.get("metadata", {})
        # Prioriza el campo 'sistema', si no existe usa el nombre del documento
        nombre_identificador = meta.get("sistema") or meta.get("document", "")
        sistemas_encontrados.add(nombre_identificador)

    # Verificamos que el sistema solicitado esté presente en todos los identificadores hallados
    return all(sistema in str(s) for s in sistemas_encontrados)