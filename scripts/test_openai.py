
from app.llm.openai_client import ask_llm

response = ask_llm(
    "Hello! Reply with exactly this sentence: InsightAI connection successful."
)

print(response)

