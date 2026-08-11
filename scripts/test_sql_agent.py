
from app.agents.sql_agent import ask_database

question = "Caner Tuzluca'nın maaşı nedir?"

result = ask_database(question)

print("\nDatabase Result:")
print(result)

