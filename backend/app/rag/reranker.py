from typing import List, Dict
import os
import cohere
from dotenv import load_dotenv

load_dotenv()

co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

class Reranker:
    def rerank(
        self,
        query: str,
        documents: List[Dict],
        top_n: int = 5
    ) -> List[Dict]:

        if not documents:
            return []

        texts = []

        for doc in documents:
            section_hint = doc["metadata"].get("section_hint")
            if section_hint:
                texts.append(f"{section_hint}\n{doc['text']}")
            else:
                texts.append(doc["text"])

        response = co.rerank(
            model="rerank-v4.0-pro",
            query=query,
            documents=texts,
            top_n=min(top_n, len(texts))
        )

        reranked_docs = []

        for result in response.results:
            original_doc = documents[result.index]
            reranked_docs.append({
                "text": original_doc["text"],
                "metadata": original_doc["metadata"],
                "score": result.relevance_score
            })

        return reranked_docs
