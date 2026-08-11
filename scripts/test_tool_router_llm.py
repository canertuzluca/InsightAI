
from app.llm.tool_router_llm import choose_tool

questions = [
    "Caner Tuzluca'nın maaşı nedir?",
    "Şirketin yıllık izin politikası nedir?",
    "Son 6 ayın satış grafiğini oluştur.",
]

for question in questions:

    print("\nQuestion:")
    print(question)

    print("Selected Tool:")
    print(choose_tool(question))

    print("-" * 40)
    