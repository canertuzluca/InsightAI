
from app.llm.sql_generator import generate_sql

question = "Caner Tuzluca'nın maaşı nedir?"

sql = generate_sql(question)

print("Question:")
print(question)

print("\nGenerated SQL:")
print(sql)
