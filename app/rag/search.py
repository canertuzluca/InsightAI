from app.rag.embedding import create_embedding
from app.rag.qdrant_client import client


COLLECTION_NAME = "company_docs"


def search_documents(question: str, limit: int = 3):

    embedding = create_embedding(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=limit,
    )

    documents = []

    for point in results.points:
        documents.append(
            {
                "score": point.score,
                "text": point.payload["text"],
                "source": point.payload["source"],
                "category": point.payload["category"],
                "title": point.payload["title"],
            }
        )

    return documents

