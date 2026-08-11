
from app.llm.openai_client import ask_llm


def generate_rag_response(question: str, documents: list) -> str:
    """
    Generates a natural language answer using retrieved documents.
    """

    if not documents:
        return "Bu soruyla ilgili şirket dokümanlarında herhangi bir bilgi bulunamadı."

    context_parts = []

    for document in documents:
        context_parts.append(
            f"Document: {document['title']}\n"
             f"Source: {document['source']}\n"
             f"Content:\n{document['text']}"
)

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are InsightAI, an AI business assistant.

Answer the user's question using ONLY the information provided
in the company documents below.

Do not use outside knowledge.

If the documents do not contain enough information to answer
the question, say that the information was not found in the
company documents.

User Question:
{question}

Company Documents:
{context}

Answer in the same language as the user's question.

Do not mention embeddings, vectors, Qdrant, semantic search,
retrieval, SQL, or internal system details.

Answer clearly and concisely.
"""

    return ask_llm(prompt)

