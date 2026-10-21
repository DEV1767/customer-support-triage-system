import re
from agent_2.database import orders_collection

def get_order(order_id: str) -> dict:
    """Retrieve the order from MongoDB database."""

    order = orders_collection.find_one(
        {"order_id": order_id},
        {"_id": 0},
    )

    if not order:
        return {
            "Success": False,
            "message": f"Order {order_id} was not found."
        }
    
    return {
        "Success": True,
        "order": order
    }

def extract_order_id(ticket:str)->str|None:
    """Extract order id from the ticket."""

    match=re.search(r"\bORD\d+\b",ticket,re.IGNORECASE)

    if match:
        return match.group(0).upper()

    return None
    