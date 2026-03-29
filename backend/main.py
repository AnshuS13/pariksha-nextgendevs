from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

from agents.claim_extractor import extract_claims
from agents.web_verifier import verify_claim
from agents.source_checker import check_source_integrity
from agents.bias_analyzer import analyze_bias

# ✅ NEW (Day 4 Task 1)
from database import init_db, log_verification, get_all_verifications

# Load .env
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Create app
app = FastAPI(
    title="PARIKSHA API",
    description="AI-Powered Newsroom Fact Verification System",
    version="1.0.0"
)

# ✅ Initialize DB (Day 4)
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleRequest(BaseModel):
    text: str

# Root
@app.get("/")
def root():
    return {
        "status": "running",
        "project": "PARIKSHA",
        "team": "NextGenDevs — Anshu, Aman, Aashirvad"
    }

# VERIFY ENDPOINT
@app.post("/verify")
async def verify_article(request: ArticleRequest):

    print("\n=== NEW REQUEST ===")

    # STEP 1: CLAIMS
    claims = extract_claims(request.text)
    claims = claims[:5]

    print("Claims:", claims)

    # STEP 2: VERIFY
    verdicts = []
    for claim in claims:
        verdicts.append(verify_claim(claim))

    # STEP 3: SOURCE + BIAS
    source_report = check_source_integrity(request.text, verdicts)
    bias_report = analyze_bias(request.text)

    # STEP 4: SCORING
    verified_count = sum(1 for v in verdicts if v["verdict"] == "VERIFIED")
    contradicted_count = sum(1 for v in verdicts if v["verdict"] == "CONTRADICTED")
    unverified_count = len(verdicts) - verified_count - contradicted_count

    if len(verdicts) > 0:
        base_score = (verified_count / len(verdicts)) * 100

        # softer penalties
        score = int(base_score - contradicted_count * 5 - unverified_count * 2)
        score = max(10, score)
    else:
        score = 0

    # Credibility label
    if score >= 75:
        label = "HIGH"
    elif score >= 45:
        label = "MODERATE"
    else:
        label = "LOW"

    # ✅ NEW (Day 4 Task 1 — Audit Logging)
    try:
        log_verification(request.text, {
            "article_length": len(request.text),
            "claims_found": len(claims),
            "credibility_score": score,
            "credibility_label": label,
            "verified_count": verified_count,
            "contradicted_count": contradicted_count,
            "unverified_count": unverified_count,
            "source_report": source_report,
            "bias_report": bias_report
        })
        print("Logged to audit database.")
    except Exception as e:
        print(f"Logging failed (non-critical): {e}")

    # FINAL RESPONSE
    return {
        "status": "success",
        "article_length": len(request.text),
        "claims_found": len(claims),
        "credibility_score": score,
        "credibility_label": label,
        "verified_count": verified_count,
        "contradicted_count": contradicted_count,
        "unverified_count": unverified_count,
        "verdicts": verdicts,
        "source_report": source_report,
        "bias_report": bias_report
    }


# ✅ NEW ENDPOINT (Day 4 Task 1)
@app.get("/history")
def get_history():
    """Returns past verification runs for the audit dashboard."""
    try:
        records = get_all_verifications()
        return {"status": "success", "records": records}
    except Exception as e:
        return {"status": "error", "message": str(e)}