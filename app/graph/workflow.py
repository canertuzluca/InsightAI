from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState

from app.graph.nodes import (
    router_node,
    sql_node,
    rag_node,
    analytics_node,
    response_node,
    decision_node,
)


def route_after_router(state: AgentState):

    tool = state["selected_tool"]

    if tool == "SQL":
        return "sql"

    if tool == "RAG":
        return "rag"

    if tool == "ANALYTICS":
        return "analytics"

    raise ValueError(
        f"Unknown tool: {tool}"
    )


def route_after_decision(state: AgentState):

    action = state["next_action"]

    if action == "ANALYTICS":
        return "analytics"

    if action == "ROUTE":
        return "router"

    if action == "FINISH":
        return "response"

    raise ValueError(
        f"Unknown agent action: {action}"
    )


graph_builder = StateGraph(AgentState)


# --------------------------------------------------
# Nodes
# --------------------------------------------------

graph_builder.add_node(
    "router",
    router_node,
)

graph_builder.add_node(
    "sql",
    sql_node,
)

graph_builder.add_node(
    "rag",
    rag_node,
)

graph_builder.add_node(
    "analytics",
    analytics_node,
)

graph_builder.add_node(
    "decision",
    decision_node,
)

graph_builder.add_node(
    "response",
    response_node,
)


# --------------------------------------------------
# START
# --------------------------------------------------

graph_builder.add_edge(
    START,
    "router",
)


# --------------------------------------------------
# Router → Tool
# --------------------------------------------------

graph_builder.add_conditional_edges(
    "router",
    route_after_router,
    {
        "sql": "sql",
        "rag": "rag",
        "analytics": "analytics",
    },
)


# --------------------------------------------------
# Tool → Decision
# --------------------------------------------------

graph_builder.add_edge(
    "sql",
    "decision",
)

graph_builder.add_edge(
    "rag",
    "decision",
)

graph_builder.add_edge(
    "analytics",
    "decision",
)


# --------------------------------------------------
# Decision → Next Action
# --------------------------------------------------

graph_builder.add_conditional_edges(
    "decision",
    route_after_decision,
    {
        "analytics": "analytics",
        "router": "router",
        "response": "response",
    },
)


# --------------------------------------------------
# Response → END
# --------------------------------------------------

graph_builder.add_edge(
    "response",
    END,
)


# --------------------------------------------------
# Compile
# --------------------------------------------------

graph = graph_builder.compile()

