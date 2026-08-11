
from app.llm.sql_generator import generate_sql
from app.agents.response_generator import generate_response
from app.database.query_executor import execute_query


question = "Caner Tuzluca'nın maaşı nedir?"

sql = generate_sql(question)

result = execute_query(sql)

answer = generate_response(question, result)

print("\nQuestion:")
print(question)

print("\nSQL:")
print(sql)

print("\nDatabase Result:")
print(result)

print("\nFinal Answer:")
print(answer)

