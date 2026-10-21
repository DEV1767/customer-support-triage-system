import uuid
from agent_2.database import escalations_collection
from datetime import datetime,timezone
from langchain_core.tools import tool


def generate_ticket_id()->str:
    """
    Generate a collosion-resistant ticket ID LIKE TKT-20261021-AB12CD.
    """
    today=datetime.now(timezone.utc).strftime("%Y%m%d")
    unique_suffix=uuid.uuid4().hex[:6].upper()
    
    return f"TKT-{today}-{unique_suffix}"


def save_escalation_from_state(
    state:dict,
    escalation_reason:str,
    ticket_id:str |None=None,
)->str:
  """Save an escalation directly from a LangGraph state dictionary (used by Python nodes).
    Returns the ticket_id.
  """
  if not ticket_id:
    ticket_id=state.get("ticket_id") or generate_ticket_id()
  
  order_id=state.get("order_id")
  category=state.get("category","general")

  missing_information=[]

  if order_id is None and category=="billing":
    missing_information.append("order_id")

  record = {
        "ticket_id": ticket_id,
        "ticket": state.get("ticket", ""),
        "order_id": order_id,
        "category": category,
        "confidence": state.get("confidence", 1.0),
        "sentiment": state.get("sentiment", "calm"),
        "reasoning": state.get("reasoning", ""),
        "escalation_reason": escalation_reason,
        "missing_information": missing_information,
        "status": (
            "awaiting_customer_information"
            if missing_information
            else "pending"
        ),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

  escalations_collection.insert_one(record)
  return ticket_id


@tool
def save_escalation(
    ticket:str,
    escalation_reason:str,
    order_id:str|None,
)->dict:
  """
  Escalate an issue to human support when an agent cannot resolve it.
    Call this tool when:
    - Customer requests a human or supervisor.
    - An issue requires human intervention (e.g. duplicate charge disputes, refund requests).
    - Customer is very upset or angry.
  """
  ticket_id=generate_ticket_id()
  missing_information=[]

  if not order_id:
    missing_information.append("order_id")




def get_ticket(ticket_id:str)->dict| None:
    """ Retrieve an existing escalation by ticket ID."""
    return escalations_collection.find_one(
        {"ticket_id":ticket_id},
        {"_id":0}
    )


def update_ticket(ticket_id:str,order_id:str)->bool:
    """Add an orderID to an existing escalation."""
    result=escalations_collection.update_one(
        {
            "ticket_id":ticket_id,
            "status":"awaiting_customer_information",
        },
        {
            "$set":{
                "order_id":order_id,
                "missing_information":[],
                "status":"pending",
                "updated_at":datetime.now(timezone.utc),
            }
        },
    )

    return result.modified_count==1