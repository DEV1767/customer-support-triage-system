from langgraph.graph import StateGraph,START,END
from agent_2.graph.state import TicketState
from agent_2.node import classify_node

def route_ticket(state:TicketState) -> str:
    
    if state["sentiment"] == "angry":
        return "human_escalation"

   
    if state["confidence"] < 0.6:
        return "human_escalation"

   
    if state["category"] == "general":
        return "human_escalation"

  
    if state["category"] == "billing":
        return "billing_agent"

   
    if state["category"] == "tech":
        return "tech_agent"

   
    return "human_escalation"


def build_graph():
    graph=StateGraph(TicketState)

    graph.add_node("classifiy",classify_node)
    graph.set_entry_point("classifiy")

    graph.add_conditional_edges(
        "classifiy",
        route_ticket,
        {
            "billing_agent":END,
            "tech_agent":END,
            "human_escalation":END
        },
    )

    return graph.compile()
    