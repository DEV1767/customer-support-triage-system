import re
from agent_2.database import orders_collection
from langchain_core.tools import tool



@tool
def get_order(order_id: str) -> dict:
    """
    Retrieve order details from the database using an order ID (e.g., 'ORD1001').

    Call this tool whenever a customer provides an order ID or asks about
    order status, shipping, or order amount.
    """
    clean_id = order_id.strip().upper()

    try:
        order = orders_collection.find_one(
            {"order_id": clean_id},
            {"_id": 0}
        )

    except Exception as e:
        return {
            "success": False,
            "message": f"Database error while searching for order: {str(e)}"
        }

    if not order:
        return {
            "success": False,
            "message": f"Order {clean_id} was not found."
        }

    return {
        "success": True,
        "order": order
    }


def extract_order_id(ticket: str) -> str | None:
    """Extract order ID pattern (e.g. ORD1001) from text if present."""
    match = re.search(r"\bORD\d+\b", ticket, re.IGNORECASE)
    if match:
        return match.group(0).upper()
    return None