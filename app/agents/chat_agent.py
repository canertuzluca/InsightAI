
from app.tools.tool_router import route_question
from app.agents.response_generator import generate_response
from app.agents.analytics_response_generator import generate_analytics_response


def chat(question: str) -> str:
    """
    Main Chat Agent.

    Routes the question to the appropriate tool
    and generates the final natural language response.
    """

    tool_response = route_question(question)

    if not tool_response.success:
        return f"Tool error: {tool_response.error}"

    if tool_response.tool == "ANALYTICS":
        return generate_analytics_response(
            question,
            tool_response.result,
        )

    return generate_response(
        question,
        tool_response.result,
    )

