import streamlit as st
import pandas as pd
from mistralai.client import MistralClient
import os

st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="��",
    layout="wide"
)

st.title("🏦 HBDB Banking Assistant Bot")
st.markdown("*Powered by Mistral AI Large - v3.0*")

# Sidebar for API key and settings
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter your Mistral API Key", type="password")
    
    st.markdown("---")
    st.header("📊 About HBDB")
    st.info("""
    HBDB Banking Services:
    - Savings & Checking Accounts
    - Credit & Debit Cards
    - Personal & Business Loans
    - Mortgage Services
    - Global Transfers
    - Mobile Banking
    """)

# Load FAQ data
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
    st.sidebar.success(f"✓ Loaded {len(faq_df)} FAQ entries")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get Mistral client
@st.cache_resource
def get_mistral_client(key):
    return MistralClient(api_key=key) if key else None

# Get response from Mistral
def get_mistral_response(user_message, client):
    if not client:
        return "Please enter a valid Mistral API key to use the bot."
    
    try:
        # Build message list
        messages = []
        for msg in st.session_state.messages:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Mistral
        response = client.chat(
            model="mistral-large-latest",
            messages=messages
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about HBDB banking services..."):
    if not api_key:
        st.error("❌ Please enter your Mistral API key in the sidebar")
    else:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                client = get_mistral_client(api_key)
                response = get_mistral_response(prompt, client)
            st.markdown(response)
        
        # Add bot response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

# Footer
st.markdown("---")
st.caption("🏦 HBDB Banking Assistant | Powered by Mistral AI Large")
