from pathlib import Path
from agent_2.graph.state import TicketState

def billing_agent(state: TicketState) -> dict:
    ticket = state["ticket"]

    response = f"Billing request received: {ticket}"

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
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "escalation.md"

    with file_path.open("a", encoding="utf-8") as file:
        file.write(
            f"\n## Support Ticket\n\n"
            f"- **Ticket:** {state['ticket']}\n"
            f"- **Category:** {state['category']}\n"
            f"- **Confidence:** {state['confidence']}\n"
            f"- **Sentiment:** {state['sentiment']}\n"
            f"- **Reasoning:** {state['reasoning']}\n"
            f"- **Status:** Requires human review\n\n---\n"
        )
    
    return {
        "response": "Your ticket has been escalated to human Support.",
        "route": "human_escalation",
        "needs_human": True
    }