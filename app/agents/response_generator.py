
from app.llm.openai_client import ask_llm


def generate_response(question: str, sql_result) -> str:
    """
    Converts SQL query results into a natural language answer.
    """

    prompt = f"""
You are an AI business assistant.

User Question:
{question}

Database Result:
{sql_result}

Answer the user's question naturally.

Do not mention SQL.

If there is no result, say that no data was found.
"""

    return ask_llm(prompt)

