from agent_2.graph.workflow import build_graph

def main():
    app = build_graph()

    ticket = input("Enter customer support ticket: ")
    initial_state = {
        "ticket": ticket,
        "category": "",
        "confidence": 0.0,
        "reasoning": "",
        "sentiment": "",
        "route": "",
        "response": "",
        "needs_human": False
    }

    result = app.invoke(initial_state)

    print("\n========== SUPPORT RESULT ==========")
    print(f"Ticket: {result['ticket']}")
    print(f"Category: {result['category']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Route: {result['route']}")
    print(f"Response: {result['response']}")
    print(f"Needs human: {result['needs_human']}")
    print("====================================")


if __name__ == "__main__":
    main()