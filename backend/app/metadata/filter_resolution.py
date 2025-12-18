def merge_filters(explicit: dict, inferred: dict) -> dict:
    """
    Los filtros explícitos (frontend) tienen prioridad absoluta.
    Solo se completan los None con valores inferidos.
    """
    result = explicit.copy()

    for key, value in inferred.items():
        if not result.get(key):
            result[key] = value

    return result
