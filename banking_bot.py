import streamlit as st
import pandas as pd
from mistralai.client import MistralClient
import os
import sys

try:
    from mistralai.client import ChatMessage
    HAS_CHAT_MESSAGE = True
except ImportError:
    HAS_CHAT_MESSAGE = False

# Set page config
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and header
st.title("🏦 HBDB Banking Assistant Bot")
st.markdown("*Powered by Mistral AI - Your 24/7 Banking Support*")

# Sidebar for API key and settings
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Enter your Mistral API Key",
        type="password",
        help="Get your API key from Mistral console"
    )
    
    st.markdown("---")
    st.header("📊 About HBDB")
    st.info("""
    HBDB is a modern banking institution offering:
    - Savings & Checking Accounts
    - Credit & Debit Cards
    - Personal & Business Loans
    - Mortgage Services
    - Global Transfers
    - Mobile Banking
    - And much more!
    """)

# Load FAQ data
@st.cache_data
def load_faq_data():
    df = pd.read_csv("hbdb_banking_faqs (2) (1).csv")
    return df

try:
    faq_df = load_faq_data()
    st.sidebar.success(f"✓ Loaded {len(faq_df)} FAQ entries")
except Exception as e:
    st.sidebar.error(f"Error loading FAQ: {e}")
    faq_df = None

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Mistral client
@st.cache_resource
def get_mistral_client(api_key):
    if api_key:
        return MistralClient(api_key=api_key)
    return None

# Create context from FAQ
def create_faq_context():
    if faq_df is None:
        return ""
    context = "HBDB Banking FAQ Database:\n\n"
    for idx, row in faq_df.iterrows():
        question = row.iloc[0] if len(row) > 0 else ""
        answer = row.iloc[1] if len(row) > 1 else ""
        context += f"Q: {question}\nA: {answer}\n\n"
    return context

# Get response from Mistral
def get_mistral_response(user_message, client):
    if not client:
        return "Please enter a valid Mistral API key to use the bot."
    
    faq_context = create_faq_context()
    
    system_prompt = f"""You are a helpful HBDB Banking Assistant. Your role is to provide accurate, 
friendly, and helpful information about HBDB banking services. 

Here is the HBDB FAQ database you should reference:

{faq_context}

When answering customer questions:
1. Search the FAQ database first for relevant information
2. Provide accurate, concise answers
3. Be friendly and professional
4. If you don't know the answer, suggest contacting HBDB customer service
5. Always mention relevant phone numbers or resources when available"""

    try:
        # Get chat history for context
        messages = []
        for msg in st.session_state.messages:
            if HAS_CHAT_MESSAGE:
                messages.append(ChatMessage(role=msg["role"], content=msg["content"]))
            else:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        if HAS_CHAT_MESSAGE:
            messages.append(ChatMessage(role="user", content=user_message))
        else:
            messages.append({"role": "user", "content": user_message})
        
        # Call Mistral API
        response = client.chat(
            model="mistral-large-latest",
            messages=messages
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error getting response: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message"><strong>🤖 HBDB Bot:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
col1, col2 = st.columns([0.9, 0.1])

with col1:
    user_input = st.text_input(
        "Ask me anything about HBDB banking services...",
        placeholder="e.g., How do I open a savings account?",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("Send", key="send_btn")

# Process user input
if send_button and user_input:
    client = get_mistral_client(api_key)
    
    if not api_key:
        st.error("❌ Please enter your Mistral API key in the sidebar to continue.")
    else:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get bot response
        with st.spinner("🤔 Thinking..."):
            bot_response = get_mistral_response(user_input, client)
        
        # Add bot response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_response
        })
        
        # Rerun to display new messages
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    🏦 HBDB Banking Assistant | Powered by Mistral AI | Always here to help
</div>
""", unsafe_allow_html=True)
