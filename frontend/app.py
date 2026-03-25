import streamlit as st
import requests

st.set_page_config(page_title="PARIKSHA", layout="wide")

st.title("🔍 PARIKSHA")
st.subheader("AI-Powered Newsroom Fact Verification")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Paste Article")
    article_text = st.text_area("", height=300)

    verify_button = st.button("🔍 Verify")

with col2:
    st.markdown("### 📊 Results")

    if verify_button:
        if not article_text.strip():
            st.warning("Please paste an article")
        else:
            try:
                response = requests.post(
                    "http://localhost:8000/verify",
                    json={"text": article_text}
                )

                if response.status_code == 200:
                    st.success("Verification done")
                    st.json(response.json())
                else:
                    st.error("Backend error")

            except:
                st.error("Backend not running")