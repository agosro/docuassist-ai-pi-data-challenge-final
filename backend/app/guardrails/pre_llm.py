def detect_forbidden_intent(question: str) -> str | None:
    q = question.lower()

    forbidden_patterns = [
        "ignora", "ignorá",
        "evadir",
        "respondé en inglés",
        "respond in english",
        "emojis",
        "mezclá",
        "mezcla",
        "usa conocimiento general",
        "aunque no esté en el manual"
    ]

    for pattern in forbidden_patterns:
        if pattern in q:
            return "La consulta viola las reglas de uso de la documentación."

    return None
