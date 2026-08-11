
from app.graph.workflow import graph


questions = [
    "Caner Tuzluca'nın maaşı nedir?",
    "Şirketin yıllık izin hakkı kaç gün?",
    "Son 6 ayın satış trendi nedir?",
]


for question in questions:

    print("=" * 60)
    print(f"Question: {question}")

    result = graph.invoke({
        "question": question
    })

    print()
    print("Selected Tool:")
    print(result["selected_tool"])

    print()
    print("Final Answer:")
    print(result["final_answer"])

    print()
    