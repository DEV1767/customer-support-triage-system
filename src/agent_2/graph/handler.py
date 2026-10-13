from pathlib import Path
from agent_2.graph.state import TicketState

def billing_agent(state:TicketState)->dict:
    ticket=state["ticket"]

    responce=f"Billing request received: {ticket}"

    return {
        "responce":responce,
        "route":"billing_agent",
        "need_human":False,
    }

def tech_agent(state:TicketState)->dict:
    ticket=state["ticket"]

    responce=f"Techincal issue received:{ticket}"

    return {
        "respoce":responce,
        "route":"tech_agent",
        "need_human":False
    }