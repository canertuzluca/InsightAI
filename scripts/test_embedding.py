
from app.rag.embedding import create_embedding

text = "Employees are entitled to 20 days of annual leave."

embedding = create_embedding(text)

print("Vector length:", len(embedding))
print("First 5 values:")
print(embedding[:5])
