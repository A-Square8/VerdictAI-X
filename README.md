<div align="center">

# VerdictAI X
### Multi-Agent Decision Intelligence

Five specialized AI agents debate your dilemma from opposing perspectives,
then synthesize a structured recommendation with quantified risk and confidence metrics.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash_&_Pro-4285F4?logo=google)
![Gradio](https://img.shields.io/badge/Interface-Gradio-orange)
![HuggingFace](https://img.shields.io/badge/Deployed-HuggingFace_Spaces-yellow?logo=huggingface)



</div>

## The Problem

Most AI tools give you one answer from one perspective. Real decisions are messier than that —
they involve tradeoffs between risk, growth, values, and timing that a single viewpoint misses.
VerdictAI X runs your decision through five adversarial agents who challenge each other,
then distills the debate into a final verdict.

## Snaps

<img width="1916" height="904" alt="image" src="https://github.com/user-attachments/assets/d860bd9a-015b-449b-bba5-88263246b1d5" />
<img width="1916" height="904" alt="image" src="https://github.com/user-attachments/assets/d236e15d-d138-4756-8800-8eb2b5f99a57" />

## How It Works

**1. Input Ingestion**
The system parses your decision, stated constraints, and implicit goals to establish a baseline analytical state.

**2. Independent Analysis**
Five agents analyze the situation concurrently, each from a distinct professional and psychological lens.

**3. Adversarial Debate**
Two rounds of live debate. Round one: agents attack vulnerabilities in each other's reasoning.
Round two: agents defend or revise their position based on the pushback received.

**4. Final Synthesis**
A dedicated Verdict Engine resolves conflicts, extracts consensus, and produces a final recommendation
with quantified risk, growth potential, and confidence scores.

## The Council

| Agent | Role |
|---|---|
| The Strategist | Optimizes for long-term ROI, mathematical leverage, and compounding returns |
| The Guardian | Risk-mitigation layer — calculates financial runways and stress-tests assumptions |
| The Visionary | Scans for non-linear upside and exponential opportunities that others overlook |
| The Humanist | Evaluates psychological cost, relationship impact, and alignment with personal values |
| The Contrarian | Interrogates the framing itself — surfaces hidden biases, shortcuts, and systemic flaws |

## Technology Stack

| Layer | Technology |
|---|---|
| Analysis LLM | Gemini 1.5 Flash — high-speed concurrent agent reasoning |
| Synthesis LLM | Gemini 1.5 Pro — high-context final verdict generation |
| Interface | Gradio with custom dark-themed CSS layer |
| Backend | Python with async streaming for real-time output |
| Deployment | Hugging Face Spaces |
| Security | Environment-based secret management, no keys in source |

## Setup

```bash
git clone https://github.com/A-Square8/VerdictAI-X
cd VerdictAI-X
pip install -r requirements.txt

cp .env.example .env
# Add your Gemini API key to .env
# Get a free key at Google AI Studio

python app.py
```

Built as a technical demonstration of multi-agent orchestration and adversarial reasoning pipelines.
