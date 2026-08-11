
from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState


def first_node(state: AgentState):

    print("First node çalıştı.")

    return {
        "tool_history": ["SQL sonucu"],
        "iteration": 1,
    }


def second_node(state: AgentState):

    print("Second node çalıştı.")

    history = state.get("tool_history", [])

    return {
        "tool_history": history + ["Analytics sonucu"],
        "iteration": state.get("iteration", 0) + 1,
    }


builder = StateGraph(AgentState)

builder.add_node("first", first_node)
builder.add_node("second", second_node)

builder.add_edge(START, "first")
builder.add_edge("first", "second")
builder.add_edge("second", END)

graph = builder.compile()


if __name__ == "__main__":

    result = graph.invoke({
        "question": "Test sorusu",
        "iteration": 0,
        "tool_history": [],
    })

    print()
    print("Final State:")
    print(result)

    