from fastapi import FastAPI
from models import ApempeArticle, ClassificationResult
from classify_with_tinnyllama import classify_with_tinnyllama

app = FastAPI(title="APEMPE Classification Agent - LLM")

@app.post("/classify", response_model=ClassificationResult)
def classify(article: ApempeArticle):
    return classify_with_tinnyllama(article.title, article.body)
