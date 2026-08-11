
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ToolResult:
    tool: str
    success: bool
    result: Any
    error: Optional[str] = None
    metadata: Optional[dict] = None

    