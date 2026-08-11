
from app.llm.openai_client import ask_llm
from app.prompts.sql_prompt import SQL_SYSTEM_PROMPT


def generate_sql(question: str) -> str:
    """
    Converts a natural language question into SQL.
    """

    prompt = f"""
{SQL_SYSTEM_PROMPT}

User Question:
{question}
"""

    sql = ask_llm(prompt)

    return sql.strip()
