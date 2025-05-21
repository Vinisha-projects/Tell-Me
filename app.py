import streamlit as st
import requests
import os
import random

# Load Groq API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Popular tools for 'Surprise Me'
popular_tools = [
    "Netflix", "Spotify", "Gmail", "Google Maps",
    "YouTube", "TikTok", "Amazon", "Grammarly"
]

# Generate LLM explanation prompt
def generate_prompt(tool):
    return f"""
You are an AI assistant that explains how artificial intelligence is used in real-world products and platforms to someone who is non-technical person

The user is asking about: "{tool}"

 Write in a friendly, easy-to-understand tone  
 Avoid saying "Let me tell you about..." or "AI and..."  
 Assume the input is a company, product, app, or tool that uses AI  
 Start by explaining what it is and what it does  
 Describe how AI is used in it (recommendations, automation, language, vision, etc.)  
 Explain how a normal person might use it (basic example)  
 Include a short, friendly safety reminder not to share personal or confidential information  
 Keep it very clear, short sentences, no technical terms, and use 1–2 emojis to make it friendly  
 Do not make anything up — only respond with known facts

Do not add an introduction. Just start directly with the explanation.

"""

# Generate explanation using Groq LLaMA 3
def get_explanation(tool):
    prompt = generate_prompt(tool)
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You explain AI in a soft, helpful, and simple way anyone can understand."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            }
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f" Error: {e}"

# LLM-powered tool validation
def is_ai_tool(tool_name):
    try:
        prompt = f"Is '{tool_name}' a real-world product or app that uses AI in some way? Just answer yes or no."

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 3
            }
        )
        reply = response.json()["choices"][0]["message"]["content"].strip().lower()
        return "yes" in reply
    except Exception:
        return False  # Fail-safe: assume invalid
        

# --------------------- Streamlit UI ---------------------

st.set_page_config(page_title="Tell Me AI", layout="centered")

# Minimalist Apple-style theme
st.markdown("""
<style>
body, .stApp {
    background-color: #f9f9f9;
    color: #1a1a1a;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
h1 {
    font-size: 2.5rem;
    font-weight: 500;
    margin-bottom: 0.25rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("### Tell Me AI")
st.caption("Understand how AI works in your favorite tools — simply, clearly, and beautifully.")

# Text input
user_input = st.text_input("Type a tool or app name:", placeholder="e.g., Netflix, Uber, ChatGPT")

# Buttons
col1, col2 = st.columns(2)

# Explain button
with col1:
    if st.button("Tell me"):
        cleaned_input = user_input.strip()
        if not cleaned_input:
            st.warning("Please type a tool or app name.")
        else:
            with st.spinner("Checking if it's a real AI-powered tool..."):
                if is_ai_tool(cleaned_input):
                    with st.spinner("Explaining clearly..."):
                        explanation = get_explanation(cleaned_input)
                    st.markdown("---")
                    st.markdown(f"#### How AI helps in {cleaned_input}")
                    st.markdown(explanation)
                else:
                    st.error("Hmm... that doesn't seem like a real AI-powered product or app. Try something like Netflix, Grammarly, or Spotify.")

#  Surprise Me button
with col2:
    if st.button("Surprise Me"):
        random_tool = random.choice(popular_tools)
        with st.spinner(f"Picking something fun: {random_tool}..."):
            explanation = get_explanation(random_tool)
        st.markdown("---")
        st.markdown(f"#### How AI helps in {random_tool}")
        st.markdown(explanation)
