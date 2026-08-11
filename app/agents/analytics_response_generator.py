
from app.llm.openai_client import ask_llm


def generate_analytics_response(question: str, analytics_result: dict) -> str:
    """
    Converts deterministic analytics results into a natural language answer.

    The LLM must only explain the provided numbers.
    It must never invent or recalculate values.
    """

    prompt = f"""
You are an AI business analytics assistant.

User Question:
{question}

Deterministic Analytics Result:
{analytics_result}

Your task is to explain the analytics result to the user in clear,
natural Turkish.

IMPORTANT RULES:

1. Use ONLY the numbers provided in the analytics result.
2. Never invent a number.
3. Never change a number.
4. Do not perform new calculations.
5. Do not mention SQL, PostgreSQL, Pandas, Python or internal implementation.
6. If a percentage is provided, you may explain what it means.
7. Clearly mention the highest and lowest month when relevant.
8. Be concise but informative.
9. If the data shows a very unusual first or last month, mention that
   this can affect the percentage-based growth interpretation.
10. Answer the user's exact question.

Return ONLY the final answer in Turkish.
"""

    return ask_llm(prompt)

