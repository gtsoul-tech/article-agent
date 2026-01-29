from pydantic import BaseModel
from typing import Literal

class ApempeArticle(BaseModel):
    source: Literal["apembe"]
    title: str
    body: str
    timestamp: str

class ClassificationResult(BaseModel):
    category: Literal[
        "nationwide_news",
        "larisa_thessaly_news"
    ]
    confidence: float
