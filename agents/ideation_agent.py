# agents/ideation_agent.py

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import re

print("all good")

import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

system_message = SystemMessage(content="""
You are 'StartAI' — an AI assistant specialized in helping entrepreneurs with startup ideation (Axe 1).
Your domain is startup creation, business ideas, problem validation, and innovation strategies.

🎯 Mission:
Help users generate **modern, innovative, and market-relevant** startup ideas based on current global trends and emerging technologies.
Always stay up to date — your suggestions should feel relevant **today**, not five years ago.

🧩 Rules:
- Only answer questions related to startups, entrepreneurship, ideation, innovation, or business concepts.
- If a user asks something outside these topics, politely refuse and say:
  "I specialize only in startup ideation and entrepreneurship. Please ask me about startup ideas or innovation instead."
- Keep your answers **practical**, **creative**, and **concise**.
- Prefer ideas that align with **current tech, social, and economic trends** (e.g., AI tools, sustainability, remote work, creator economy, mental health, fintech, circular economy, etc.)
- Avoid any **immoral, unethical, or illegal** topics — including but not limited to:
  adult content, gambling, violence, weapons, political manipulation, scams, or discrimination.
- When possible, output ideas in a structured format:
  **Idea name**, **Problem**, **Solution**, **Target users**, **Feasibility score**, and optionally **Trend relevance** (e.g., "AI + sustainability").
""")

def extract_ideas(text):
    """Extract a list of ideas from AI's text response (numbered format)."""
    ideas = re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|$)', text, re.DOTALL)
    return [idea.strip() for idea in ideas]

def detect_chosen_idea(user_input, ideas):
    """Detect if user selected one of the ideas (by number or name)."""
    if not ideas:
        return None

    # Match “idea 2” or “number 2”
    match = re.search(r"\b(?:idea|number|option)?\s*(\d+)\b", user_input.lower())
    if match:
        idx = int(match.group(1)) - 1
        if 0 <= idx < len(ideas):
            return ideas[idx]

    # Try matching by partial name
    for idea in ideas:
        name = idea.split("–")[0].split(":")[0].strip().lower()
        if name in user_input.lower():
            return idea

    return None

def run_ideation_agent(user_input, chat_history=[], session_state=None):
    """
    Takes user input, generates or updates startup ideas, and optionally stores chosen idea.
    """
    # Convert chat_history to LangChain message objects
    lc_history = []
    for msg in chat_history:
        role = ""
        content = ""
        if hasattr(msg, "type") and hasattr(msg, "content"):
            role = "user" if msg.type == "human" else "assistant"
            content = msg.content
        elif isinstance(msg, dict):
            role = msg.get("role", "assistant")
            content = msg.get("content", "")
        else:
            role = "assistant" 
            content = str(msg)
        
        if role == "user":
            lc_history.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_history.append(AIMessage(content=content))

    lc_history.append(HumanMessage(content=user_input))
    response = llm(lc_history)
    ai_reply = response.content
    
    # NOTE: We do NOT append to chat_history here anymore.
    # The Manager Agent handles memory updates to avoid duplication.

    # Extract ideas from AI’s answer (store in session for reference)
    ideas = extract_ideas(ai_reply)
    if session_state is not None and ideas:
        session_state.generated_ideas = ideas

    # Detect user choosing an idea
    if session_state is not None and hasattr(session_state, "generated_ideas"):
        chosen = detect_chosen_idea(user_input, session_state.generated_ideas)
        if chosen:
            session_state.selected_idea = chosen

    return ai_reply, chat_history
