from typing import List, Dict
import os
import cohere
from dotenv import load_dotenv

from app.vectorstore.client import get_vectorstore

load_dotenv()

co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))


def build_where(filters: Dict[str, str] | None):
    if not filters:
        return None

    items = [{k: v} for k, v in filters.items()]

    # 1 solo filtro → sin operador lógico
    if len(items) == 1:
        return items[0]

    # 2 o más filtros → AND
    return {
        "$and": items
    }


class Retriever:
    """
    Recupera los chunks más relevantes desde la base vectorial
    usando búsqueda por similaridad + filtros por metadata.
    """

    def __init__(self, collection_name: str = "documentation"):
        client = get_vectorstore()
        self.collection = client.get_or_create_collection(name=collection_name)

    def retrieve(
        self,
        query: str,
        filters: Dict[str, str],
        top_k: int = 10
    ) -> List[Dict]:
        """
        Busca chunks similares a la consulta aplicando filtros por metadata
        y fuerza coincidencia estricta por modelo si está presente.
        """

        # Embedding de la query
        response = co.embed(
            model="embed-multilingual-v3.0",
            texts=[query],
            input_type="search_query"
        )

        query_embedding = response.embeddings.float[0]

        # Limpieza de filtros (elimina None y strings vacíos)
        where_filters = {k: v for k, v in filters.items() if v}
        where_clause = build_where(where_filters)

        # Query a la base vectorial
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause
        )

        # Post-filter estricto por modelo (CLAVE)
        modelo_filtro = filters.get("modelo")

        retrieved_chunks = []

        for i in range(len(results["documents"][0])):
            text = results["documents"][0][i]
            metadata = results["metadatas"][0][i]
            distance = results["distances"][0][i]

            # 🚨 Si hay modelo seleccionado, SOLO aceptar ese modelo
            if modelo_filtro:
                if metadata.get("modelo") != modelo_filtro:
                    continue

            retrieved_chunks.append({
                "text": text,
                "metadata": metadata,
                "distance": distance
            })

        return retrieved_chunks
