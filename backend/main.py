from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from agents.claim_extractor import extract_claims
from agents.web_verifier import verify_claim
import os

# Load .env correctly
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Create app
app = FastAPI(
    title="PARIKSHA API",
    description="AI-Powered Newsroom Fact Verification",
    version="1.0.0"
)

# CORS (for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ArticleRequest(BaseModel):
    text: str

# Root endpoint
@app.get("/")
def root():
    return {
        "status": "running",
        "project": "PARIKSHA",
        "team": "NextGenDevs — Anshu, Aman, Aashirvad"
    }

# ✅ ONLY ONE VERIFY ENDPOINT (REAL AI PIPELINE)
@app.post("/verify")
async def verify_article(request: ArticleRequest):

    print(f"\n--- New Verification Request ---")
    print(f"Article length: {len(request.text)} characters")

    # STEP 1: Extract claims
    try:
        claims = extract_claims(request.text)
        print(f"Extracted claims: {claims}")
    except Exception as e:
        return {
            "status": "error",
            "message": f"Claim extraction failed: {str(e)}"
        }

    # Limit claims (performance)
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

    print(f"Final Score: {score}%")

    # STEP 4: Response
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