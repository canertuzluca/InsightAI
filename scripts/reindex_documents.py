from pathlib import Path
from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct, VectorParams, Distance

from app.rag.embedding import create_embedding
from app.rag.qdrant_client import client


COLLECTION_NAME = "company_docs"


def reindex_documents():

    # Collection varsa önce sil
    if client.collection_exists(COLLECTION_NAME):
        print(f"Deleting existing collection: {COLLECTION_NAME}")
        client.delete_collection(COLLECTION_NAME)

    # Temiz collection oluştur
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE,
        ),
    )

    print(f"Created collection: {COLLECTION_NAME}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    documents = list(Path("docs").rglob("*.md"))

    points = []

    for path in documents:

        text = path.read_text(encoding="utf-8")

        chunks = splitter.split_text(text)

        category = path.parent.name

        title = path.stem.replace("_", " ").title()

        for chunk in chunks:

            enriched_text = f"Document: {title}\n\n{chunk}"

            embedding = create_embedding(enriched_text)

            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "text": chunk,
                        "source": str(path),
                        "category": category,
                        "title": title,
                    },
                )
            )

        print(f"Indexed: {path}")
        print(f"Chunks: {len(chunks)}")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print()
    print("Reindex completed.")
    print(f"Total points: {len(points)}")


if __name__ == "__main__":
    reindex_documents()

