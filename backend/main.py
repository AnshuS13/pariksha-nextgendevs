from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="PARIKSHA API",
    description="AI-Powered Newsroom Fact Verification",
    version="1.0.0"
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request format
class ArticleRequest(BaseModel):
    text: str

# Health check
@app.get("/")
def root():
    return {
        "status": "running",
        "project": "PARIKSHA"
    }

# Main endpoint
@app.post("/verify")
async def verify_article(request: ArticleRequest):
    return {
        "status": "success",
        "message": "Article received",
        "length": len(request.text)
    }