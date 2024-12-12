from typing import TypedDict, Annotated
from langchain_core.agents import AgentAction
import operator



class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str
    
    
class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]
    
class AgentState(TypedDict):
    input: str
    # chat_history: list[BaseMessage]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    
