
from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState


def test_node(state: AgentState):
    print("Node çalıştı.")

    return {
        "final_answer": f"LangGraph soruyu aldı: {state['question']}"
    }


graph_builder = StateGraph(AgentState)

graph_builder.add_node("test_node", test_node)

graph_builder.add_edge(START, "test_node")
graph_builder.add_edge("test_node", END)

graph = graph_builder.compile()


if __name__ == "__main__":

    result = graph.invoke({
        "question": "LangGraph çalışıyor mu?"
    })

    print()
    print("Final State:")
    print(result)
    