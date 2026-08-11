
from app.database.query_executor import execute_query


rows = execute_query(
    """
    SELECT
        first_name,
        last_name,
        salary
    FROM employees
    LIMIT 5;
    """
)

print(rows)
