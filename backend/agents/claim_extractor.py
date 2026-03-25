from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import json

def extract_claims(article_text: str) -> list:
    """
    Takes a full article and returns a list of
    individual verifiable factual claims.
    """
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0  # 0 = consistent, not creative
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional fact-checker working for a newsroom.
        
Your job is to read a news article and extract every verifiable factual claim.

A verifiable factual claim is:
- A specific statistic (e.g. "India has 21 crore demat accounts")
- A named event (e.g. "The RBI raised rates in March 2025")
- A quote attributed to a specific person
- A specific date, number, or percentage
- A cause-and-effect statement about real events

Do NOT include:
- Opinions or editorials
- Future predictions
- Vague general statements

Return ONLY a JSON array of strings. No explanation. No markdown. No extra text.
Example output: ["Claim 1 here", "Claim 2 here", "Claim 3 here"]
"""),
        ("human", "Extract all verifiable factual claims from this article:\n\n{article}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"article": article_text})
    
    # Clean the response and parse JSON
    raw = response.content.strip()
    
    # Remove markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    try:
        claims = json.loads(raw)
        return claims
    except json.JSONDecodeError:
        # If JSON parsing fails, split by newline as fallback
        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        return lines