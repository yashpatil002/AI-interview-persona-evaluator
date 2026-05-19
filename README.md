# 🎯 AI Interview Persona Evaluator

> Built for Talview JD — AI interviewer persona framework + LLM scoring rubrics

## What it does

- Input job role + candidate transcript
- Select interviewer persona (Technical / HR / Executive / Sales)
- Claude evaluates across 5 dimensions using prompt-engineered rubrics
- Dashboard: weighted overall score, per-dimension gauges, friction points, strengths, coaching tip

## Dimensions scored

| Dimension | What it measures |
|-----------|-----------------|
| Relevance | Answer actually addresses the question + role |
| Clarity | Logical flow, no rambling, easy to follow |
| Tone | Professionalism, warmth, appropriateness |
| Structure | STAR / narrative structure, conciseness |
| Confidence | Assertive language, ownership, no hedging |

## Persona weight system

Each persona re-weights dimensions to match interviewer priorities:
- **Technical** → Relevance-heavy (35%)
- **HR** → Tone-heavy (30%)
- **Executive** → Confidence + Structure (25% each)
- **Sales** → Tone + Confidence (55% combined)

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
streamlit run app.py
```

## Stack

- Streamlit (UI)
- Anthropic Claude API (claude-sonnet-4-20250514)
- Prompt-engineered JSON rubric (zero fine-tuning)

---

## Resume headline

> Built GenAI candidate response evaluator using prompt engineering + LLM scoring rubrics;
> simulated enterprise hiring persona framework across 4 interviewer archetypes with
> weighted multi-dimension scoring dashboard
