
from app.llm.agent_decision import decide_next_action


action = decide_next_action(
    question="Caner Tuzluca'nın maaşı nedir?",
    tool_history=[],
    iteration=0,
)

print("Decision:", action)

