# agents/manager_agent.py

import google.generativeai as genai
from agents.ideation_agent import run_ideation_agent
from agents.business_agent import run_business_agent
from agents.legal_agent import run_legal_agent

import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# 🔧 CONFIGURATION
# -------------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
router_model = genai.GenerativeModel("gemini-2.5-flash-lite")

# -------------------------------
# 🧠 LLM-BASED ROUTER
# -------------------------------
def decide_agent(user_input, conversation_context):
    """
    Uses an LLM to decide which agent should handle the user query.
    Prioritizes unsafe and emotional detection before business logic.
    """
    router_prompt = f"""
You are the Manager Agent overseeing a team of AI specialists that help entrepreneurs.

Agents available:
- Ideation Agent → for startup ideas, innovation, problem validation, creativity (Axe 1)
- Business Agent → for business models, pricing, investors, cost structure, and strategy (Axe 5)
- Legal Agent → for legal & regulatory compliance, NDAs, contracts, IP protection, and risk management (Axe 6)

Conversation context:
{conversation_context}

User message:
"{user_input}"

Your task:
1️⃣ If the message contains pornographic, sexual, violent, discriminatory, or illegal content,
    classify it as **Unsafe** — do NOT route it to any agent.

2️⃣ If the user expresses sadness, depression, stress, anxiety, burnout, or emotional distress in any form,
    classify it as **Support** and respond with empathy:
    "I'm really sorry you're feeling this way. You’re not alone — it might really help to talk to a qualified mental-health professional or someone you trust.
    If you ever feel unsafe or overwhelmed, please reach out to your local emergency helpline or a mental-health service right now."

3️⃣ Otherwise:
    - "Ideation" → if related to startups, idea generation, creativity, or innovation.
    - "Business" → if related to business models, pricing, investors, or funding.
    - "Legal" → if related to contracts, compliance, regulations, or intellectual property.

4️⃣ If the question is unrelated to these (e.g., math, jokes, random chat),
    return "None" and suggest focusing on one of the supported axes (Axe 1, 5, 6).

Return one of:
"Ideation", "Business", "Legal", "Support", "Unsafe", or "None".
"""
    response = router_model.generate_content(router_prompt)
    decision = response.text.strip().lower()

    # Normalize model output
    if "unsafe" in decision:
        return "unsafe"
    elif "support" in decision:
        return "support"
    elif "ideation" in decision:
        return "ideation"
    elif "business" in decision:
        return "business"
    elif "legal" in decision:
        return "legal"
    else:
        return "none"

# -------------------------------
# 🧩 MANAGER HANDLER
# -------------------------------
def get_role_and_content(msg):
    """Normalize message format between LangChain and dict types."""
    if hasattr(msg, "type") and hasattr(msg, "content"):
        role = "user" if msg.type == "human" else "assistant"
        content = msg.content
    elif isinstance(msg, dict):
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
    else:
        role, content = "assistant", str(msg)
    return role, content


def handle_query(user_input, session_state):
    """
    Routes queries to the correct agent (Ideation, Business, or Legal),
    shares memory (selected idea, etc.), and declines out-of-scope topics.
    """
    context = "\n".join(
        f"{get_role_and_content(msg)[0]}: {get_role_and_content(msg)[1]}"
        for msg in session_state.conversation[-10:]
    )

    chosen_agent = decide_agent(user_input, context)
    reply = "🤖 I’m not sure which agent fits this question yet."

    # -------------------------------
    # 🔒 UNSAFE CONTENT
    # -------------------------------
    if chosen_agent == "unsafe":
        reply = (
            "⚠️ I'm sorry, but I can’t assist with topics that involve explicit, violent, or inappropriate content. "
            "Please ask about something constructive — like startup ideation (Axe 1), business modeling (Axe 5), "
            "or legal compliance (Axe 6)."
        )

    # -------------------------------
    # ❤️ SUPPORT (mental health)
    # -------------------------------
    elif chosen_agent == "support":
        reply = (
            "❤️ I'm really sorry you're feeling this way. You're not alone — it might really help to talk to a "
            "qualified mental-health professional or someone you trust. If you ever feel unsafe or overwhelmed, "
            "please reach out to your local emergency helpline or a trusted counselor. You deserve care and support."
        )

    # -------------------------------
    # 💡 IDEATION AGENT (Axe 1)
    # -------------------------------
    elif chosen_agent == "ideation":
        reply, _ = run_ideation_agent(
            user_input,
            chat_history=session_state.conversation,
            session_state=session_state
        )

    # -------------------------------
    # 💼 BUSINESS AGENT (Axe 5)
    # -------------------------------
    elif chosen_agent == "business":
        selected_idea = getattr(session_state, "selected_idea", None)
        reply, _ = run_business_agent(
            user_input,
            chat_history=session_state.conversation,
            selected_idea=selected_idea
        )

    # -------------------------------
    # ⚖️ LEGAL AGENT (Axe 6)
    # -------------------------------
    elif chosen_agent == "legal":
        reply, _ = run_legal_agent(
            user_input,
            chat_history=session_state.conversation
        )

    # -------------------------------
    # 🚫 OUTSIDE ALL AXES
    # -------------------------------
    elif chosen_agent == "none":
        reply = (
            "🚫 I’m sorry, but this question seems outside our focus areas. "
            "I can only assist with **startup ideation (Axe 1)**, "
            "**business modeling (Axe 5)**, or **legal & regulatory compliance (Axe 6)**. "
            "Please ask something related to one of these."
        )

    # -------------------------------
    # 🧠 MEMORY UPDATE
    # -------------------------------
    session_state.conversation.append({"role": "user", "content": user_input})
    session_state.conversation.append(
        {"role": "assistant", "content": f"({chosen_agent.capitalize()} Agent) {reply}"}
        if chosen_agent != "none"
        else {"role": "assistant", "content": reply}
    )

    return reply, chosen_agent
