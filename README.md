# 🚀 Startup AI Hub

**Startup AI Hub** is a multi-agent AI assistant that helps entrepreneurs build startups — from ideation to business modeling and legal compliance.  
Built with **Streamlit** and powered by **Google Gemini (2.5 Pro & Flash)** models.

---

## 🧩 Features

- 🧠 **Ideation Agent (StartAI)** – Generates innovative startup ideas aligned with current global trends.  
- 💼 **Business Agent (BizAI)** – Creates complete business models (Canvas, pricing, cost structure, investor summary).  
- ⚖️ **Legal Agent (LexAI)** – Provides guidance on contracts, IP, GDPR, and compliance checklists.  
- 🗨️ **Conversational Memory** – Remembers previous interactions to provide contextual answers.  
- 🧭 **Intent Detection** – Uses Gemini Flash to determine when to generate or refine business models.  
- 🌐 **Streamlit UI** – Real-time chat interface for a smooth, interactive experience.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Backend** | Python |
| **LLMs** | Google Gemini 2.5 Pro / Flash |
| **Frameworks** | LangChain, Google Generative AI SDK |
| **Storage** | JSON (temporary session persistence) |

---

## 🏗️ Project Architecture

Startup-assistant/
│
├── app.py # Streamlit UI entry point
└── agents/
├── ideation_agent.py # Startup ideation (Axe 1)
├── business_agent.py # Business model generation (Axe 5)
├── legal_agent.py # Legal and compliance (Axe 6)
└── manager_agent.py # Central controller managing agent communication
