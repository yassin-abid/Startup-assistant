# agents/business_model.py

import google.generativeai as genai
import json

import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------------
# ⚙️ CONFIGURE GEMINI
# --------------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
classifier_model = genai.GenerativeModel("gemini-2.5-flash")  # fast, for classification


# --------------------------------
# 💼 SYSTEM INSTRUCTION
# --------------------------------
BUSINESS_SYSTEM_PROMPT = """
You are 'BizAI' — a startup business consultant specialized in entrepreneurship, business modeling, and financial strategy.

You help with:
- Business model canvas and structure
- Market and pricing strategies
- Cost and revenue analysis
- Investment and scaling advice

Rules:
- Only answer questions related to startups, entrepreneurship, business models, finance, or strategy.
- If a user asks something unrelated (e.g., math, general trivia, personal questions), politely say:
  "I specialize only in startup business modeling and strategy. Please ask me about business or finance topics."
- Keep answers concise, practical, and clearly structured.
"""


# --------------------------------
# 🧠 SMART INTENT DETECTION
# --------------------------------
def should_generate_business_model(user_input: str) -> bool:
    """Ask the small model if the user is requesting a business model."""
    classification_prompt = f"""
You are an intent classifier for a startup assistant.

User said: "{user_input}"

Determine if the user wants to GENERATE or UPDATE a BUSINESS MODEL for a known startup idea.

Answer only 'yes' or 'no' — no explanations.
"""
    response = classifier_model.generate_content(classification_prompt)
    return "yes" in response.text.strip().lower()


# --------------------------------
# 🏗️ BUSINESS MODEL GENERATION
# --------------------------------
def generate_business_model(selected_idea, chat_history):
    """Generate a structured business model for a startup idea."""
    prompt = f"""{BUSINESS_SYSTEM_PROMPT}

Analyze the startup idea: "{selected_idea}" (do not rename or rebrand it).

Create a structured and concise business model including:
1. **Business Model Canvas (9 Blocks)** – each block in 1–2 bullet points.
2. **Revenue Streams** – 2–3 main income sources.
3. **Cost Structure** – list main fixed & variable costs.
4. **Pricing Strategy** – suggest simple, clear pricing tiers or key price points.
5. **Break-even Estimate** – provide round-number assumptions.
6. **Investor Summary** – short paragraph on opportunities & risks.
7. **Alternative Scenarios** – short paragraph for 1–2 alternative business strategies.
"""
    response = model.generate_content(prompt)
    business_model = response.text.strip()

    chat_history.append({"role": "system", "content": "Business model generated."})

    # Save output for record
    with open("business_model.json", "w", encoding="utf-8") as f:
        json.dump(
            {"idea": selected_idea, "business_model": business_model},
            f,
            indent=4,
            ensure_ascii=False,
        )

    return business_model


# --------------------------------
# 💬 CONVERSATION HANDLER
# --------------------------------
def get_role_and_content(msg):
    """Normalize message structure between dict and LangChain types."""
    if hasattr(msg, "type") and hasattr(msg, "content"):
        role = "user" if msg.type == "human" else "assistant"
        content = msg.content
    elif isinstance(msg, dict):
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
    else:
        role, content = "assistant", str(msg)
    return role, content


def chat_with_agent(user_input, chat_history):
    """Engage in normal conversation about business strategy."""
    context = "\n".join(
        [f"{get_role_and_content(msg)[0].capitalize()}: {get_role_and_content(msg)[1]}" for msg in chat_history[-6:]]
    )

    prompt = f"""{BUSINESS_SYSTEM_PROMPT}

Conversation context:
{context}

User just asked: "{user_input}"

If the question is unrelated to business, politely decline.
Otherwise, respond as a professional consultant would.
"""
    response = model.generate_content(prompt)
    reply = response.text.strip()

    reply = response.text.strip()

    # NOTE: We do NOT append to chat_history here. 
    # Manager Agent handles it.

    return reply


# --------------------------------
# 🚀 MAIN ENTRY POINT
# --------------------------------
def run_business_agent(user_input, chat_history=[], selected_idea=None):
    """Main interface used by the manager agent."""
    if selected_idea and should_generate_business_model(user_input):
        business_model = generate_business_model(selected_idea, chat_history)
        reply = f"Here's the business model for **{selected_idea}**:\n\n{business_model}"
    else:
        reply = chat_with_agent(user_input, chat_history)

    return reply, chat_history
