**PARIKSHA — AI-Powered Newsroom Fact Verification System**

---

## 🎯 Problem Statement

In today’s digital ecosystem, **news spreads faster than it can be verified**.
Business journalism, in particular, deals with **data-heavy claims, financial statistics, and policy updates**, where even minor misinformation can lead to **serious economic and public impact**.

Despite this:

* Journalists **manually verify facts**, which is time-consuming
* Readers **consume unverified content**, often trusting unreliable sources
* There is **no real-time credibility scoring system** for news articles

As highlighted in the *AI-Native News Experience* challenge, current news delivery is **static, non-interactive, and lacks intelligence** 

👉 There is a need for an **AI-native layer that transforms raw articles into verified, explainable, and trustworthy insights**.

---

## 💡 Our Solution

**PARIKSHA** is an **AI-powered multi-agent fact verification system** that transforms any news article into a **structured credibility report**.

Instead of just reading news, users can:

✅ Extract factual claims automatically
✅ Verify them using real-time web data
✅ Understand source reliability
✅ Detect bias and sensationalism
✅ Get an overall credibility score

---

## ⚙️ How It Works (Multi-Agent Pipeline)

PARIKSHA follows a **modular AI-agent architecture**:

### 🔹 1. Claim Extraction Agent

* Uses LLM (Groq – Llama 3.1)
* Breaks article into **verifiable factual claims**

---

### 🔹 2. Verification Agent

* Uses **Tavily API** for real-time web search
* Cross-checks claims across multiple sources
* Classifies each claim as:

  * VERIFIED
  * CONTRADICTED
  * UNVERIFIED

---

### 🔹 3. Source Integrity Analyzer

* Detects:

  * Weak sources
  * Unnamed references
  * Missing citations
* Outputs **source quality report**

---

### 🔹 4. Bias Detection Agent

* Identifies:

  * Emotional language
  * Sensational claims
  * One-sided framing
* Outputs **bias score and explanation**

---

### 🔹 5. Scoring Engine

* Aggregates all signals into:

  * **Credibility Score (0–100)**
  * **Credibility Label (High / Moderate / Low)**

---

## 🧩 Key Features

* 🧠 Multi-agent AI system (not single LLM call)
* 🌐 Real-time verification using web search
* 📊 Structured outputs (JSON → UI-ready)
* ⚖️ Bias + source analysis (not just fact-checking)
* ⚡ Fast API-based backend (FastAPI)
* 🧪 Demo-ready interface (Streamlit)

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **LLM:** Groq (Llama 3.1)
* **Search:** Tavily API
* **Frontend:** Streamlit (React optional)
* **Architecture:** Multi-agent pipeline

---

## 📈 Impact & Innovation

### 🚨 Why this stands out:

Most solutions:
❌ Just summarize news
❌ Just classify fake/real

PARIKSHA:
✅ Breaks article into claims
✅ Verifies each claim independently
✅ Explains reasoning
✅ Adds bias + source intelligence

---

### 📊 Real-World Impact

* ⏱️ **Reduces verification time** from hours → seconds
* 📰 Helps journalists **validate articles before publishing**
* 👥 Helps readers **make informed decisions**
* 🏦 Useful for **financial/news platforms like ET Markets**

---

## 🔥 Future Scope

* Browser extension for live article verification
* Integration with newsroom CMS systems
* Portfolio-based personalized news credibility
* Multilingual fact-checking

---

## 🏁 Conclusion

PARIKSHA reimagines news consumption by adding an **AI-powered verification layer**, making journalism:

👉 More **transparent**
👉 More **trustworthy**
👉 More **intelligent**
