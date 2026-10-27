import streamlit as st
import os
from google import genai

st.set_page_config(page_title="AI Grammar Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Grammar & Writing Assistant")
st.write("Paste your draft below to check grammar, spelling, and phrasing.")

# Fetch API key securely from Streamlit Secrets or environment
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please configure GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Input text box
user_text = st.text_area(
    "Your Text:",
    placeholder="e.g., Take a print, ank keep it for furthur references.",
    height=150
)

col1, col2 = st.columns([1, 4])
with col1:
    check_button = st.button("Check Writing", type="primary")

if check_button:
    if not user_text.strip():
        st.warning("Please type or paste some text first.")
    else:
        with st.spinner("Analyzing text with Gemini..."):
            prompt = f"""
            You are a professional copy editor and English tutor.
            Analyze the following text for spelling, grammar, punctuation, and phrasing:

            Text:
            "{user_text}"

            Format your response clearly:
            1. **Corrected Version**: The clean, polished sentence(s).
            2. **Detailed Breakdown**: Bullet points explaining each specific typo, grammatical error, or awkward phrasing, and why it was changed.
            3. **Alternative Phrasings**: 2-3 natural alternatives (formal, casual, or concise).
            """
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.divider()
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error checking text: {e}")
