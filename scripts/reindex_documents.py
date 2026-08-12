
from pathlib import Path
from uuid import uuid4

from qdrant_client.models import PointStruct, VectorParams, Distance

from app.rag.embedding import create_embedding
from app.rag.qdrant_client import client

COLLECTION_NAME = "company_docs"


def parse_markdown_sections(text: str):
    """
    Splits Markdown documents into meaningful sections.

    Each section keeps its heading so that the embedding
    contains the semantic context of the text.
    """

    lines = text.splitlines()

    sections = []

    current_heading = None
    current_content = []

    for line in lines:

        if line.startswith("#"):
            if current_content and current_heading:
                sections.append(
                    {
                        "section": current_heading,
                        "text": "\n".join(current_content).strip(),
                    }
                )

            current_heading = line.lstrip("#").strip()
            current_content = []

        else:
            current_content.append(line)

    if current_content and current_heading:
        sections.append(
            {
                "section": current_heading,
                "text": "\n".join(current_content).strip(),
            }
        )

    return sections


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

    documents = list(Path("docs").rglob("*.md"))

    points = []

    for path in documents:

        text = path.read_text(encoding="utf-8")

        sections = parse_markdown_sections(text)

        category = path.parent.name
        title = path.stem.replace("_", " ").title()

        print()
        print(f"Indexed: {path}")
        print(f"Sections: {len(sections)}")

        for section in sections:

            section_name = section["section"]
            section_text = section["text"]

            if not section_text.strip():
                continue

            enriched_text = (
                f"Document: {title}\n"
                f"Section: {section_name}\n\n"
                f"{section_text}"
            )

            embedding = create_embedding(enriched_text)

            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "text": section_text,
                        "source": str(path),
                        "category": category,
                        "title": title,
                        "section": section_name,
                    },
                )
            )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print()
    print("Reindex completed.")
    print(f"Total points: {len(points)}")


if __name__ == "__main__":
    reindex_documents()

    