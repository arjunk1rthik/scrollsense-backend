from transformers import pipeline
from .scoring import compute_scores
from .summarizer import summarize_text

class LocalAI:
    def __init__(self):
        # Lightweight sentiment model that runs on CPU
        self.sentiment = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    async def analyze(self, text: str):
        # Summaries
        summary = summarize_text(text)

        # Sentiment result
        sent = self.sentiment(text[:512])[0]

        # Compute numeric mental health scores
        scores = compute_scores(text, sent)

        # Recommendations
        recommendations = []
        if scores["comparisonLevel"] > 0.6:
            recommendations.append("Limit exposure to content involving comparisons.")
        if scores["anxietyLevel"] > 0.6:
            recommendations.append("Take a break and practice mindfulness.")
        if scores["fomoTriggers"] > 0.6:
            recommendations.append("Unfollow accounts that make you feel left out.")
        if not recommendations:
            recommendations.append("Content appears healthy — keep up the good habits!")

        return {
            "summary": summary,
            "riskLevel": scores["riskLevel"],
            "recommendations": recommendations,
            **scores
        }
