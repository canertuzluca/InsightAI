
from app.rag.search import search_documents
from app.rag.response_generator import generate_rag_response
from app.models.tool_result import ToolResult


def rag_tool(question: str) -> ToolResult:
    """
    RAG Tool

    Searches company documents and generates
    a natural language answer.
    """

    try:
        documents = search_documents(
            question,
            limit=5
        )

        if not documents:
            return ToolResult(
                tool="RAG",
                success=False,
                result=None,
                error="Bu konu hakkında şirket dokümanlarında bilgi bulunamadı."
            )

        answer = generate_rag_response(
            question,
            documents
        )

        return ToolResult(
            tool="RAG",
            success=True,
            result=answer,
            metadata={
                "documents_found": len(documents)
            }
        )

    except Exception as e:
        return ToolResult(
            tool="RAG",
            success=False,
            result=None,
            error=str(e)
        )
    