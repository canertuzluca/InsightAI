
import json

from app.llm.openai_client import client


def decide_next_action(
    question: str,
    tool_history: list,
    iteration: int,
) -> str:
    """
    LLM-based Agent Decision.

    Decides whether the agent should:
    - FINISH
    - ANALYTICS
    - ROUTE
    """

    history_text = []

    for i, result in enumerate(tool_history, start=1):

        history_text.append(
            f"""
Tool {i}:
Name: {result.tool}
Success: {result.success}
Result: {result.result}
Error: {result.error}
"""
        )

    history_text = "\n".join(history_text)

    prompt = f"""
You are the decision-making component of an enterprise AI agent.

Your task is to decide what the agent should do NEXT.

User question:
{question}

Tool history:
{history_text}

Current iteration:
{iteration}

Available actions:

FINISH
Use FINISH ONLY when the user's ENTIRE question has already been
answered by the available tool results.

ANALYTICS
Use ANALYTICS when:
- the user asks about sales performance,
- sales trends,
- revenue,
- sales statistics,
- sales aggregation,
- department sales performance,
- employee sales performance,
- numerical analysis,
- statistics,
- or any other business analytics.

ROUTE
Use ROUTE when the current tool was inappropriate and another
tool should be selected.

IMPORTANT RULES:

1. Read the ENTIRE user question carefully.

2. A question may contain MULTIPLE parts.

3. If SQL answered only the employee/company information part,
   but the question also asks for sales performance or analytics,
   DO NOT FINISH.

4. Example:

User question:
"Caner Tuzluca hangi departmanda çalışıyor ve bu departmanın
satış performansı nedir?"

If SQL result says:
"Caner Tuzluca -> IT"

Then SQL has answered ONLY the first part.

The correct next action MUST be:

ANALYTICS

5. If the question contains the words or concepts:
   "satış performansı",
   "satış trendi",
   "satış analizi",
   "ciro",
   "gelir",
   "satış miktarı",
   "satışları",
   "performansı"
   then ANALYTICS should be strongly preferred unless
   the complete answer is already present in tool history.

6. Never FINISH if an explicit analytics request remains unanswered.

7. If SQL has already answered the question completely,
   use FINISH.

8. Never invent information.

9. Never exceed 3 iterations.

10. Return ONLY valid JSON.

Expected output:

{{
    "action": "FINISH"
}}

or

{{
    "action": "ANALYTICS"
}}

or

{{
    "action": "ROUTE"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise agent decision engine. "
                    "Return only valid JSON."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)

        action = data.get("action")

        if action in {"FINISH", "ANALYTICS", "ROUTE"}:
            return action

    except json.JSONDecodeError:
        pass

    # Safe fallback
    return "FINISH"
