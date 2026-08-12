from typing import TypedDict, Any, List


class AgentState(TypedDict, total=False):

    question: str

    selected_tool: str

    tool_result: Any

    tool_history: List[Any]

    iteration: int

    next_action: str

    final_answer: str

    context: dict

    validation_status: str

    validation_feedback: str
