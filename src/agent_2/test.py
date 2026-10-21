from agent_2.tools.get_order import extract_order_id

tickets = [
    "Please refund order ORD1001.",
    "Can you check ORD1002?",
    "I need a refund for my purchase.",
]

for ticket in tickets:
    order_id = extract_order_id(ticket)

    print(f"Ticket: {ticket}")
    print(f"Order ID: {order_id}")
    print("-" * 40)