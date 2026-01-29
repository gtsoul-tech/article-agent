from fastapi import FastAPI
from models import ApempeArticle, ClassificationResult
from classify_with_llama import classify_with_llama

app = FastAPI(title="APEMPE Classification Agent - LLM")

@app.post("/classify", response_model=ClassificationResult)
def classify(article: ApempeArticle):
    return classify_with_llama(article.title, article.body)
