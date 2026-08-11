
from app.agents.chat_agent import chat


question = "Caner Tuzluca'nın maaşı nedir?"

answer = chat(question)

print()
print("Question:")
print(question)

print()
print("Answer:")
print(answer)
