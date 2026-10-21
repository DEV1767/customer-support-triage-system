import uuid

from agent_2.graph.workflow import build_graph
from agent_2.tools.get_order import extract_order_id
from agent_2.tools.save_escalations import get_ticket, update_ticket


def main():
    app = build_graph()

    current_ticket_id = None
    waiting_for_order_id = False

    print("Customer Support System")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("You: ").strip()

        if message.lower() == "exit":
            print("Conversation ended.")
            break

        if not message:
            continue

        # Handle a follow-up when an order ID is missing
        if waiting_for_order_id and current_ticket_id:
            order_id = extract_order_id(message)

            if order_id:
                ticket = get_ticket(current_ticket_id)

                if ticket is None:
                    print("Assistant: I couldn't find your previous ticket.\n")
                    waiting_for_order_id = False
                    current_ticket_id = None
                    continue

                updated = update_ticket(current_ticket_id, order_id)

                if updated:
                    print(
                        f"Assistant: Thank you. I've added order {order_id} "
                        f"to ticket {current_ticket_id}. "
                        "Your ticket is pending human review.\n"
                    )
                    waiting_for_order_id = False
                else:
                    print(
                        "Assistant: I couldn't update the ticket. "
                        "Please try again or contact support.\n"
                    )

                continue

        # Process a new support ticket
        order_id = extract_order_id(message)

        initial_state = {
            "ticket": message,
            "ticket_id": None,
            "order_id": order_id,
            "category": "",
            "confidence": 0.0,
            "reasoning": "",
            "sentiment": "",
            "route": "",
            "response": "",
            "needs_human": False,
            "conversation_state": "new",
        }

        result = app.invoke(initial_state)

        current_ticket_id = result.get("ticket_id")

        print(f"\nAssistant: {result.get('response', '')}")

        if current_ticket_id:
            print(f"Ticket ID: {current_ticket_id}")

        # Check whether the saved ticket is waiting for an order ID
        if current_ticket_id:
            ticket = get_ticket(current_ticket_id)

            if ticket and ticket.get("status") == "awaiting_customer_information":
                waiting_for_order_id = True

        print()


if __name__ == "__main__":
    main()