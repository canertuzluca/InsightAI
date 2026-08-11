
from sqlalchemy import text

from app.database.connection import engine


def execute_query(query: str, params: dict | None = None):
    """
    Executes a SQL query and returns the results.

    Args:
        query: SQL query
        params: Optional SQL parameters

    Returns:
        list[dict]
    """

    with engine.connect() as connection:

        result = connection.execute(
            text(query),
            params or {},
        )

        rows = result.mappings().all()

        return [dict(row) for row in rows]
    