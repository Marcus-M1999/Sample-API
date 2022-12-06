import logging
import os

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import asyncio
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

model_path = "./distilbert-base-uncased-finetuned-sst2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    return_all_scores=True,
)

logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://redis:6379"
app = FastAPI()


@app.on_event("startup")
def startup():
    redis = aioredis.from_url('redis://redis:6379', encoding = 'utf8', decode_responses = True)
    FastAPICache.init(RedisBackend(redis), prefix = 'fastapi-cache')


class SentimentRequest(BaseModel):
    label: str
    score: float


class Sentiment(BaseModel):
    text: list[str]


class SentimentResponse(BaseModel):
    predictions: {list[Sentiment]}
    # ... [Sentiment]


@app.post("/predict", response_model=SentimentResponse)
@cache(expire=30)
def predict(sentiments: SentimentRequest):
    return {"predictions": classifier(sentiments.text)}


@app.get("/health")
async def health():
    return {"status": "healthy"}
