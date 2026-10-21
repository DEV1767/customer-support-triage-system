
import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv(
    "API_URL",
    "https://openrouter.ai/api/alpha/decisions",
)

MODEL = (
    os.getenv("OPENROUTER_MODEL")
    or os.getenv("JEV_MODEL", "typesafe/jev-1.13-20260917")
)

API_KEY = os.getenv("OPENROUTER_API_KEY")

THRESHOLD = 0.6


def classify_ticket(ticket: str) -> dict:
    """Classify a support ticket using JEV."""

    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing in .env")

    payload = {
        "model": MODEL,
        "state": {
            "ticket": ticket,
            "instructions": """
                Classify customer support tickets objectively.

                Billing: payments, refunds, invoices, subscriptions,
                order status, and payment status.

                Tech: bugs, errors, login problems, and technical issues.

                General: requests unrelated to billing or technical issues.

                Angry: clear frustration, anger, or hostility.
                Calm: neutral or polite messages.
            """,
        },
        "questions": {
            "billing": {
                "type": "choice",
                "instructions": (
                    "Does this ticket concern billing, payments, refunds, "
                    "invoices, subscriptions, or checking an order or "
                    "payment status?"
                ),
                "criteria": {
                    "relevant": (
                        "The customer asks about billing, a payment, refund, "
                        "invoice, subscription, order status, or payment status."
                    ),
                    "not_relevant": (
                        "The ticket is unrelated to billing, payments, refunds, "
                        "invoices, subscriptions, or order and payment status."
                    ),
                },
            },
            "tech": {
                "type": "choice",
                "instructions": (
                    "Does this ticket concern a technical problem, "
                    "software bug, error, or login issue?"
                ),
                "criteria": {
                    "relevant": (
                        "The customer reports a technical problem, "
                        "software bug, error, or login issue."
                    ),
                    "not_relevant": (
                        "The ticket does not concern a technical problem."
                    ),
                },
            },
            "general": {
                "type": "choice",
                "instructions": (
                    "Is this a general support request unrelated to "
                    "billing or technical problems?"
                ),
                "criteria": {
                    "relevant": (
                        "The request is unrelated to billing, payments, "
                        "order status, or technical problems."
                    ),
                    "not_relevant": (
                        "The request concerns billing or a technical problem."
                    ),
                },
            },
            "angry": {
                "type": "choice",
                "instructions": (
                    "Does the customer express clear anger, hostility, "
                    "or strong frustration?"
                ),
                "criteria": {
                    "relevant": (
                        "The customer clearly expresses anger, hostility, "
                        "or strong frustration."
                    ),
                    "not_relevant": (
                        "The customer does not express clear anger or hostility."
                    ),
                },
            },
        },
    }

    # Retry failed requests with exponential backoff.
    for attempt in range(3):
        try:
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()
            break

        except (requests.RequestException, ValueError):
            if attempt == 2:
                raise

            time.sleep(2**attempt)

    answers = data.get("answers", {})

    def get_score(question_name: str) -> float:
        """Extract and validate a JEV relevance score."""

        answer = answers.get(question_name, {})
        probabilities = answer.get("probabilities", {})

        score = probabilities.get("relevant")

        if score is None:
            choice = answer.get("choice")

            if choice == "relevant":
                score = 1.0
            elif choice == "not_relevant":
                score = 0.0
            else:
                raise ValueError(
                    f"Missing or invalid JEV answer for {question_name}: "
                    f"{answer}"
                )

        score = float(score)

        if not 0.0 <= score <= 1.0:
            raise ValueError(
                f"Invalid JEV score for {question_name}: {score}"
            )

        return score

    # Obtain scores for all three categories.
    scores = {
        "billing": get_score("billing"),
        "tech": get_score("tech"),
        "general": get_score("general"),
    }

    # Select the category with the highest score.
    category = max(scores, key=scores.get)
    confidence = scores[category]

    # Apply the required confidence threshold.
    if confidence < THRESHOLD:
        category = "general"

    # Classify sentiment independently.
    sentiment = "angry" if get_score("angry") >= 0.5 else "calm"

    reasoning = (
        f"JEV category scores: {scores}. "
        f"Selected category: {category}. "
        f"Classification score: {confidence:.2f}."
    )

    result = {
        "category": category,
        "confidence": confidence,
        "reasoning": reasoning,
        "sentiment": sentiment,
    }

    print("Classification:", result)

    return result

