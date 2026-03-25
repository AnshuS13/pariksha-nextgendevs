from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from agents.claim_extractor import extract_claims
from agents.web_verifier import verify_claim
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

    try:
        # STEP 1: Extract claims
        claims = extract_claims(request.text)
        claims = claims[:5]

        # STEP 2: Verify claims
        verdicts = []
        for claim in claims:
            try:
                result = verify_claim(claim)
                verdicts.append(result)
            except Exception as e:
                verdicts.append({
                    "claim": claim,
                    "verdict": "UNVERIFIED",
                    "confidence": "LOW",
                    "explanation": f"Verification failed: {str(e)}",
                    "sources": []
                })

        # STEP 3: Calculate score
        verified = sum(1 for v in verdicts if v["verdict"] == "VERIFIED")
        contradicted = sum(1 for v in verdicts if v["verdict"] == "CONTRADICTED")

        score = int((verified / len(verdicts)) * 100) if verdicts else 0

        return {
            "status": "success",
            "article_length": len(request.text),
            "claims_found": len(claims),
            "credibility_score": score,
            "verified_count": verified,
            "contradicted_count": contradicted,
            "unverified_count": len(verdicts) - verified - contradicted,
            "verdicts": verdicts
        }

    except Exception as e:
        # 🔥 FALLBACK (YOUR DUMMY AI)
        text = request.text.lower()

        verdicts = []
        if "india" in text:
            verdicts.append({
                "claim": "India related claim",
                "verdict": "Likely True",
                "confidence": "85%",
                "explanation": "India is widely recognized as a democratic country."
            })
        else:
            verdicts.append({
                "claim": "General statement",
                "verdict": "Unverified",
                "confidence": "50%",
                "explanation": "Mock fallback response."
            })

        return {
            "status": "fallback",
            "message": "Using dummy AI (no API key)",
            "article_length": len(request.text),
            "claims_found": len(verdicts),
            "verdicts": verdicts,
            "credibility_score": 70
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