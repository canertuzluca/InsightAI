from pathlib import Path
from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct

from app.rag.embedding import create_embedding
from app.rag.qdrant_client import client


COLLECTION_NAME = "company_docs"


def index_document(file_path: str):
    path = Path(file_path)

    text = path.read_text(encoding="utf-8")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = splitter.split_text(text)

    category = path.parent.name

    title = path.stem.replace("_", " ").title()

    points = []

    for chunk in chunks:

        enriched_text = f"Document: {title}\n\n{chunk}"

        embedding = create_embedding(enriched_text)

        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "source": str(path),
                "category": category,
                "title": title,
            },
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(f"Document indexed successfully: {path}")
    print(f"Chunks created: {len(chunks)}")

    