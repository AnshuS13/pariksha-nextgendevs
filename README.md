# 🧠 PARIKSHA AI  
### AI-Powered Newsroom Fact Verification System  

---

## 🚨 Problem Statement

In today’s fast-paced digital media landscape, misinformation spreads faster than it can be verified. Journalists and editors often face:

- Time-consuming manual fact-checking processes  
- Difficulty verifying multiple claims within an article  
- Lack of tools to detect bias and unreliable sources  
- No structured audit trail for verification decisions  

This leads to:
- Spread of fake or misleading news 
- Reduced trust in journalism  
- Increased editorial risk  

---

## 💡 Our Solution

**PARIKSHA AI** is an intelligent newsroom assistant that automates the process of fact verification.

It:
- Extracts key claims from articles  
- Verifies them using real-time web sources  
- Assigns a credibility score  
- Detects bias and weak sources  
- Maintains an audit log of all verifications  

---

## 🎯 Hackathon Alignment

This project aligns with the **ET Gen AI Hackathon problem statement** focused on:

> Leveraging AI to improve newsroom workflows, enhance credibility, and combat misinformation.

PARIKSHA directly addresses:
- Automated verification  
- AI-assisted journalism  
- Trust and transparency in media  

---

## ⚙️ How It Works (Flow)

### 🔁 End-to-End Pipeline

1. **User Input**
   - Journalist inputs an article

2. **Claim Extraction**
   - AI extracts key factual claims

3. **Verification Engine**
   - Each claim is verified using web search + LLM reasoning

4. **Source Analysis**
   - Detects:
     - Weak sources  
     - Unnamed references  
     - Statistical inconsistencies  

5. **Bias Detection**
   - Identifies:
     - Emotional language  
     - Sensational tone  
     - One-sided framing  

6. **Scoring System**
   - Generates:
     - Credibility Score (0–100)  
     - Label (HIGH / MODERATE / LOW)

7. **Audit Logging**
   - Stores every verification for traceability

---

## 🔄 Architecture
<img width="771" height="451" alt="image" src="https://github.com/user-attachments/assets/733512de-a79a-4b83-98a2-6db13823befd" />

---

## 🧠 Key Features

- ✅ Multi-claim extraction  
- ✅ Real-time verification using web sources  
- ✅ Credibility scoring system  
- ✅ Source integrity analysis  
- ✅ Bias detection engine  
- ✅ Audit logging (`/history` endpoint)  
- ✅ Structured, explainable outputs  

---

## 🆚 How It’s Different from Existing Tools

### Existing Tools (e.g., Bloomberg, Fact-check platforms)

- Mostly manual workflows  
- Focus on post-publication verification  
- Limited bias detection  
- No unified scoring system  
- No transparent audit trail  

---

### 🚀 PARIKSHA AI Advantage

|          Feature          | Traditional Tools | PARIKSHA |
|-------------|-------------|---------|---------|----|-----|
| Claim-level verification  |        ❌         |   ✅    |
| Real-time AI reasoning    |        ❌         |   ✅    |
| Bias detection            |        ❌         |   ✅    |
| Credibility scoring       |        ❌         |   ✅    |
| Audit logging             |        ❌         |   ✅    |
| Automation                |      Partial      |   Full   |

---

## 🛠️ Tech Stack

### Backend
- FastAPI  
- Python  

### AI & APIs
- Groq LLM (Claim extraction & reasoning)  
- Tavily API (Web search)  

### Data & Storage
- SQLite (Audit logging)  

### Frontend
- Streamlit  

### Tools
- Git & GitHub  
- VS Code  

---

## 📊 Impact

- ⏱️ Reduces verification time by ~95%  
- 💰 Cuts operational costs for newsrooms  
- 📉 Reduces misinformation risk  
- 📈 Improves editorial decision-making  
- 🏛️ Enables auditability and transparency  

---

## 👥 Team — NextGenDevs

### 👤 Anshu Singh  
- Backend development  
- API design and integration  
- Verification pipeline orchestration  
- @AnshuS13
---

### 👤 Aman  
- Frontend development  
- UI/UX design  
- API integration with frontend  

---

### 👤 Aashirwad  
- Research and data sourcing  
- Demo article curation  
- System validation support  

---

## 🚀 Future Scope

- Integration with newsroom CMS  
- Real-time news feed verification  
- Multilingual support  
- Advanced contradiction detection  
- Explainable AI dashboards  

---

## 🧠 Final Thought

> PARIKSHA AI is not just a verification tool —  
> it is a step towards responsible, transparent, and AI-assisted journalism.  
