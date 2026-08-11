
from qdrant_client.models import Distance, VectorParams

from app.rag.qdrant_client import client


COLLECTION_NAME = "company_docs"


def create_collection():
    existing = [
        c.name
        for c in client.get_collections().collections
    ]

    if COLLECTION_NAME in existing:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE,
        ),
    )

    print(f"Collection '{COLLECTION_NAME}' created successfully.")


if __name__ == "__main__":
    create_collection()

    