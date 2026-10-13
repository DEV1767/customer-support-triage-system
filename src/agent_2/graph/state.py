from typing import TypeDict,Optional

class TicketState(TypeDict):
    ticket:str
    category:Optional[str]
    confidence:Optional[str]
    reasoning:Optional[str]
    sentiments:Optional[str]
    route:Optional[str]
    responce:Optional[str]
    need_human:bool
    