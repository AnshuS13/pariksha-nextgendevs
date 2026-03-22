from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os

# FIX: ensure .env loads correctly from backend folder
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = FastAPI(
    title="PARIKSHA API",
    description="AI-Powered Newsroom Fact Verification",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {
        "status": "running",
        "project": "PARIKSHA",
        "team": "NextGenDevs — Anshu, Aman, Aashirvad"
    }

@app.post("/verify")
async def verify_article(request: ArticleRequest):
    print(f"\n--- New Request ---")
    print(f"Length: {len(request.text)} characters")
    print(f"Preview: {request.text[:100]}...")
    return {
        "status": "success",
        "message": "Article received",
        "article_length": len(request.text),
        "claims_found": 0,
        "verdicts": [],
        "credibility_score": 0
    }

# Test your Groq key here
@app.get("/test-ai")
async def test_ai():
    from langchain_groq import ChatGroq
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )
        response = llm.invoke(
            "Say PARIKSHA is ready and nothing else."
        )
        return {
            "status": "success",
            "response": response.content
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }