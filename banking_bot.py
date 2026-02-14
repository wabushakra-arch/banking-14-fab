import streamlit as st
import pandas as pd
from mistralai.client import MistralClient
import os

st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="��",
    layout="wide"
)

st.markdown("""
    <style>
    .user-message { background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; }
    .bot-message { background-color: #f3e5f5; border-left: 4px solid #9c27b0; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 HBDB Banking Assistant Bot")
st.markdown("*Powered by Mistral AI - v2.0*")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Mistral API Key", type="password")
    st.markdown("---")
    st.info("HBDB Banking Services: Accounts, Cards, Loans, Transfers & More")

@st.cache_data
def load_faq_data():
    try:
        if os.path.exists("hbdb_faqs.csv"):
            return pd.read_csv("hbdb_faqs.csv")
        return pd.DataFrame()
    except:
        return pd.DataFrame()

faq_df = load_faq_data()
if len(faq_df) > 0:
    st.sidebar.success(f"✓ {len(faq_df)} FAQs loaded")

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def get_mistral_client(key):
    return MistralClient(api_key=key) if key else None

def get_response(msg, client):
    if not client:
        return "Please enter your API key in the sidebar."
    
    try:
        msgs = []
        for m in st.session_state.messages[-5:]:
            msgs.append({"role": m["role"], "content": m["content"]})
        
        msgs.append({"role": "user", "content": msg})
        
        resp = client.chat(model="mistral-large-latest", messages=msgs)
        return resp.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)[:100]}"

if st.session_state.messages:
    st.subheader("Chat")
    for m in st.session_state.messages:
        if m["role"] == "user":
            st.markdown(f'<div class="user-message"><b>You:</b> {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message"><b>Bot:</b> {m["content"]}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([0.9, 0.1])
with col1:
    inp = st.text_input("Ask about HBDB services...", label_visibility="collapsed")
with col2:
    btn = st.button("Send")

if btn and inp:
    if not api_key:
        st.error("Enter API key in sidebar")
    else:
        st.session_state.messages.append({"role": "user", "content": inp})
        with st.spinner("Thinking..."):
            resp = get_response(inp, get_mistral_client(api_key))
        st.session_state.messages.append({"role": "assistant", "content": resp})
        st.rerun()

st.markdown("---")
st.caption("🏦 HBDB Banking Assistant | Powered by Mistral AI")
