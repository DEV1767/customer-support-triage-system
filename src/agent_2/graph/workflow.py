from langgraph.graph import StateGraph,START,END
from agent_2.graph.state import TicketState
from agent_2.node import classify_node
from agent_2.graph.handler import billing_agent,tech_agent,human_escalation



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
    graph.add_node("billing_agent",billing_agent)
    graph.add_node("tech_agent",tech_agent)
    graph.add_node("human_escalation",human_escalation)


    graph.set_entry_point("classifiy")

    graph.add_conditional_edges(
        "classifiy",
        route_ticket,
        {
            "billing_agent":"billing_agent",
            "tech_agent":"tech_agent",
            "human_escalation":"human_escalation"
        },
    )

    graph.add_edge("billing_agent",END)
    graph.add_edge("tech_agent",END)
    graph.add_edge("human_escalation",END)


    return graph.compile()
    