from app.llm.agent_decision import decide_next_action

from typing import Any

from app.llm.tool_router_llm import choose_tool

from app.tools.sql_tool import sql_tool
from app.tools.rag_tool import rag_tool
from app.tools.analytics_tool import analytics_tool

from app.agents.response_generator import generate_response
from app.agents.analytics_response_generator import generate_analytics_response

from app.graph.state import AgentState


def router_node(state: AgentState):

    question = state["question"]

    tool = choose_tool(question)

    print(f"[Agent] Selected tool: {tool}")

    return {
        "selected_tool": tool
    }


def sql_node(state: AgentState):

    result = sql_tool(state["question"])

    history = state.get("tool_history", [])
    context = state.get("context", {})

    if result.success:
        context["sql_result"] = result.result

    return {
        "tool_result": result,
        "tool_history": history + [result],
        "iteration": state.get("iteration", 0) + 1,
        "context": context,
    }


def rag_node(state: AgentState):

    result = rag_tool(state["question"])

    history = state.get("tool_history", [])

    return {
        "tool_result": result,
        "tool_history": history + [result],
        "iteration": state.get("iteration", 0) + 1,
    }


def analytics_node(state: AgentState):

    history = state.get("tool_history", [])

    sql_result = None

    # Önceki tool sonuçları içinde başarılı SQL sonucunu bul
    for result in history:
        if result.tool == "SQL" and result.success:
            sql_result = result.result
            break

    print("\n[DEBUG] Analytics Node")
    print(f"[DEBUG] SQL Result: {sql_result}")

    context = {
        "sql_result": sql_result
    }

    result = analytics_tool(
        state["question"],
        context
    )

    print(f"[DEBUG] Analytics Result: {result.result}")
    print(f"[DEBUG] Analytics Metadata: {result.metadata}")

    return {
        "tool_result": result,
        "tool_history": history + [result],
        "iteration": state.get("iteration", 0) + 1,
    }


"""def response_node(state: AgentState):

    tool_response = state["tool_result"]

    if not tool_response.success:
        return {
            "final_answer": f"Tool error: {tool_response.error}"
        }

    if tool_response.tool == "ANALYTICS":

        answer = generate_analytics_response(
            state["question"],
            tool_response.result,
        )

    else:

        answer = generate_response(
            state["question"],
            tool_response.result,
        )

    return {
        "final_answer": answer
    }"""

def response_node(state: AgentState):

    tool_response = state["tool_result"]

    print("\n[DEBUG] Response Node")
    print(f"[DEBUG] Tool: {tool_response.tool}")
    print(f"[DEBUG] Success: {tool_response.success}")
    print(f"[DEBUG] Result: {tool_response.result}")

    if not tool_response.success:
        return {
            "final_answer": f"Tool error: {tool_response.error}"
        }

    if tool_response.tool == "ANALYTICS":

        answer = generate_analytics_response(
            state["question"],
            tool_response.result,
        )

    else:

        answer = generate_response(
            state["question"],
            tool_response.result,
        )

    return {
        "final_answer": answer
    }

def decision_node(state: AgentState):

    question = state["question"]
    history = state.get("tool_history", [])
    iteration = state.get("iteration", 0)

    print(
        f"[Agent] Decision step. "
        f"Iteration: {iteration}"
    )

    question_lower = question.lower()

    # --------------------------------------------------
    # Safety: maximum iteration
    # --------------------------------------------------

    if iteration >= 3:
        return {
            "next_action": "FINISH"
        }

    # --------------------------------------------------
    # No tool has been executed yet
    # --------------------------------------------------

    if len(history) == 0:
        return {
            "next_action": "ROUTE"
        }

    # --------------------------------------------------
    # Check whether the question requires analytics
    # --------------------------------------------------

    analytics_keywords = [
        "satış performansı",
        "satış performans",
        "satış trendi",
        "satış analizi",
        "satışları",
        "satışlar",
        "ciro",
        "gelir",
        "satış miktarı",
        "performansı",
        "performans",
    ]

    requires_analytics = any(
        keyword in question_lower
        for keyword in analytics_keywords
    )

    # --------------------------------------------------
    # Check whether analytics has already been executed
    # --------------------------------------------------

    analytics_executed = any(
        result.tool == "ANALYTICS"
        for result in history
    )

    # --------------------------------------------------
    # If the question explicitly requires analytics
    # and analytics has not been executed yet,
    # ALWAYS continue with ANALYTICS.
    # --------------------------------------------------

    if requires_analytics and not analytics_executed:

        print(
            "[Agent] Analytics is required but has not "
            "been executed yet."
        )

        return {
            "next_action": "ANALYTICS"
        }

    # --------------------------------------------------
    # Otherwise finish
    # --------------------------------------------------

    return {
        "next_action": "FINISH"
    }





