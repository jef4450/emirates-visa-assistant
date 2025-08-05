import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Page config
st.set_page_config(page_title="Emirates Visa Assistant", layout="wide")

# ----------------- 🌟 Emirates Black & Gold Theme -------------------
st.markdown("""
    <style>
    body {
        background-color: #0b0c10;
        color: #f2c94c;
    }
    .stApp {
        background-color: #0b0c10;
        color: #f2c94c;
    }
    .stButton>button {
        background-color: #f2c94c;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        border: none;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1d;
        color: #f2c94c;
    }
    .stMarkdown {
        font-size: 16px;
        color: #f2c94c;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- 🚀 App Layout -------------------
st.title("🇦🇪 Emirates Visa Assistant")
language = st.selectbox("🌐 Select Language", ["English", "Arabic"])

st.markdown("Ask anything about **UAE visas**, documents, golden visas, or residency rules.")

# ----------------- 📌 FAQs -------------------
with st.expander("📚 UAE Visa FAQs (Click to expand)"):
    st.markdown("""
    **1. What types of visas are available for UAE?**  
    - Tourist Visa  
    - Employment Visa  
    - Golden Visa  
    - Student Visa  
    - Business/Investor Visa  

    **2. What documents are needed for UAE Employment Visa?**  
    - Valid passport  
    - Passport-size photo  
    - Job offer letter  
    - Medical test results  
    - Emirates ID application  

    **3. How long does visa processing take?**  
    Usually 2–7 working days depending on the type.

    **4. What is the UAE Golden Visa?**  
    A long-term 5 or 10-year visa for investors, skilled professionals, and researchers.
    """)

# ----------------- 💬 Chat Section -------------------
question = st.text_input("💬 Your Question")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if question:
    with st.spinner("Thinking..."):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Referer": "https://yourdomain.com",  # Replace with actual domain or localhost
            "X-Title": "Emirates Visa Assistant"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": 
    "You are a helpful assistant for UAE visa and residency-related questions. "
    + ("Answer clearly and concisely in Arabic." if language == "Arabic" else "Answer clearly and concisely in English.")
},

                {"role": "user", "content": question}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            st.success("✅ Here's the answer:")
            st.markdown(f"**🤖 Assistant:** {answer}")

            # Save to session state
            st.session_state.chat_history.append(("🧑 You", question))
            st.session_state.chat_history.append(("🤖 Assistant", answer))
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")

# ----------------- 📜 Chat History -------------------
if st.session_state.chat_history:
    st.divider()
    with st.expander("📖 Chat History"):
        for role, msg in st.session_state.chat_history:
            st.markdown(f"**{role}:** {msg}")

# ----------------- 🧹 Clear Button -------------------
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.success("Chat history cleared.")

# ----------------- ✨ Footer -------------------
st.markdown("""
<hr style="border:1px solid #f2c94c">
<div style='text-align: center; color: #f2c94c'>
    Built with ❤️ for the Emirates by <b>Jefcodes</b><br>
    Powered by OpenRouter ·
</div>
""", unsafe_allow_html=True)
