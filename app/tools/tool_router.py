
from app.llm.tool_router_llm import choose_tool

from app.tools.sql_tool import sql_tool
from app.tools.rag_tool import rag_tool
from app.tools.analytics_tool import analytics_tool


def route_question(question: str):

    tool = choose_tool(question)

    print(f"[Router] Selected tool: {tool}")

    if tool == "SQL":
        return sql_tool(question)

    elif tool == "RAG":
        return rag_tool(question)

    elif tool == "ANALYTICS":
        return analytics_tool(question)

    else:
        raise ValueError(
            f"Unknown tool: {tool}"
        )
    
    