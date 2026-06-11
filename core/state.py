# Define the structure of the agent's state
from typing import List, TypedDict


class AgentState(TypedDict):
    input: str
    decision: str
    tool_output: str
    intermediate_steps: List[str]
    output: str