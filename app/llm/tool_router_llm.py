
from app.llm.openai_client import client
from app.prompts.router_prompt import ROUTER_SYSTEM_PROMPT


def choose_tool(question: str) -> str:
    """
    Uses the LLM to decide which tool should handle
    the user's question.

    Returns one of:
        SQL
        RAG
        ANALYTICS
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": ROUTER_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return response.output_text.strip().upper()
