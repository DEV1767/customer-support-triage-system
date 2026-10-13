from agent_2.agents.classifier import classify_ticket
from agent_2.graph.state import TicketState


def classify_node(state:TicketState)->dict:
    result=classify_ticket(state["ticket"])

    return {
        "category":result["category"],
        "confidence":result["confidence"],
        "sentiment":result["sentiment"],
        "reasoning":result["reasoning"]
    }