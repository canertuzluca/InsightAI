
from app.llm.sql_generator import generate_sql
from app.database.query_executor import execute_query
from app.database.sql_guard import validate_sql


def ask_database(question: str):
    """
    End-to-end SQL Agent.

    Question
        ↓
    GPT
        ↓
    SQL Guard
        ↓
    PostgreSQL
        ↓
    Result
    """

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    if not validate_sql(sql):
        raise ValueError("Unsafe SQL generated.")

    result = execute_query(sql)

    return result

