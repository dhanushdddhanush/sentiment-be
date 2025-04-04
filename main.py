import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")


def authenticate_client():
    return TextAnalyticsClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))

client = authenticate_client()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Sentiment Analysis API"}

@app.post("/sentiment/")
async def analyze_sentiment(request: SentimentRequest):
    response = client.analyze_sentiment([request.text])[0]
    return {
        "sentiment": response.sentiment,
        "confidence_scores": response.confidence_scores
    }

# changed my server to this: uvicorn filename:app --reload-8091
