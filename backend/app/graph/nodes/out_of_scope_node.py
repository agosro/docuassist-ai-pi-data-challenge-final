from app.graph.state import ChatState


def out_of_scope_node(state: ChatState) -> ChatState:
    return {
        **state,
        "answer": (
            "Puedo ayudarte únicamente con consultas relacionadas "
            "a la documentación interna de la empresa."
        ),
        "sources": []
    }
