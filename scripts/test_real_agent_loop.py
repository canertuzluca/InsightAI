
from app.graph.workflow import graph


question = "Caner Tuzluca hangi departmanda çalışıyor ve bu departmanın satış performansı nedir?"



result = graph.invoke({
    "question": question,
    "tool_history": [],
    "iteration": 0,
})


print()
print("=" * 60)

print("Question:")
print(question)

print()
print("Tool History:")

for item in result.get("tool_history", []):
    print(
        f"- {item.tool}"
    )

print()
print("Final Answer:")
print(result.get("final_answer"))


