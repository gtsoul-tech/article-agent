from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from models import ApempeArticle, ClassificationResult
from classify_with_llama import classify_with_llama

app = FastAPI(title="APEMPE Classification Agent - LLM")

from typing import List
from pydantic import BaseModel

class ClassificationResult(BaseModel):
    title: str
    category: str
    confidence: float
    timestamp: str

RESULTS: List[ClassificationResult] = []

@app.post("/classify")
def classify(article: ApempeArticle):
    result = classify_with_llama(article.title, article.body)

    entry = ClassificationResult(
        title=article.title,
        category=result["category"],
        confidence=result["confidence"],
        timestamp=article.timestamp
    )

    RESULTS.append(entry)
    return result

@app.get("/results")
def get_results():
    return RESULTS


app.mount("/", StaticFiles(directory="static", html=True), name="static")