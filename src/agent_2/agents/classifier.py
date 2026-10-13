import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()

API_URL = "https://openrouter.ai/api/alpha/decisions"
MODEL = os.getenv("JEV_MODEL", "typesafe/jev-1.13-20260917")
API_KEY = os.getenv("OPENROUTER_API_KEY")

THRESHOLD = 0.6


def classify_ticket(ticket: str) -> dict:
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing in .env")

    payload = {
        "model": MODEL,
        "state": {
            "ticket": ticket,
            "instructions": """
                Classify customer support tickets objectively.
                Consider the actual issue, not just individual keywords.
                Billing: payments, refunds, invoices, subscriptions.
                Tech: bugs, errors, login and technical problems.
                General: other requests.
                Angry: clear frustration, anger or hostility.
                Calm: neutral, polite or non-angry messages.
            """
        },
        "questions": {
            "billing": {
                "type": "choice",
                "instructions": (
                    "Does this ticket primarily concern billing, "
                    "payments, refunds, invoices or subscriptions?"
                ),
                "criteria": {
                    "relevant": "The ticket is primarily about billing.",
                    "not_relevant": "The ticket is not primarily about billing."
                }
            },
            "tech": {
                "type": "choice",
                "instructions": (
                    "Does this ticket primarily concern technical "
                    "problems, bugs, errors or login issues?"
                ),
                "criteria": {
                    "relevant": "The ticket is primarily about a technical problem.",
                    "not_relevant": "The ticket is not primarily about a technical problem."
                }
            },
            "general": {
                "type": "choice",
                "instructions": (
                    "Is this ticket a general support request "
                    "rather than a billing or technical issue?"
                ),
                "criteria": {
                    "relevant": "The ticket is a general support request.",
                    "not_relevant": "The ticket is primarily billing or technical."
                }
            },
            "angry": {
                "type": "choice",
                "instructions": (
                    "Does the customer express clear anger, "
                    "hostility or strong frustration?"
                ),
                "criteria": {
                    "relevant": "The customer expresses anger or strong frustration.",
                    "not_relevant": "The customer does not express clear anger."
                }
            }
        }
    }

    # Retry failed requests with exponential backoff.
    for attempt in range(3):
        try:
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()
            break

        except (requests.RequestException, ValueError):
            if attempt == 2:
                raise

            time.sleep(2 ** attempt)

    answers = data.get("answers", {})

    def get_score(question_name: str) -> float:
        answer = answers.get(question_name, {})
        probabilities = answer.get("probabilities", {})

        score = probabilities.get("relevant")

        if score is None:
            score = 1.0 if answer.get("choice") == "relevant" else 0.0

        score = float(score)

        if not 0.0 <= score <= 1.0:
            raise ValueError(f"Invalid JEV score for {question_name}")

        return score

    # Get category scores.
    scores = {
        "billing": get_score("billing"),
        "tech": get_score("tech"),
        "general": get_score("general")
    }

    # Select the category with the highest score.
    category = max(scores, key=scores.get)
    confidence = scores[category]

    # Apply the required confidence threshold.
    if confidence < THRESHOLD:
        category = "general"

    # Determine sentiment.
    sentiment = "angry" if get_score("angry") >= 0.5 else "calm"

    # Explain the classification without inventing model reasoning.
    reasoning = (
        f"JEV category scores: {scores}. "
        f"Selected category: {category}. "
        f"Classification confidence: {confidence:.2f}."
    )

    result = {
        "category": category,
        "confidence": confidence,
        "reasoning": reasoning,
        "sentiment": sentiment
    }

    print("Classification:", result)

    return result