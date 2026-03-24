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
    text = request.text.lower()

    print(f"\n--- New Request ---")
    print(f"Length: {len(request.text)} characters")
    print(f"Preview: {request.text[:100]}...")

    verdicts = []

    # Simple mock AI logic
    if "india" in text:
        verdicts.append({
            "claim": "India related claim",
            "verdict": "Likely True",
            "confidence": "85%",
            "explanation": "India is widely recognized as a democratic country."
        })

    if "moon" in text:
        verdicts.append({
            "claim": "Moon related claim",
            "verdict": "Suspicious",
            "confidence": "60%",
            "explanation": "This claim requires scientific verification."
        })

    if len(verdicts) == 0:
        verdicts.append({
            "claim": "General statement",
            "verdict": "Unverified",
            "confidence": "50%",
            "explanation": "No strong data found (mock AI response)."
        })

    credibility_score = 80 if "india" in text else 50

    return {
        "status": "success",
        "message": "AI analysis complete",
        "article_length": len(request.text),
        "claims_found": len(verdicts),
        "verdicts": verdicts,
        "credibility_score": credibility_score
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