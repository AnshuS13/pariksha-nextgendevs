import streamlit as st
import requests

st.set_page_config(
    page_title="PARIKSHA",
    page_icon="🔍",
    layout="wide"
)

# ---------- STYLES ----------
st.markdown("""
<style>
.verified-card {
    background-color: #d4edda;
    border-left: 5px solid #28a745;
    padding: 12px 16px;
    border-radius: 4px;
    margin: 8px 0;
}
.unverified-card {
    background-color: #fff3cd;
    border-left: 5px solid #ffc107;
    padding: 12px 16px;
    border-radius: 4px;
    margin: 8px 0;
}
.contradicted-card {
    background-color: #f8d7da;
    border-left: 5px solid #dc3545;
    padding: 12px 16px;
    border-radius: 4px;
    margin: 8px 0;
}
.claim-text {
    font-weight: bold;
    font-size: 14px;
    color: #1a1a1a;
}
.explain-text {
    font-size: 13px;
    color: #444;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🔍 PARIKSHA")
st.subheader("AI-Powered Newsroom Fact Verification System")
st.caption(
    "Paste any news article — PARIKSHA verifies every factual claim in under 60 seconds using 4 AI agents."
)

st.markdown("---")

# ---------- TABS ----------
tab1, tab2 = st.tabs(["🔍 Verify Article", "📋 Verification History"])

# ================= TAB 1 =================
with tab1:
    col1, col2 = st.columns([1, 1])

    # LEFT SIDE
    with col1:
        st.markdown("### 📝 Paste Article Here")

        article_text = st.text_area(
            label="article",
            placeholder="Paste your news article here...",
            height=400,
            label_visibility="collapsed"
        )

        verify_btn = st.button(
            "🔍 Verify This Article",
            type="primary",
            use_container_width=True
        )

    # RIGHT SIDE
    with col2:
        st.markdown("### 📊 Verification Results")

        if verify_btn:
            if not article_text.strip():
                st.warning("⚠️ Please paste an article first.")

            else:
                with st.spinner("🤖 4 AI agents working in parallel..."):
                    try:
                        resp = requests.post(
                            "https://pariksha-nextgendevs.onrender.com/verify,
                            json={"text": article_text},
                            timeout=180
                        )

                        if resp.status_code == 200:
                            data = resp.json()

                            if data["status"] == "success":

                                # SCORE
                                score = data["credibility_score"]
                                label = data.get("credibility_label", "UNKNOWN")

                                if score >= 75:
                                    sc = "#28a745"
                                elif score >= 45:
                                    sc = "#ffc107"
                                else:
                                    sc = "#dc3545"

                                st.markdown(
                                    f"""
                                    <div style='background:{sc}20;
                                    border:2px solid {sc};
                                    border-radius:8px;padding:16px;
                                    text-align:center;margin-bottom:12px'>
                                    <h1 style='color:{sc};margin:0'>{score}%</h1>
                                    <b style='color:{sc}'>{label} CREDIBILITY</b>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                                # STATS
                                s1, s2, s3 = st.columns(3)
                                s1.metric("✅ Verified", data["verified_count"])
                                s2.metric("⚠️ Unverified", data["unverified_count"])
                                s3.metric("❌ Contradicted", data["contradicted_count"])

                                st.markdown("---")

                                # CLAIMS
                                st.markdown(f"**{data['claims_found']} claims analyzed:**")

                                for i, v in enumerate(data["verdicts"]):
                                    verdict = v.get("verdict", "UNVERIFIED")
                                    claim = v.get("claim", "")
                                    explanation = v.get("explanation", "")
                                    sources = v.get("sources", [])

                                    if verdict == "VERIFIED":
                                        css = "verified-card"
                                        ico = "✅ VERIFIED"
                                    elif verdict == "CONTRADICTED":
                                        css = "contradicted-card"
                                        ico = "❌ CONTRADICTED"
                                    else:
                                        css = "unverified-card"
                                        ico = "⚠️ UNVERIFIED"

                                    st.markdown(
                                        f"""
                                        <div class='{css}'>
                                            <div class='claim-text'>{ico} — Claim {i+1}</div>
                                            <div class='explain-text'>{claim}</div>
                                            <div class='explain-text'><i>{explanation}</i></div>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

                                    if sources:
                                        with st.expander(f"📎 Sources ({i+1})"):
                                            for s in sources[:2]:
                                                st.markdown(f"- {s}")

                                # SOURCE REPORT
                                if "source_report" in data:
                                    st.markdown("---")
                                    st.markdown("### 🔎 Source Integrity")

                                    sr = data["source_report"]
                                    quality = sr.get("overall_source_quality", "MODERATE")

                                    if quality == "GOOD":
                                        st.success(f"✅ Source Quality: {quality}")
                                    elif quality == "POOR":
                                        st.error(f"❌ Source Quality: {quality}")
                                    else:
                                        st.warning(f"⚠️ Source Quality: {quality}")

                                    for issue in sr.get("quote_issues", []):
                                        st.markdown(f"- {issue}")

                                    for issue in sr.get("statistic_issues", []):
                                        st.markdown(f"- {issue}")

                                    if sr.get("recommendation"):
                                        st.info(f"💡 {sr['recommendation']}")

                                # BIAS REPORT
                                if "bias_report" in data:
                                    st.markdown("---")
                                    st.markdown("### 🎭 Bias Analysis")

                                    br = data["bias_report"]
                                    score = br.get("bias_score", 0)
                                    btype = br.get("bias_type", "NONE")

                                    st.markdown(f"**Bias Score: {score}/100**")
                                    st.progress(score / 100)

                                    if score < 30:
                                        st.success(f"✅ {btype} — Neutral")
                                    elif score < 60:
                                        st.warning(f"⚠️ {btype} — Moderate Bias")
                                    else:
                                        st.error(f"❌ {btype} — Strong Bias")

                                    if br.get("overall_assessment"):
                                        st.caption(br["overall_assessment"])

                            else:
                                st.error(data.get("message", "Error"))

                        else:
                            st.error(f"Backend error: {resp.status_code}")

                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to backend. Make sure server is running.")

                    except requests.exceptions.Timeout:
                        st.warning("⏳ Request timeout. Try shorter article.")

# ================= TAB 2 =================
with tab2:
    st.markdown("### 📋 Verification History")

    if st.button("🔄 Refresh History"):
        st.rerun()

    try:
        hist = requests.get("http://localhost:8000/history", timeout=10)

        if hist.status_code == 200:
            records = hist.json().get("records", [])

            if not records:
                st.info("No verifications yet.")
            else:
                for r in records:
                    score = r["credibility_score"]
                    label = r["credibility_label"]

                    ico = "🟢" if score >= 75 else "🟡" if score >= 45 else "🔴"

                    with st.expander(
                        f"{ico} {label} ({score}%) — {r['timestamp'][:16]}"
                    ):
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Score", f"{score}%")
                        c2.metric("Claims", r["claims_found"])
                        c3.metric("✅", r["verified_count"])
                        c4.metric("❌", r["contradicted_count"])

                        st.caption(
                            f"Bias: {r['bias_type']} | Source: {r.get('source_quality','N/A')}"
                        )

    except:
        st.error("Backend not connected.")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:gray;font-size:12px'>"
    "Team NextGenDevs | ET Gen AI Hackathon 2026"
    "</div>",
    unsafe_allow_html=True
)