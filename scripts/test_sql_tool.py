
from app.tools.sql_tool import sql_tool

question = "Caner Tuzluca'nın maaşı nedir?"

response = sql_tool(question)

print("\nGenerated SQL:")
print(response["sql"])

print("\nDatabase Result:")
print(response["result"])
