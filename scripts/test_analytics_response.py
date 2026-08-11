
from app.tools.analytics_tool import analytics_tool
from app.agents.analytics_response_generator import generate_analytics_response


question = "Son 6 ayın satış trendi nedir?"

analytics = analytics_tool(question)

answer = generate_analytics_response(
    question,
    analytics["result"]
)

print("\nQuestion:")
print(question)

print("\nAnalytics Result:")
print(analytics)

print("\nFinal Answer:")
print(answer)

