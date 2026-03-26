from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
import json
import re

def analyze_bias(article_text):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a strict JSON generator.

Analyze bias in the article.

Return ONLY VALID JSON:

{{
 "bias_score": number between 0-100,
 "bias_type": "NONE or SENSATIONAL or POLITICAL",
 "emotional_language_found": [],
 "one_sided_framing": true or false,
 "flagged_sentences": [],
 "overall_assessment": "one sentence"
}}

No explanation. Only JSON.
"""),
        ("human", "{article}")
    ])

    res = (prompt | llm).invoke({"article": article_text})
    raw = res.content.strip()

    print("\nBIAS RAW:", raw)

    raw = re.sub(r'```json', '', raw)
    raw = re.sub(r'```', '', raw)

    try:
        return json.loads(raw)
    except:
        return {
            "error": "Parsing failed",
            "raw_output": raw[:200]
        }