
from app.tools.analytics_tool import analytics_tool


question = "Son 6 ayın satış trendi nedir?"

result = analytics_tool(question)

print("\nQuestion:")
print(question)

print("\nAnalytics Result:")
print(result)

