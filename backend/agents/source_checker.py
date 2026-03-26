from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import json
import re

def check_source_integrity(article_text, verdicts):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
       ("system", """You are a strict JSON generator.

Analyze source integrity.

Return ONLY VALID JSON (no text, no explanation):

{{
 "quote_issues": [],
 "statistic_issues": [],
 "secondary_source_issues": [],
 "overall_source_quality": "GOOD or MODERATE or POOR",
 "recommendation": "one sentence"
}}

If unsure, still return valid JSON.
"""),
        ("human", "{article}")
    ])

    res = (prompt | llm).invoke({"article": article_text})
    raw = res.content.strip()

    print("\nSOURCE RAW:", raw)

    raw = re.sub(r'```json', '', raw)
    raw = re.sub(r'```', '', raw)

    try:
        return json.loads(raw)
    except:
        return {
            "error": "Parsing failed",
            "raw_output": raw[:200]
        }