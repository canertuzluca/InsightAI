from app.rag.search import search_documents


questions = [
    "What are the standard working hours?",
    "What are the standard working hours?",
    "How many annual leave days do employees have?",
]


for question in questions:

    print("\n" + "=" * 60)
    print("Question:", question)
    print("=" * 60)

    results = search_documents(question, limit=3)

    for result in results:
        print("\nScore:", result["score"])
        print("Source:", result["source"])
        print("Category:", result["category"])
        print("Text:")
        print(result["text"])

