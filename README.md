# 🎯 AI Interview Persona Evaluator

> GenAI-powered candidate response evaluator using prompt-engineered LLM scoring rubrics — built to simulate enterprise hiring persona frameworks.

---

## What It Does

- Paste a **job role** + **candidate interview transcript**
- Select an **interviewer persona** (Technical / HR / Executive / Sales)
- LLM evaluates response across **5 dimensions** using custom prompt-engineered rubrics
- Dashboard shows **weighted overall score**, per-dimension breakdown, gauge bars, friction points, strengths, and a coaching tip

---

## Tech Stack

| Layer | Tool |
|-------|------|
| UI | Streamlit |
| LLM | Groq API — `llama-3.3-70b-versatile` |
| Eval | Prompt-engineered JSON rubric (zero fine-tuning) |
| Secrets | Streamlit `st.secrets` |

---

## Scoring Dimensions

| Dimension | What It Measures |
|-----------|-----------------|
| **Relevance** | Answer addresses the question + role context |
| **Clarity** | Logical flow, no rambling, easy to follow |
| **Tone** | Professionalism, warmth, appropriateness |
| **Structure** | STAR-like narrative, conciseness |
| **Confidence** | Assertive language, ownership, no hedging |

---

## Persona Weight System

Each persona re-weights dimensions to match interviewer priorities:

| Persona | Priority |
|---------|----------|
| **Technical Interviewer** | Relevance-heavy (35%) |
| **HR / Culture Fit** | Tone-heavy (30%) |
| **Executive / Leadership** | Confidence + Structure (25% each) |
| **Sales / Client-Facing** | Tone + Confidence (55% combined) |

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-interview-persona-evaluator.git
cd ai-interview-persona-evaluator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
→ console.groq.com — no credit card required

### 4. Create secrets file

**Windows:** Create folder + file at:
```
C:\Users\YOUR_USERNAME\.streamlit\secrets.toml
```

**Mac/Linux:**
```bash
mkdir -p ~/.streamlit
nano ~/.streamlit/secrets.toml
```

**Contents:**
```toml
GROQ_API_KEY = "gsk_your_key_here"
```

### 5. Run
```bash
streamlit run app.py
```

---

## ⚠️ Important — Never Commit Your Key

Make sure `.streamlit/secrets.toml` is in `.gitignore`:
```
.streamlit/secrets.toml
```

GitHub will block pushes if it detects an API key in your commits.

---

## Resume Headline

> Built GenAI candidate response evaluator using prompt engineering + LLM scoring rubrics (Groq/Llama 3.3); simulated enterprise hiring persona framework across 4 interviewer archetypes with weighted multi-dimension scoring dashboard
