from agent_2.graph.workflow import route_ticket
ticket = {
    "category": "billing",
    "confidence": 0.95,
    "sentiment": "calm"
}

result = route_ticket(ticket)

print("Selected route:", result)