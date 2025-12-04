# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class AnalyzeRequest(BaseModel):
    content: str


class EnhancedContentAnalysis(BaseModel):
    summary: str
    riskLevel: str
    comparisonLevel: float
    selfEsteemImpact: float
    depressionRisk: float
    anxietyLevel: float
    fomoTriggers: float
    cyberbullyingRisk: float
    addictivePotential: float
    recommendations: List[str]


def basic_score(content: str, keywords: List[str]) -> float:
    """Very simple heuristic scoring: 0.0–1.0 based on keyword hits."""
    text = content.lower()
    if not text.strip():
        return 0.0

    hits = sum(text.count(k) for k in keywords)
    # cap at 1.0
    return min(1.0, hits / 5.0)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/analyze", response_model=EnhancedContentAnalysis)
async def analyze(request: AnalyzeRequest):
    text = request.content

    # Very simple keyword-based “AI”
    negative_words = ["sad", "depressed", "hate", "worthless", "bad", "ugly"]
    anxiety_words = ["nervous", "anxious", "stressed", "panic", "worried"]
    fomo_words = ["everyone", "left out", "missing out", "fomo"]
    bullying_words = ["loser", "kill yourself", "stupid", "idiot", "bully"]
    comparison_words = ["better than me", "perfect body", "richer", "skinnier"]

    depression = basic_score(text, negative_words)
    anxiety = basic_score(text, anxiety_words)
    fomo = basic_score(text, fomo_words)
    cyberbullying = basic_score(text, bullying_words)
    comparison = basic_score(text, comparison_words)

    # self-esteem impact: high when lots of comparison / negative words
    self_esteem = min(1.0, (comparison + depression) / 2.0)

    addictive = basic_score(
        text,
        ["scroll", "swipe", "hooked", "hours", "can’t stop", "addicted"],
    )

    # overall risk level
    max_risk = max(depression, anxiety, fomo, cyberbullying, self_esteem, addictive)
    if max_risk > 0.7:
        risk_level = "high"
    elif max_risk > 0.3:
        risk_level = "medium"
    else:
        risk_level = "low"

    # simple summary
    summary_parts = []
    if depression > 0.3:
        summary_parts.append("The content includes language that may relate to sadness or low mood.")
    if anxiety > 0.3:
        summary_parts.append("There are phrases that may be associated with anxiety or stress.")
    if comparison > 0.3:
        summary_parts.append("The content suggests a lot of comparison to others.")
    if cyberbullying > 0.3:
        summary_parts.append("Some phrases look like possible cyberbullying or harassment.")
    if not summary_parts:
        summary_parts.append("The content does not strongly indicate negative mental health risks.")

    summary = " ".join(summary_parts)

    # recommendations
    recs = [
        "Take a short break from scrolling and check in with how you feel.",
        "Remember that social media often shows a filtered version of people’s lives.",
        "Talk to a trusted adult or friend if something online is upsetting you.",
        "Consider muting or unfollowing accounts that make you feel worse about yourself.",
    ]

    if cyberbullying > 0.3:
        recs.append("If you experience cyberbullying, save evidence and talk to a trusted adult or school counselor.")
    if depression > 0.6 or anxiety > 0.6:
        recs.append("If these feelings are intense or long-lasting, consider reaching out to a mental health professional.")

    return EnhancedContentAnalysis(
        summary=summary,
        riskLevel=risk_level,
        comparisonLevel=comparison,
        selfEsteemImpact=self_esteem,
        depressionRisk=depression,
        anxietyLevel=anxiety,
        fomoTriggers=fomo,
        cyberbullyingRisk=cyberbullying,
        addictivePotential=addictive,
        recommendations=recs,
    )
