import google.generativeai as genai

import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

LEGAL_SYSTEM_PROMPT = """
You are 'LexAI' — a legal and regulatory compliance assistant for startups (Axe 6).

You help with:
- Intellectual property (IP) and data privacy
- Drafting NDAs, partnership agreements, and contracts
- Regulatory compliance (e.g., GDPR)
- Risk identification and legal checklists for startups

Rules:
- Only answer questions related to legal, regulatory, or compliance topics for startups.
- If unrelated, respond:
  "I specialize only in legal and regulatory compliance for startups. Please ask about contracts, IP, privacy, or compliance."
- Do not provide legally binding advice or replace a lawyer.
- Avoid unethical or illegal topics.
- Format answers as:
  1. **Summary of Legal Area**
  2. **Main Risks**
  3. **Checklist / Recommended Steps**
  4. **Disclaimer**
"""

def get_role_and_content(msg):
    if hasattr(msg, "type") and hasattr(msg, "content"):
        role = "user" if msg.type == "human" else "assistant"
        content = msg.content
    elif isinstance(msg, dict):
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
    else:
        role, content = "assistant", str(msg)
    return role, content

def chat_with_legal_agent(user_input, chat_history):
    context = "\n".join(
        [f"{get_role_and_content(msg)[0]}: {get_role_and_content(msg)[1]}" for msg in chat_history[-6:]]
    )
    prompt = f"""{LEGAL_SYSTEM_PROMPT}

Conversation context:
{context}

User just asked: "{user_input}"

If unrelated to legal/compliance, politely decline.
Otherwise, respond as a professional legal assistant.
"""
    reply = model.generate_content(prompt).text.strip()
    # NOTE: We do NOT append to chat_history here. 
    # Manager Agent handles it.
    return reply

def run_legal_agent(user_input, chat_history=[]):
    reply = chat_with_legal_agent(user_input, chat_history)
    return reply, chat_history
