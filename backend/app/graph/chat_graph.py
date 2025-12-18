from langgraph.graph import StateGraph, END
from app.graph.state import ChatState
from app.graph.nodes.classify_intent import classify_intent
from app.graph.nodes.conversational_node import conversational_node
from app.graph.nodes.out_of_scope_node import out_of_scope_node
from app.graph.nodes.documentation_node import documentation_node



def build_chat_graph():
    graph = StateGraph(ChatState)

    #  Nodos
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("conversational", conversational_node)
    graph.add_node("out_of_scope", out_of_scope_node)
    graph.add_node("documentation", documentation_node)

    #  Entry point
    graph.set_entry_point("classify_intent")

    #  Ruteo según intención
    graph.add_conditional_edges(
        "classify_intent",
        lambda state: state["intent"],
        {
            "greeting": "conversational",
            "documentation": "documentation",
            "out_of_scope": "out_of_scope"
        }
    )

    #  Finalización
    graph.add_edge("conversational", END)
    graph.add_edge("out_of_scope", END)
    graph.add_edge("documentation", END)

    return graph.compile()
