from typing import TypedDict, Optional

class TicketState(TypedDict):
    ticket: str
    category: Optional[str]
    confidence: Optional[float]
    reasoning: Optional[str]
    sentiment: Optional[str]
    route: Optional[str]
    response: Optional[str]
    needs_human: bool