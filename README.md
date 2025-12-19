# **Startup AI Hub**
*Your Intelligent Multi-Agent Co-Founder Powered by Gemini*

![last-commit](https://img.shields.io/github/last-commit/yassin-abid/Startup-assistant?style=flat&logo=git&logoColor=white&color=0080ff)
![repo-top-language](https://img.shields.io/github/languages/top/yassin-abid/Startup-assistant?style=flat&color=0080ff)
![repo-language-count](https://img.shields.io/github/languages/count/yassin-abid/Startup-assistant?style=flat&color=0080ff)

### **Built with:**
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C.svg?style=flat&logo=LangChain&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2.svg?style=flat&logo=Google%20Gemini&logoColor=white)

---

## **📑 Table of Contents**
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Features](#features)

---

## **📘 Overview**

**Startup AI Hub** is a comprehensive, multi-agent platform designed to guide entrepreneurs from the spark of an idea to a solid business strategy.
It orchestrates specialized AI agents to handle ideation, business modeling, and legal compliance, delivering a seamless co-founder experience.

### **Why Startup AI Hub?**

This project democratizes access to high-quality startup consulting, allowing anyone to build, validate, and plan their business with the speed and intelligence of Google's Gemini models.

### ✅ **Core Features**
- 🧩 **Multi-Agent Architecture**
  Orchestrates specialized agents (Ideation, Business, Legal) via a central intelligent router.

- 💡 **Smart Ideation (Axe 1)**
  Generates innovative, market-relevant startup ideas with feasibility scores and trend analysis.

- 💼 **Instant Business Modeling (Axe 5)**
  Automatically creates full Business Model Canvases, identifying revenue streams, pricing strategies, and break-even points in seconds.

- ⚖️ **Legal & Compliance (Axe 6)**
  Provides instant guidance on IP, NDAs, and regulatory risks like GDPR.

- 🛡️ **Safety & Guardrails**
  Built-in filters for unsafe content and empathetic responses for mental health support.

- 🧠 **Context Awareness**
  Remembers your selected idea and conversation history for a natural, flowing dialogue.

---

## **🚀 Getting Started**

### **Prerequisites**
Make sure you have the following installed:

- **Programming Language:** Python 3.9+
- **Package Manager:** pip

---

## **📦 Installation**

Clone the repository:

```sh
git clone https://github.com/yassin-abid/Startup-assistant.git
```

Navigate into the project:

```sh
cd Startup-assistant
```

Create a virtual environment (optional but recommended):

```sh
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Set up your environment variables:
Create a `.env` file in the root directory and add your Google API key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## **▶️ Usage**

Start the Streamlit application:

```sh
streamlit run app.py
```

---

## **🧪 Testing**

To verify the installation, ensure the app launches in your browser at `http://localhost:8501`.
You can test the agents by asking:
- "Give me a startup idea in agriculture."
- "Generate a business model for this."
- "What are the legal risks?"
