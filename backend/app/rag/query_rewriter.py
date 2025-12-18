import re

# Verbos comunes en lenguaje natural → forma nominal típica de manuales
VERB_TO_NOUN = {
    "generar": "generación",
    "volver a generar": "generación",
    "descargar": "descarga",
    "configurar": "configuración",
    "instalar": "instalación",
    "declarar": "declaración",
    "imprimir": "impresión",
    "ver": "visualización",
    "consultar": "consulta",
}


def normalize_query(q: str) -> str:
    """
    Normalización liviana:
    - minúsculas
    - sin signos
    - elimina muletillas conversacionales
    """
    q = q.lower()
    q = re.sub(r"[¿?]", "", q)

    fillers = [
        "como puedo",
        "cómo puedo",
        "como hago",
        "cómo hago",
        "puedo",
        "volver a",
    ]

    for f in fillers:
        q = q.replace(f, "")

    return q.strip()


def nominalize_query(q: str) -> str:
    """
    Convierte verbos frecuentes en sustantivos técnicos.
    """
    for verb, noun in VERB_TO_NOUN.items():
        q = q.replace(verb, noun)
    return q


def expand_for_manual_structure(q: str) -> str:
    """
    Agrega términos genéricos típicos de manuales:
    secciones, informes, reportes, pantallas, etc.
    """
    return f"{q} informe reporte sección pantalla"


def build_retrieval_query(question: str, is_system_doc: bool) -> str:
    """
    Construye una query optimizada SOLO para retrieval.
    """
    if not is_system_doc:
        return question

    q = normalize_query(question)
    q = nominalize_query(q)
    q = expand_for_manual_structure(q)

    return q
