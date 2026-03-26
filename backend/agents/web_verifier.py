from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import json
import requests

def verify_claim(claim: str):

    tavily_key = os.getenv("TAVILY_API_KEY")

    # SEARCH
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": tavily_key,
                "query": claim,
                "max_results": 3
            }
        )
        results = response.json().get("results", [])
    except:
        return {"claim": claim, "verdict": "UNVERIFIED", "confidence": "LOW", "explanation": "Search failed", "sources": []}

    # CONTEXT
    search_context = ""
    sources = []

    for i, r in enumerate(results):
        url = r.get("url", "")
        content = r.get("content", "")[:500]

        search_context += f"\nSource {i+1}: {url}\n{content}\n"
        sources.append(url)

    search_context = search_context[:1500]

    # LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a strict fact-checker.

Rules:
- VERIFIED → strong agreement
- CONTRADICTED → explicitly proven false
- UNVERIFIED → no evidence OR unclear

IMPORTANT:
- Missing info ≠ contradiction
- Lack of proof → UNVERIFIED
- Be conservative

Return JSON:
{{
 "verdict": "VERIFIED or UNVERIFIED or CONTRADICTED",
 "confidence": "HIGH or MEDIUM or LOW",
 "explanation": "short reason"
}}
"""),
        ("human", "Claim: {claim}\n\n{context}")
    ])

    try:
        res = (prompt | llm).invoke({
            "claim": claim,
            "context": search_context
        })

        raw = res.content.strip()

        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        parsed = json.loads(raw)

        return {
            "claim": claim,
            "verdict": parsed.get("verdict", "UNVERIFIED"),
            "confidence": parsed.get("confidence", "LOW"),
            "explanation": parsed.get("explanation", ""),
            "sources": sources
        }

    except:
        return {
            "claim": claim,
            "verdict": "UNVERIFIED",
            "confidence": "LOW",
            "explanation": "Parsing failed",
            "sources": sources
        }