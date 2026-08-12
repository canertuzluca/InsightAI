from app.llm.agent_decision import decide_next_action
from app.llm.validator import validate_results

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

    history = state.get("tool_history", [])

    print("\n[DEBUG] Response Node")

    for result in history:
        print(
            f"[DEBUG] Tool: {result.tool} | "
            f"Success: {result.success}"
        )

    successful_results = [
        result
        for result in history
        if result.success
    ]

    if not successful_results:
        return {
            "final_answer": "Soruyu yanıtlamak için gerekli bilgi bulunamadı."
        }

    # --------------------------------------------------
    # Single tool result
    # --------------------------------------------------

    if len(successful_results) == 1:

        tool_response = successful_results[0]

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

    # --------------------------------------------------
    # Multiple tool results
    # --------------------------------------------------

    combined_results = []

    for result in successful_results:

        combined_results.append(
            f"""
TOOL: {result.tool}

RESULT:
{result.result}
"""
        )

    combined_context = "\n\n---\n\n".join(
        combined_results
    )

    prompt = f"""
        You are InsightAI, an AI business assistant.

        Answer the user's question using ONLY the
        information provided by the tools.

        User Question:
        {state["question"]}

        Tool Results:
        {combined_context}

        Rules:

        1. Use only information contained in the tool results.
        2. Do not invent any information.
        3. Do not change numbers.
        4. Combine information from multiple tools when necessary.
        5. If RAG provided company policy information,
        use it for policy-related parts of the answer.
        6. If SQL provided employee or company data,
        use it for database-related parts.
        7. If ANALYTICS provided statistical results,
        use those results for performance-related parts.
        8. Answer in Turkish.
        9. Be concise but informative.
        10. Do not mention SQL, RAG, Qdrant, embeddings,
            Pandas, PostgreSQL or internal system details.

        Return ONLY the final answer.
        """

    from app.llm.openai_client import ask_llm

    answer = ask_llm(prompt)

    return {
        "final_answer": answer
    }

# `app/graph/nodes.py` — Yeni `decision_node`


def decision_node(state: AgentState):

    question = state["question"]
    history = state.get("tool_history", [])
    iteration = state.get("iteration", 0)

    print(
        f"[Agent] Decision step. "
        f"Iteration: {iteration}"
    )

    # --------------------------------------------------
    # Safety
    # --------------------------------------------------

    if iteration >= 6:
        print("[Agent] Maximum iteration reached. Finishing.")

        return {
            "next_action": "FINISH"
        }

    # --------------------------------------------------
    # Tool status
    # --------------------------------------------------

    successful_tools = {
        result.tool
        for result in history
        if result.success
    }

    failed_tools = {
        result.tool
        for result in history
        if not result.success
    }

    # --------------------------------------------------
    # Deterministic Analytics dependency
    #
    # If the question requires analytics and SQL has
    # already succeeded, Analytics must be executed.
    # --------------------------------------------------

    question_lower = question.lower()

    analytics_keywords = [
        "satış performansı",
        "satış performans",
        "satış analizi",
        "satış trend",
        "satışlar",
        "gelir",
        "ciro",
        "istatistik",
        "performans",
        "büyüme",
        "analiz",
    ]

    requires_analytics = any(
        keyword in question_lower
        for keyword in analytics_keywords
    )

    if (
        requires_analytics
        and "SQL" in successful_tools
        and "ANALYTICS" not in successful_tools
    ):
        print(
            "[Agent] SQL context available. "
            "Analytics is required. Running Analytics."
        )

        return {
            "next_action": "ANALYTICS",
            "validation_feedback": "",
        }

    # --------------------------------------------------
    # If Analytics already succeeded, we can finish.
    # --------------------------------------------------

    if "ANALYTICS" in successful_tools:
        print(
            "[Agent] Analytics completed successfully. "
            "Finishing."
        )

        return {
            "next_action": "FINISH",
            "validation_feedback": "",
        }

    # --------------------------------------------------
    # Validation feedback
    # --------------------------------------------------

    validation_feedback = state.get(
        "validation_feedback",
        ""
    )

    if validation_feedback:
        print(
            f"[Agent] Validation feedback: "
            f"{validation_feedback}"
        )

    # --------------------------------------------------
    # Ask LLM Orchestrator
    # --------------------------------------------------

    action = decide_next_action(
        question,
        history,
        validation_feedback,
    )

    print(
        f"[Agent] Orchestrator decision: {action}"
    )

    # --------------------------------------------------
    # Prevent unnecessary repetition
    #
    # A failed tool may be retried.
    # A successful tool is not repeated.
    # --------------------------------------------------

    previous_results = [
        result
        for result in history
        if result.tool == action
    ]

    successful_tool_exists = any(
        result.success
        for result in previous_results
    )

    if successful_tool_exists and not validation_feedback:

        print(
            f"[Agent] {action} already executed successfully. "
            f"Finishing to avoid unnecessary repetition."
        )

        return {
            "next_action": "FINISH",
            "validation_feedback": "",
        }

    return {
        "next_action": action,
        "validation_feedback": "",
    }


def validation_node(state: AgentState):
    """
    Validates the final answer against the collected tool results.
    """

    question = state["question"]
    final_answer = state.get("final_answer", "")
    history = state.get("tool_history", [])

    print("\n[DEBUG] Validation Node")

    successful_results = [
        result
        for result in history
        if result.success
    ]

    if not successful_results:
        return {
            "validation_status": "FAILED",
            "validation_feedback": "No successful tool results available."
        }

    combined_results = []

    for result in successful_results:
        combined_results.append(
            f"""
TOOL: {result.tool}

RESULT:
{result.result}
"""
        )

    combined_context = "\n---\n".join(combined_results)

    from app.llm.openai_client import ask_llm

    prompt = f"""
You are the validation agent of InsightAI.

Your job is to verify whether the final answer is supported
by the information returned from the tools.

User Question:
{question}

Tool Results:
{combined_context}

Final Answer:
{final_answer}

Validation rules:

1. The final answer must be supported by the tool results.
2. No information may be invented.
3. Numbers must match the tool results.
4. If multiple tools were used, the final answer may combine
   information from them.
5. The answer must actually address the user's question.
6. Minor wording differences are acceptable.
7. If the answer is correct and supported, return PASS.
8. If the answer contains unsupported or incorrect information,
   return FAIL.

Return ONLY:

PASS

or

FAIL: <short explanation>
"""

    validation = ask_llm(prompt).strip()

    print(f"[DEBUG] Validation Result: {validation}")

    if validation.upper().startswith("PASS"):
        return {
            "validation_status": "PASSED",
            "validation_feedback": validation,
        }

    return {
        "validation_status": "FAILED",
        "validation_feedback": validation,
    }
