from pathlib import Path
from app.graph.state import ChatState
from app.llm.cohere_client import CohereClient

PROMPT_PATH = Path("app/rag/prompts/chat_prompt.txt")

llm = CohereClient()
prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

def conversational_node(state: ChatState) -> ChatState:
    question = state["question"]

    prompt = prompt_template.format(question=question)
    # Respuesta conversacional: dejamos la temperatura por defecto
    # definida en CohereClient para mantener algo de variación.
    answer = llm.generate(prompt)

    return {
        **state,
        "answer": answer,
        "sources": [],
        "images": [],
        "used_rag": False
    }
