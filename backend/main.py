from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="PARIKSHA API",
    description="AI-Powered Newsroom Fact Verification",
    version="1.0.0"
)

# Allow Aman's Streamlit to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what data frontend sends us
class ArticleRequest(BaseModel):
    text: str

# Health check — visit localhost:8000/
@app.get("/")
def root():
    return {
        "status": "running",
        "project": "PARIKSHA",
        "team": "NextGenDevs — Anshu, Aman, Aashirvad"
    }

# Main endpoint — Aman connects to this
@app.post("/verify")
async def verify_article(request: ArticleRequest):
    print(f"\n--- New Request ---")
    print(f"Length: {len(request.text)} characters")
    print(f"Preview: {request.text[:100]}...")

    # Day 1 — just acknowledge receipt
    # Day 2 — real agent logic goes here
    return {
        "status": "success",
        "message": "Article received",
        "article_length": len(request.text),
        "claims_found": 0,
        "verdicts": [],
        "credibility_score": 0
    }

# Test OpenAI key — visit localhost:8000/test-ai
@app.get("/test-ai")
async def test_ai():
    from langchain_openai import ChatOpenAI
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        response = llm.invoke("Say PARIKSHA is ready and nothing else.")
        return {"status": "success", "response": response.content}
    except Exception as e:
        return {"status": "error", "error": str(e)}