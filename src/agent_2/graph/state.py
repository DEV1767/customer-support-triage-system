from typing import TypedDict, Optional,Annotated,List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class TicketState(TypedDict):
    ticket: str
    order_id:str|None
    ticket_id:str | None

    category: Optional[str]
    confidence: Optional[float]
    reasoning: Optional[str]
    sentiment: Optional[str]

    route: Optional[str]
    response: Optional[str]
    needs_human: bool
    
    conversation_state:str
    messages:Annotated[List[AnyMessage],add_messages]
