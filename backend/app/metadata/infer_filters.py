# app/metadata/infer_filters.py

from typing import Dict
import re


# Diccionario de sistemas conocidos con sus variantes
SISTEMAS_CONOCIDOS = {
    "StarPOSMarketManual": ["starpos", "star pos", "starpos market", "star-pos"],
    "BackupMaster": ["backupmaster", "backup master"],
    "CloudSync": ["cloudsync", "cloud sync"],
    "DataVault": ["datavault", "data vault"],
}


def infer_filters_from_question(question: str) -> Dict[str, str]:
    """
    Infere únicamente filtros NO críticos.
    NO infiere marca ni modelo (demasiado riesgo de error).
    SÍ infiere sistema (nombres únicos de software).
    """
    q = question.lower()
    filters = {}

    # Categoría de equipo (opcional)
    if "impresora" in q:
        filters["categoria_equipo"] = "impresora"
    elif "balanza" in q:
        filters["categoria_equipo"] = "balanza"

    # Tipo de documentación
    if any(word in q for word in ["especificaciones", "características", "tecnicas"]):
        filters["tipo_documentacion"] = "tecnica"

    if any(word in q for word in ["configurar", "instalar", "usar", "cargar", "cierre"]):
        filters["tipo_documentacion"] = "sistema"

    # 🔍 INFERIR NOMBRE DEL SISTEMA
    # Buscar coincidencias con sistemas conocidos
    for sistema_real, variantes in SISTEMAS_CONOCIDOS.items():
        for variante in variantes:
            # Usar búsqueda flexible (ignora espacios y guiones)
            pattern = re.escape(variante).replace(r"\ ", r"[\s\-]*")
            if re.search(pattern, q):
                filters["sistema"] = sistema_real
                filters["tipo_documentacion"] = "sistema"  # Forzar tipo
                break
        
        if "sistema" in filters:
            break

    return filters
