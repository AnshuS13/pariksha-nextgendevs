from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import json
import re

def extract_claims(article_text: str):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional fact-checker.

Extract ONLY strong factual claims.

STRICT RULES:
- Return ONLY a JSON array
- No explanation
- Max 5 claims

Example:
["India GDP grew by 8.2%", "RBI raised repo rate"]
"""),
        ("human", "{article}")
    ])

    res = (prompt | llm).invoke({"article": article_text})
    raw = res.content.strip()

    # Clean markdown
    raw = re.sub(r'```json', '', raw)
    raw = re.sub(r'```', '', raw)

    # Extract JSON safely
    start = raw.find("[")
    end = raw.rfind("]") + 1

    if start != -1 and end != -1:
        raw = raw[start:end]

    try:
        claims = json.loads(raw)
        return [c.strip() for c in claims if len(c.strip()) > 25][:5]
    except:
        return []