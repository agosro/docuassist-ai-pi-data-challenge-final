from pathlib import Path

from app.llm.cohere_client import CohereClient
from app.graph.state import ChatState


PROMPT_PATH = Path("app/rag/prompts/intent_prompt.txt")

llm = CohereClient()
prompt_template = PROMPT_PATH.read_text(encoding="utf-8")


def classify_intent(state: ChatState) -> ChatState:
    question = state["question"]

    prompt = prompt_template.format(question=question)

    # Para clasificación queremos un comportamiento determinista,
    # por eso usamos temperatura 0.
    intent = llm.generate(prompt, temperature=0.0).strip().lower()

    return {
        **state,
        "intent": intent
    }
