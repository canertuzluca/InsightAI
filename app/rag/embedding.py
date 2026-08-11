from openai import OpenAI

from app.config.settings import get_settings

settings = get_settings()

client = OpenAI(api_key=settings.openai_api_key)


def create_embedding(text: str) -> list[float]:
    """
    Creates an embedding vector using OpenAI.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding
