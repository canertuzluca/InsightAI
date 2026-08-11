
from openai import OpenAI

from app.config.settings import get_settings

settings = get_settings()

client = OpenAI(
    api_key=settings.openai_api_key
)


def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to OpenAI and returns the response text.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text
