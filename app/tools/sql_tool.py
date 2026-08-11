
from app.llm.sql_generator import generate_sql
from app.database.sql_guard import validate_sql
from app.database.query_executor import execute_query
from app.models.tool_result import ToolResult


def sql_tool(question: str) -> ToolResult:
    """
    SQL Tool

    Converts a natural language question into SQL,
    validates it, executes it,
    and returns a standardized ToolResult.
    """

    try:
        sql = generate_sql(question)

        if not validate_sql(sql):
            return ToolResult(
                tool="SQL",
                success=False,
                result=None,
                error="Unsafe SQL generated."
            )

        result = execute_query(sql)

        return ToolResult(
            tool="SQL",
            success=True,
            result=result,
            metadata={
                "sql": sql
            }
        )

    except Exception as e:
        return ToolResult(
            tool="SQL",
            success=False,
            result=None,
            error=str(e)
        )
    
    