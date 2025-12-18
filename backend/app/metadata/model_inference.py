import re
from typing import Dict
from app.metadata.infer_filters import infer_filters_from_question


MODEL_ALIASES = {
    "smhpt250f": {
        "marca": "hasar",
        "modelo": "Impresora_fiscal_Hasar_SMH-PT-250F",
        "categoria_equipo": "impresora",
        "subtipo": "fiscal"
    },
    "smhp441f": {
        "marca": "hasar",
        "modelo": "Impresora_fiscal_Hasar_SMH-P-441F",
        "categoria_equipo": "impresora",
        "subtipo": "fiscal"
    },
    "tmt20": {
        "marca": "epson",
        "modelo": "Impresora_NO_fiscal_Epson_TM-T20",
        "categoria_equipo": "impresora"
    }
}


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def infer_model_from_question(question: str) -> Dict[str, str]:
    """
    Infiere filtros específicos:
    1. Primero intenta detectar modelos (aliases)
    2. Luego usa inferencia general (categoria_equipo, tipo_documentacion, sistema)
    
    Los filtros de modelo específico tienen prioridad.
    """
    q = normalize(question)
    
    # Intentar encontrar modelo específico
    matches = [
        metadata
        for key, metadata in MODEL_ALIASES.items()
        if key in q
    ]

    if len(matches) > 1:
        raise ValueError("Modelo ambiguo detectado en la consulta")
    
    # Si encontró modelo específico, retornarlo
    if len(matches) == 1:
        return matches[0]

    # Si no hay modelo específico, usar inferencia general
    # (categoria_equipo, tipo_documentacion, sistema)
    return infer_filters_from_question(question)