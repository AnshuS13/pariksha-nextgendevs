from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import json
import requests


def verify_claim(claim: str) -> dict:
    """
    Verify claim using Tavily API directly
    """

    tavily_key = os.getenv("TAVILY_API_KEY")

    # STEP 1: Call Tavily API directly
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": tavily_key,
                "query": claim,
                "max_results": 3
            }
        )

        data = response.json()
        results = data.get("results", [])

    except Exception as e:
        return {
            "claim": claim,
            "verdict": "UNVERIFIED",
            "confidence": "LOW",
            "explanation": f"Search failed: {str(e)}",
            "sources": []
        }

    # STEP 2: Build context
    search_context = ""
    sources = []

    for i, r in enumerate(results):
        url = r.get("url", "")
        content = r.get("content", "")

        search_context += f"\nSource {i+1}: {url}\n{content}\n"
        sources.append(url)

    # STEP 3: LLM reasoning
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional fact-checker.

Return ONLY JSON:
{{
  "verdict": "VERIFIED or UNVERIFIED or CONTRADICTED",
  "confidence": "HIGH or MEDIUM or LOW",
  "explanation": "one line"
}}
"""),
        ("human", """Claim: {claim}

Search Results:
{context}
""")
    ])

    chain = prompt | llm

    try:
        res = chain.invoke({
            "claim": claim,
            "context": search_context
        })

        raw = res.content.strip()

        if raw.startswith("```"):
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

    except Exception as e:
        return {
            "claim": claim,
            "verdict": "UNVERIFIED",
            "confidence": "LOW",
            "explanation": f"LLM parsing failed: {str(e)}",
            "sources": sources
        }