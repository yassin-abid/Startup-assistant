# app.py
import streamlit as st
from agents.manager_agent import handle_query

# -------------------------------
# 🚀 Streamlit App Setup
# -------------------------------
st.set_page_config(page_title="Startup AI Hub", page_icon="🚀", layout="wide")

# -------------------------------
# 💾 Initialize session memory
# -------------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "ideation_history" not in st.session_state:
    st.session_state.ideation_history = []
if "business_history" not in st.session_state:
    st.session_state.business_history = []
if "selected_idea" not in st.session_state:
    st.session_state.selected_idea = None
if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = None  # prevent duplicate calls

# -------------------------------
# 🧠 App Header
# -------------------------------
st.title("🚀 Startup AI Hub")
st.markdown(
    """
Your **multi-agent startup assistant** — powered by Gemini 💡  
Supports:  
- 🧩 **Axe 1:** Startup Ideation  
- 💼 **Axe 5:** Business Modeling  
- ⚖️ **Axe 6:** Legal & Regulatory Compliance  
"""
)

# -------------------------------
# 💬 Chat Input
# -------------------------------
user_input = st.chat_input("Ask anything about your startup idea, business model, or legal topic...")

# Process only *new* user messages (prevents double-run)
if user_input and user_input != st.session_state.last_user_input:
    st.session_state.last_user_input = user_input  # store to avoid re-run duplication
    with st.spinner("🤔 Thinking..."):
        handle_query(user_input, st.session_state)

# -------------------------------
# 📜 Message Display Helper
# -------------------------------
def get_role_and_content(msg):
    """Unify message structure between dicts and LangChain objects."""
    if hasattr(msg, "type") and hasattr(msg, "content"):
        role = "user" if msg.type == "human" else "assistant"
        content = msg.content
    elif isinstance(msg, dict):
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
    else:
        role, content = "assistant", str(msg)
    return role, content

# -------------------------------
# 🗨️ Chat Display (No Duplication)
# -------------------------------
st.divider()
st.subheader("💬 Conversation")

# Render messages only once in order
for msg in st.session_state.conversation:
    role, content = get_role_and_content(msg)
    if role == "user":
        st.chat_message("user").write(f"🧍‍♂️ **You:** {content}")
    elif role == "assistant":
        st.chat_message("assistant").write(content)
