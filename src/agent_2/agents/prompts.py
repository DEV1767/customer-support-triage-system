CLASSIFIER_PROMPT = """
Classify the customer support ticket.

Categories: billing, tech, general.
Sentiments: calm, angry.

Return:
- category
- confidence (0 to 1)
- reasoning
- sentiment

Rules:
- If confidence < 0.6, category = general.
- Never invent information.
"""