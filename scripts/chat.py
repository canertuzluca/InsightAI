
from app.agents.chat_agent import chat


print("=" * 50)
print("InsightAI")
print("Type 'exit' to quit.")
print("=" * 50)

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    answer = chat(question)

    print("\nAnswer:")
    print(answer)
    