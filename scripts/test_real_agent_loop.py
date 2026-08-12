
from app.graph.workflow import graph


questions = [
    (
        "RAG",
        "Çalışanların yıllık ücretli izin hakkı kaç gün?"
    ),
    (
        "SQL",
        "Caner Tuzluca hangi departmanda çalışıyor?"
    ),
    (
        "ANALYTICS",
        "IT departmanının satış performansı nedir?"
    ),
    (
        "SQL + ANALYTICS",
        "Caner Tuzluca hangi departmanda çalışıyor ve bu departmanın satış performansı nedir?"
    ),
    (
        "RAG + SQL + ANALYTICS",
        "Şirketin uzaktan çalışma politikası nedir ve IT departmanının satış performansı nasıldır?"
    ),
]


for test_name, question in questions:

    print()
    print("=" * 70)
    print(f"TEST: {test_name}")
    print(f"QUESTION: {question}")
    print("=" * 70)

    result = graph.invoke({
        "question": question,
        "tool_history": [],
        "iteration": 0,
    })

    print()
    print("Tool History:")

    for item in result.get("tool_history", []):
        print(
            f"- {item.tool}"
        )

    print()
    print("Final Answer:")
    print(result.get("final_answer"))

    