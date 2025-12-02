from fastapi import FastAPI
from pydantic import BaseModel
from AIService.ai_handler import LocalAI

app = FastAPI()
ai = LocalAI()

class AnalysisRequest(BaseModel):
    content: str

@app.get("/")
def root():
    return {"status": "ScrollSense AI Backend is running"}

@app.post("/analyze")
async def analyze(req: AnalysisRequest):
    result = await ai.analyze(req.content)
    return result
