
from app.rag.search import search_documents
from app.rag.response_generator import generate_rag_response


question = "Uzaktan çalışma haftada kaç gün yapılabilir?"

documents = search_documents(question, limit=3)

answer = generate_rag_response(question, documents)

print("\nQuestion:")
print(question)

print("\nRetrieved Documents:")

for document in documents:
    print("-" * 50)
    print("Source:", document["source"])
    print("Score:", document["score"])
    print(document["text"])

print("\nFinal Answer:")
print(answer)
