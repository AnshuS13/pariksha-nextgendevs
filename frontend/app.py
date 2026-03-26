import streamlit as st
import requests

st.set_page_config(page_title="PARIKSHA", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>

body {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
}

/* Header */
.title {
    text-align: center;
    font-size: 64px;
    font-weight: 900;
    letter-spacing: 2px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 40px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

/* Score Box */
.score-box {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

/* Claim box */
.claim-box {
    background: rgba(255,255,255,0.04);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 60px;
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title">🔍 PARIKSHA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Newsroom Fact Verification System</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1, 1])

# ---------- INPUT ----------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📝 Paste Article")
    article_text = st.text_area("Enter article...", height=300)

    verify_button = st.button("🚀 Analyze Now")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RESULTS ----------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📊 Results")

    if verify_button:
        if not article_text.strip():
            st.warning("⚠️ Please paste an article")

        else:
            with st.spinner("🔎 AI analyzing..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/verify",
                        json={"text": article_text},
                        timeout=60
                    )

                    if response.status_code == 200:
                        data = response.json()

                        st.success("✅ Verification Complete")

                        # ---------- SCORE ----------
                        score = data.get("credibility_score", 0)
                        label = data.get("credibility_label", "UNKNOWN")

                        if score >= 75:
                            color = "#14532d"
                            emoji = "🟢"
                        elif score >= 45:
                            color = "#854d0e"
                            emoji = "🟡"
                        else:
                            color = "#7f1d1d"
                            emoji = "🔴"

                        st.markdown(
                            f'<div class="score-box" style="background:{color};">{emoji} {score}% - {label}</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown("---")

                        # ---------- CLAIMS ----------
                        st.markdown("### 🔎 Claims & Verdicts")

                        for v in data.get("verdicts", []):
                            st.markdown('<div class="claim-box">', unsafe_allow_html=True)

                            st.markdown(f"**👉 {v.get('claim','N/A')}**")

                            verdict = v.get("verdict", "UNKNOWN")

                            if verdict == "VERIFIED":
                                st.success("✅ VERIFIED")
                            elif verdict == "CONTRADICTED":
                                st.error("❌ CONTRADICTED")
                            else:
                                st.warning("⚠️ UNVERIFIED")

                            st.write(v.get("reason", "No explanation available"))

                            # Sources
                            sources = v.get("sources", [])
                            if sources:
                                st.markdown("📎 **Sources:**")
                                for s in sources:
                                    st.markdown(f"- {s}")

                            st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown("---")

                        # ---------- SOURCE ANALYSIS ----------
                        st.markdown("### 📚 Source Analysis")
                        st.info(data.get("source_report", {}).get("overall_source_quality", "N/A"))
                        st.write(data.get("source_report", {}).get("recommendation", ""))

                        # ---------- BIAS ----------
                        st.markdown("### ⚖️ Bias Analysis")
                        st.write(data.get("bias_report", {}).get("overall_assessment", ""))

                        # ---------- RAW ----------
                        with st.expander("📂 Full Technical Report"):
                            st.json(data)

                    else:
                        st.error(f"❌ Backend Error: {response.status_code}")

                except Exception as e:
                    st.error(f"❌ Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
🚀 Built by NextGenDevs | PARIKSHA AI Fact Checker  
</div>
""", unsafe_allow_html=True)