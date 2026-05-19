import streamlit as st
import json
import re
import os
from groq import Groq

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Persona Evaluator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ---------- global ---------- */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp { background: #0f1117 !important; color: #e2e8f0 !important; }

  /* force ALL text elements light */
  h1, h2, h3, h4, h5, h6, p, span, div, label,
  .stMarkdown, .stMarkdown p, .stMarkdown span,
  [data-testid="stMarkdownContainer"],
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] span,
  .stTextInput label, .stTextArea label, .stSelectbox label,
  .stSelectbox [data-baseweb="select"] span,
  .stSelectbox [data-baseweb="select"] div,
  [data-testid="stWidgetLabel"],
  [data-testid="stWidgetLabel"] p,
  [data-testid="stWidgetLabel"] span {
    color: #e2e8f0 !important;
  }

  /* main content area */
  .main .block-container { color: #e2e8f0 !important; }

  /* selectbox dropdown text */
  [data-baseweb="select"] * { color: #e2e8f0 !important; background: #1e2130 !important; }
  [data-baseweb="menu"] { background: #1e2130 !important; }
  [data-baseweb="option"] { background: #1e2130 !important; color: #e2e8f0 !important; }
  [data-baseweb="option"]:hover { background: #2d3748 !important; }

  /* spinner text */
  .stSpinner > div { color: #e2e8f0 !important; }

  /* alert/error boxes */
  .stAlert { background: #1e2130 !important; color: #e2e8f0 !important; }

  /* ---------- sidebar ---------- */
  [data-testid="stSidebar"] {
    background: #1a1d27 !important;
    border-right: 1px solid #2d3748;
    color: #e2e8f0 !important;
  }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #e2e8f0 !important; }

  /* ---------- inputs ---------- */
  .stTextInput > div > div > input,
  .stSelectbox > div > div,
  .stTextArea > div > div > textarea {
    background: #1e2130 !important;
    border: 1px solid #2d3748 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
  }
  .stTextArea > div > div > textarea:focus,
  .stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.25) !important;
  }

  /* ---------- button ---------- */
  .stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: opacity 0.2s !important;
    width: 100%;
  }
  .stButton > button:hover { opacity: 0.88 !important; }

  /* ---------- score card ---------- */
  .score-card {
    background: #1e2130;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    transition: transform 0.2s;
  }
  .score-card:hover { transform: translateY(-2px); }
  .score-label { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.5rem; }
  .score-value { font-size: 2.6rem; font-weight: 700; line-height: 1; }
  .score-sub   { font-size: 0.78rem; color: #64748b; margin-top: 0.35rem; }

  /* score colours */
  .score-green  { color: #34d399; }
  .score-yellow { color: #fbbf24; }
  .score-red    { color: #f87171; }
  .score-blue   { color: #60a5fa; }
  .score-purple { color: #a78bfa; }

  /* ---------- friction item ---------- */
  .friction-item {
    background: #1e2130;
    border-left: 3px solid #f87171;
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    color: #cbd5e1;
  }
  .friction-item strong { color: #f87171; display: block; margin-bottom: 0.25rem; font-size: 0.75rem; letter-spacing: 0.05em; text-transform: uppercase; }

  /* ---------- strength item ---------- */
  .strength-item {
    background: #1e2130;
    border-left: 3px solid #34d399;
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    color: #cbd5e1;
  }
  .strength-item strong { color: #34d399; display: block; margin-bottom: 0.25rem; font-size: 0.75rem; letter-spacing: 0.05em; text-transform: uppercase; }

  /* ---------- gauge bar ---------- */
  .gauge-wrap { margin-bottom: 1rem; }
  .gauge-label { display: flex; justify-content: space-between; font-size: 0.78rem; color: #94a3b8; margin-bottom: 0.3rem; }
  .gauge-track { background: #2d3748; border-radius: 999px; height: 8px; overflow: hidden; }
  .gauge-fill  { height: 100%; border-radius: 999px; transition: width 0.6s ease; }

  /* ---------- verdict badge ---------- */
  .verdict { display: inline-block; padding: 0.4rem 1.2rem; border-radius: 999px; font-weight: 700; font-size: 0.9rem; margin-top: 0.5rem; }
  .verdict-strong  { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid #34d399; }
  .verdict-good    { background: rgba(96,165,250,0.15); color: #60a5fa; border: 1px solid #60a5fa; }
  .verdict-average { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid #fbbf24; }
  .verdict-weak    { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid #f87171; }

  /* ---------- section header ---------- */
  .section-header {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #6366f1;
    border-bottom: 1px solid #2d3748; padding-bottom: 0.4rem;
    margin-bottom: 1rem;
  }

  /* ---------- divider ---------- */
  hr { border-color: #2d3748 !important; }

  /* ---------- dropdown options ---------- */
  ul[role="listbox"] { background: #1e2130 !important; border: 1px solid #2d3748 !important; }
  ul[role="listbox"] li { color: #e2e8f0 !important; background: #1e2130 !important; }
  ul[role="listbox"] li:hover { background: #2d3748 !important; color: #ffffff !important; }
  li[role="option"] { color: #e2e8f0 !important; background: #1e2130 !important; }
  [data-baseweb="menu"] { background: #1e2130 !important; }
  [data-baseweb="menu"] * { color: #e2e8f0 !important; }
  [data-baseweb="option"] { background: #1e2130 !important; color: #e2e8f0 !important; }
  [data-baseweb="option"]:hover { background: #2d3748 !important; color: #ffffff !important; }
  [data-baseweb="popover"] { background: #1e2130 !important; }
  [data-baseweb="popover"] * { background: #1e2130 !important; color: #e2e8f0 !important; }

  /* ---------- placeholder text ---------- */
  textarea::placeholder { color: #94a3b8 !important; opacity: 1 !important; }
  input::placeholder { color: #94a3b8 !important; opacity: 1 !important; }
  ::-webkit-input-placeholder { color: #94a3b8 !important; opacity: 1 !important; }
  ::-moz-placeholder { color: #94a3b8 !important; opacity: 1 !important; }

  /* ---------- spinner + alerts ---------- */
  .stSpinner > div { color: #e2e8f0 !important; }
  .stAlert { background: #1e2130 !important; color: #e2e8f0 !important; }

  /* hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── persona frameworks ─────────────────────────────────────────────────────────
PERSONAS = {
    "Technical Interviewer": {
        "description": "Evaluates depth, precision, and problem-solving approach",
        "weights": {"Relevance": 0.35, "Clarity": 0.25, "Tone": 0.15, "Structure": 0.15, "Confidence": 0.10},
        "focus": "technical depth, concrete examples, correct terminology",
    },
    "HR / Culture Fit": {
        "description": "Evaluates communication, values alignment, and emotional intelligence",
        "weights": {"Tone": 0.30, "Clarity": 0.25, "Relevance": 0.20, "Structure": 0.15, "Confidence": 0.10},
        "focus": "culture alignment, communication style, interpersonal warmth",
    },
    "Executive / Leadership": {
        "description": "Evaluates strategic thinking, leadership signals, and vision",
        "weights": {"Relevance": 0.30, "Structure": 0.25, "Confidence": 0.25, "Clarity": 0.10, "Tone": 0.10},
        "focus": "vision, strategic framing, decisiveness, leadership narrative",
    },
    "Sales / Client-Facing": {
        "description": "Evaluates persuasion, enthusiasm, and customer empathy",
        "weights": {"Tone": 0.30, "Confidence": 0.25, "Clarity": 0.20, "Relevance": 0.15, "Structure": 0.10},
        "focus": "persuasion, energy, active listening cues, client-centric language",
    },
}

DIMENSION_COLORS = {
    "Relevance":   ("#6366f1", "score-purple"),
    "Clarity":     ("#60a5fa", "score-blue"),
    "Tone":        ("#34d399", "score-green"),
    "Structure":   ("#fbbf24", "score-yellow"),
    "Confidence":  ("#f87171", "score-red"),
}

# ── helpers ────────────────────────────────────────────────────────────────────
def score_color_class(score: float) -> str:
    if score >= 80: return "score-green"
    if score >= 60: return "score-yellow"
    return "score-red"


def verdict(score: float) -> tuple[str, str]:
    if score >= 80: return "Strong Candidate", "verdict-strong"
    if score >= 65: return "Good Candidate",   "verdict-good"
    if score >= 50: return "Average Candidate", "verdict-average"
    return "Weak Candidate", "verdict-weak"


def build_eval_prompt(role: str, transcript: str, persona_name: str, persona: dict) -> str:
    dims = list(persona["weights"].keys())
    dims_list = "\n".join(f"  - {d}" for d in dims)
    return f"""You are an expert AI interview evaluator acting as a **{persona_name}** persona.

Persona focus: {persona["focus"]}

Job Role being evaluated: **{role}**

Candidate Transcript:
\"\"\"
{transcript}
\"\"\"

Evaluate the candidate across these dimensions:
{dims_list}

For each dimension score 0-100. Be rigorous — reserve 85+ for truly exceptional responses.

Return ONLY valid JSON (no markdown, no explanation) exactly matching this schema:
{{
  "scores": {{
    "Relevance": <int 0-100>,
    "Clarity": <int 0-100>,
    "Tone": <int 0-100>,
    "Structure": <int 0-100>,
    "Confidence": <int 0-100>
  }},
  "friction_points": [
    {{"label": "<short tag>", "detail": "<one sentence explanation>"}},
    ...
  ],
  "strengths": [
    {{"label": "<short tag>", "detail": "<one sentence explanation>"}},
    ...
  ],
  "summary": "<2-3 sentence overall assessment>",
  "recommendation": "<one concrete actionable coaching tip>"
}}

friction_points: 2-4 items where candidate underperformed or introduced risk.
strengths: 2-4 items where candidate performed well.
"""


def call_claude(prompt: str) -> dict:
    import os
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY", "")
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.2,
    )
    raw = response.choices[0].message.content.strip()
    # strip possible ```json fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def weighted_score(scores: dict, weights: dict) -> float:
    total = sum(scores[d] * w for d, w in weights.items())
    return round(total, 1)

# ── sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎯 Persona Evaluator")
    st.markdown("<div style='color:#64748b;font-size:0.82rem;margin-bottom:1.2rem;'>AI-powered interview scoring using prompt-engineered evaluation rubrics</div>", unsafe_allow_html=True)

    st.markdown("---")
    persona_name = st.selectbox("Interviewer Persona", list(PERSONAS.keys()))
    persona = PERSONAS[persona_name]
    st.markdown(f"<div style='color:#64748b;font-size:0.8rem;padding:0.6rem;background:#131620;border-radius:8px;'>{persona['description']}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-header'>Dimension Weights</div>", unsafe_allow_html=True)
    for dim, weight in persona["weights"].items():
        color, _ = DIMENSION_COLORS[dim]
        st.markdown(f"""
        <div class='gauge-wrap'>
          <div class='gauge-label'><span>{dim}</span><span>{int(weight*100)}%</span></div>
          <div class='gauge-track'><div class='gauge-fill' style='width:{int(weight*100)}%;background:{color};'></div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='color:#475569;font-size:0.72rem;text-align:center;'>Built for Talview JD · Claude API</div>", unsafe_allow_html=True)

# ── main ───────────────────────────────────────────────────────────────────────
st.markdown("## AI Interview Persona Evaluator")
st.markdown("<div style='color:#64748b;margin-bottom:1.5rem;'>Enter job role + candidate transcript → get LLM-scored evaluation with friction analysis</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='section-header'>Input</div>", unsafe_allow_html=True)
    job_role = st.text_input("Job Role", placeholder="e.g. Senior Backend Engineer, Product Manager")
    transcript = st.text_area(
        "Candidate Transcript",
        height=320,
        placeholder="Paste the candidate's interview response here...\n\nExample:\n'I led the migration of our monolith to microservices at my last company. We started by identifying the highest-traffic bounded contexts — payments and auth — then...'",
    )
    evaluate = st.button("⚡ Evaluate Candidate")

with col2:
    st.markdown("<div class='section-header'>Quick Guide</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#64748b;font-size:0.85rem;line-height:1.8;'>
    1. Pick persona → sets scoring weights<br>
    2. Enter job role + transcript<br>
    3. Hit Evaluate → Claude scores 5 dimensions<br>
    4. Review dashboard, friction points, coaching tip
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Sample Transcript</div>", unsafe_allow_html=True)
    sample = """When our payment service started timing out at peak load, I immediately pulled Datadog metrics and identified a slow DB query — missing index on the transactions table. I coordinated with the DBA, we added a composite index in staging, and deployed during a low-traffic window. Downtime reduced from 8 minutes per hour to zero. Post-mortem doc was shared company-wide."""
    st.markdown(f"<div style='background:#131620;border-radius:8px;padding:0.8rem;font-size:0.78rem;color:#94a3b8;font-style:italic;'>{sample}</div>", unsafe_allow_html=True)

# ── evaluation ─────────────────────────────────────────────────────────────────
if evaluate:
    if not job_role.strip():
        st.error("Enter job role first.")
    elif not transcript.strip():
        st.error("Paste candidate transcript first.")
    else:
        with st.spinner("Gemini evaluating against persona framework…"):
            try:
                prompt = build_eval_prompt(job_role, transcript, persona_name, persona)
                result = call_claude(prompt)
                scores = result["scores"]
                overall = weighted_score(scores, persona["weights"])
                verdict_label, verdict_class = verdict(overall)

                st.markdown("---")
                st.markdown("## Evaluation Dashboard")

                # ── overall score ──────────────────────────────────────────────
                oc1, oc2, oc3 = st.columns([1, 1, 2])
                with oc1:
                    cls = score_color_class(overall)
                    st.markdown(f"""
                    <div class='score-card'>
                      <div class='score-label'>Overall Score</div>
                      <div class='score-value {cls}'>{overall}</div>
                      <div class='score-sub'>/ 100  ·  weighted</div>
                      <div class='verdict {verdict_class}'>{verdict_label}</div>
                    </div>""", unsafe_allow_html=True)
                with oc2:
                    best_dim = max(scores, key=scores.get)
                    worst_dim = min(scores, key=scores.get)
                    _, best_css = DIMENSION_COLORS[best_dim]
                    _, worst_css = DIMENSION_COLORS[worst_dim]
                    st.markdown(f"""
                    <div class='score-card' style='margin-bottom:0.75rem;'>
                      <div class='score-label'>Strongest</div>
                      <div class='score-value {best_css}'>{scores[best_dim]}</div>
                      <div class='score-sub'>{best_dim}</div>
                    </div>
                    <div class='score-card'>
                      <div class='score-label'>Weakest</div>
                      <div class='score-value {worst_css}'>{scores[worst_dim]}</div>
                      <div class='score-sub'>{worst_dim}</div>
                    </div>""", unsafe_allow_html=True)
                with oc3:
                    st.markdown("<div class='section-header'>Assessment</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color:#cbd5e1;font-size:0.9rem;line-height:1.7;'>{result['summary']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-top:0.8rem;padding:0.75rem;background:#1a1d27;border-radius:8px;border-left:3px solid #6366f1;color:#a78bfa;font-size:0.85rem;'><strong style='color:#6366f1;'>Coaching Tip:</strong> {result['recommendation']}</div>", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── dimension scores ───────────────────────────────────────────
                st.markdown("<div class='section-header'>Dimension Breakdown</div>", unsafe_allow_html=True)
                cols = st.columns(5)
                for i, (dim, score) in enumerate(scores.items()):
                    color, css_cls = DIMENSION_COLORS[dim]
                    sc_cls = score_color_class(score)
                    with cols[i]:
                        st.markdown(f"""
                        <div class='score-card'>
                          <div class='score-label'>{dim}</div>
                          <div class='score-value {sc_cls}'>{score}</div>
                          <div class='score-sub'>weight {int(persona["weights"][dim]*100)}%</div>
                        </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── gauge bars ─────────────────────────────────────────────────
                st.markdown("<div class='section-header'>Score Gauges</div>", unsafe_allow_html=True)
                for dim, score in scores.items():
                    color, _ = DIMENSION_COLORS[dim]
                    st.markdown(f"""
                    <div class='gauge-wrap'>
                      <div class='gauge-label'><span>{dim}</span><span>{score}/100</span></div>
                      <div class='gauge-track'><div class='gauge-fill' style='width:{score}%;background:{color};'></div></div>
                    </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── friction + strengths ───────────────────────────────────────
                fc1, fc2 = st.columns(2)
                with fc1:
                    st.markdown("<div class='section-header'>⚠ Friction Points</div>", unsafe_allow_html=True)
                    for fp in result.get("friction_points", []):
                        st.markdown(f"<div class='friction-item'><strong>{fp['label']}</strong>{fp['detail']}</div>", unsafe_allow_html=True)
                with fc2:
                    st.markdown("<div class='section-header'>✓ Strengths</div>", unsafe_allow_html=True)
                    for s in result.get("strengths", []):
                        st.markdown(f"<div class='strength-item'><strong>{s['label']}</strong>{s['detail']}</div>", unsafe_allow_html=True)

            except json.JSONDecodeError as e:
                st.error(f"JSON parse error: {e}. Try again.")
            except Exception as e:
                st.error(f"Evaluation failed: {e}")