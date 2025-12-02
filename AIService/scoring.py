import re

def compute_scores(text, sentiment):
    text_lower = text.lower()

    comparison_keywords = ["better than me", "perfect life", "success", "rich", "famous"]
    anxiety_keywords = ["anxiety", "stress", "scared", "panic"]
    depression_keywords = ["sad", "empty", "depressed", "worthless"]
    fomo_keywords = ["left out", "everybody", "missing out"]
    cyberbullying_keywords = ["hate you", "kill yourself", "loser"]

    def count(words):
        return sum(1 for w in words if w in text_lower)

    # Compute raw values
    comparison = min(count(comparison_keywords) * 0.2, 1.0)
    anxiety = min(count(anxiety_keywords) * 0.25, 1.0)
    depression = min(count(depression_keywords) * 0.25, 1.0)
    fomo = min(count(fomo_keywords) * 0.3, 1.0)
    cyber = min(count(cyberbullying_keywords) * 0.4, 1.0)

    # Combine
    raw_risk = (anxiety + depression + cyber + comparison + fomo) / 5

    if raw_risk > 0.6:
        risk = "high"
    elif raw_risk > 0.3:
        risk = "medium"
    else:
        risk = "low"

    return {
        "comparisonLevel": comparison,
        "anxietyLevel": anxiety,
        "depressionRisk": depression,
        "fomoTriggers": fomo,
        "cyberbullyingRisk": cyber,
        "addictivePotential": 0.4,  # static baseline score
        "selfEsteemImpact": (comparison + depression) / 2,
        "riskLevel": risk
    }
