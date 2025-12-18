from typing import List, Dict
from pathlib import Path

from app.llm.cohere_client import CohereClient

GENERIC_PROMPT_PATH = Path("app/rag/prompts/rag_prompt_generic.txt")
SPECIFIC_PROMPT_PATH = Path("app/rag/prompts/rag_prompt.txt")


class Generator:
    """
    Genera la respuesta final utilizando el contexto recuperado (RAG)
    y devuelve información para groundedness.
    """

    def __init__(self):
        self.llm = CohereClient()
        self.generic_prompt = GENERIC_PROMPT_PATH.read_text(encoding="utf-8")
        self.specific_prompt = SPECIFIC_PROMPT_PATH.read_text(encoding="utf-8")

    def generate_answer(
        self,
        question: str,
        documents: List[Dict],
        is_generic: bool,
        marca: str | None = None,
        modelo: str | None = None,
    ) -> Dict:
        # Filtro de seguridad adicional por modelo: aunque el nodo de
        # documentación ya filtra, aquí reforzamos que el contexto y las
        # fuentes correspondan únicamente al modelo seleccionado.
        if modelo:
            documents = [
                d for d in documents
                if d.get("metadata", {}).get("modelo") == modelo
            ]

        if not documents:
            return {
                "answer": (
                    "La documentación disponible no contiene información "
                    "sobre este tema para el modelo consultado."
                ),
                "sources": []
            }

        context_blocks = []
        sources = []

        for doc in documents:
            context_blocks.append(doc["text"])
            sources.append({
                "document": doc["metadata"]["document"],
                "page": doc["metadata"]["page"]
            })

        context = "\n\n".join(context_blocks)

        prompt_template = (
            self.generic_prompt if is_generic else self.specific_prompt
        )

        # Permite usar plantillas que incluyan {marca} y {modelo} sin fallar
        # cuando no se proporcionan (se reemplazan por cadena vacía).
        prompt = prompt_template.format(
            context=context,
            question=question,
            marca=marca or "",
            modelo=modelo or "",
        )

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": sources
        }
