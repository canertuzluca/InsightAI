from app.llm.openai_client import client
from app.prompts.validation_prompt import VALIDATION_SYSTEM_PROMPT


def validate_results(question: str, tool_history: list) -> tuple[str, str]:

    results = []

    for result in tool_history:
        if result.success:
            results.append(
                f"""
TOOL: {result.tool}

RESULT:
{result.result}
"""
            )

    combined_results = "\n---\n".join(results)

    prompt = f"""
User Question:
{question}

Collected Tool Results:
{combined_results}

Validate whether the collected information is sufficient
to completely answer the user's question.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": VALIDATION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    result = response.output_text.strip()

    if result.startswith("VALID"):
        return "VALID", ""

    if result.startswith("INVALID:"):
        feedback = result[len("INVALID:"):].strip()
        return "INVALID", feedback

    return "INVALID", "Validation sonucu anlaşılamadı."
