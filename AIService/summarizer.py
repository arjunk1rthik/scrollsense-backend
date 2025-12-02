from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def summarize_text(text: str) -> str:
    text = text[:1000]
    result = summarizer(text, max_length=80, min_length=25, do_sample=False)
    return result[0]["summary_text"]
