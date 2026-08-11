
from app.tools.tool_router import route_question

question = "Caner Tuzluca'nın maaşı nedir?"

response = route_question(question)

print("\nGenerated SQL:")
print(response["sql"])

print("\nDatabase Result:")
print(response["result"])
