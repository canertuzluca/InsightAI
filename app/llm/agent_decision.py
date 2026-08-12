from app.llm.openai_client import client
from app.prompts.decision_prompt import DECISION_SYSTEM_PROMPT


def decide_next_action(
    question: str,
    tool_history: list,
    validation_feedback: str = "",
) -> str:
    """
    Uses the LLM to decide what the agent should do next.

    Possible outputs:
        SQL
        RAG
        ANALYTICS
        FINISH
    """

    history_text = []

    for result in tool_history:
        history_text.append(
            f"""
Tool: {result.tool}
Success: {result.success}
Result: {result.result}
Error: {result.error}
"""
        )

    history = "\n---\n".join(history_text)

    validation_context = ""

    if validation_feedback:
        validation_context = f"""
Validation feedback:

{validation_feedback}

The previous answer was incomplete.

You MUST select the tool required to obtain the missing information.
"""

    prompt = f"""
User Question:
{question}

Tools already executed:
{history}

{validation_context}

Decide the next action.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": DECISION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    action = response.output_text.strip().upper()

    allowed_actions = {
        "SQL",
        "RAG",
        "ANALYTICS",
        "FINISH",
    }

    if action not in allowed_actions:
        return "FINISH"

    return action
