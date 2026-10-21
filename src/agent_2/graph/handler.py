import uuid
from agent_2.graph.state import TicketState
from agent_2.tools.get_order import get_order,extract_order_id
from agent_2.tools.save_escalations import save_order


def billing_agent(state: TicketState) -> dict:
    ticket = state["ticket"]

    order_id=extract_order_id(ticket)

    if not  order_id:
        return {
            "responce":"Please provide your order ID",
            "route":"billing_agent",
            "needs_human":False,
        }

    result=get_order(order_id)

    if not result["success"]:
        return {
            "response": result["message"],
            "route": "billing_agent",
            "needs_human": False,
        }

    order = result["order"]

    response = (
        f"Order ID: {order['order_id']}\n"
        f"Amount: {order['currency']} {order['amount']}\n"
        f"Status: {order['status']}"
    )
    return {
        "response": response,
        "route": "billing_agent",
        "needs_human": False,
    }

def tech_agent(state: TicketState) -> dict:
    ticket = state["ticket"]

    response = f"Technical issue received: {ticket}"

    return {
        "response": response,
        "route": "tech_agent",
        "needs_human": False
    }

def human_escalation(state: TicketState) -> dict:
    """Escalate a support ticket and save it to MongoDB."""
    
    ticket_id=f"TKT-{uuid.uuid4().hex[:8].upper()}"

    if state["sentiment"]=="angry":
        reason="angry_customer"
    elif state["confidence"]<0.6:
        reason="low_classification_confidence"
    elif state["category"]=="general":
        reason="general_category"
    else:
        reason="require_human_review"
    
    escalation_id=save_order(state,reason,ticket_id)

    return {
          "response": (
            "Your ticket has been escalated to human support "
            "for further review."
        ),
        "route": "human_escalation",
        "needs_human": True,
    }