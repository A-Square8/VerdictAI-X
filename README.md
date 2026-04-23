# VerdictAI X

VerdictAI X is a high-end decision support system designed to provide guidance for individuals and small groups in making complex real-world decisions. Unlike standard conversational interfaces, it highlights the benefits of long-context language models and multi-agent systems through a structured reasoning process. Instead of a single answer, it provides a panel of AI agents who examine a situation from multiple perspectives to identify hidden aspects and provide balanced advice.

## How It Works

The platform follows a multi-stage pipeline to ensure a 360-degree view of any dilemma:

1. Input Ingestion: The system parses your decision, constraints, and implicit goals to establish a baseline analytical state.
2. Independent Analysis: Five specialized AI agents analyze the situation concurrently from their unique professional and personal perspectives.
3. Adversarial Debate: The agents engage in two rounds of live debate. In the first round, they challenge vulnerabilities in each other's logic. In the second, they defend their positions or refine their stances based on the pushback.
4. Final Synthesis: A dedicated Verdict Engine extracts consensus, resolves conflicts, and generates a final recommendation with quantified risk, growth, and confidence metrics.

## The Council of Agents

The system utilizes five distinct personas to cover all dimensions of a decision:

- The Strategist: Optimizes for long-term ROI, mathematical leverage, and compounding returns.
- The Guardian: Acts as the risk-mitigation layer, calculating financial runways and stress-testing positive assumptions.
- The Visionary: Scans for non-linear upside and exponential growth opportunities that might be overlooked.
- The Humanist: Evaluates psychological bandwidth, relationship impact, and alignment with personal core values.
- The Contrarian: Interrogates the initial framing of the decision to identify hidden shortcuts, biases, or systemic flaws.

## Technology Stack

- Language Models: Google Gemini 1.5 Flash (for high-speed analysis and debate) and Gemini 1.5 Pro (for final high-context synthesis).
- Interface: Gradio with a custom-engineered CSS layer for a premium, responsive dark-themed dashboard.
- Backend: Python with asynchronous streaming integration for real-time feedback during the analysis phase.
- Security: Environment-based secret management to ensure API keys are never exposed in the source code.
- Deployment: Optimized for production on Hugging Face Spaces.

## Getting Started

### 1. Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/A-Square8/VerdictAI-X
cd VerdictAI-X
pip install -r requirements.txt
```

### 2. Configuration

Set up your Gemini API key by creating a .env file from the example:

```bash
cp .env.example .env
# Open .env and paste your Gemini API key in the appropriate field
```

You can obtain a free API key from the Google AI Studio website.

### 3. Execution

Launch the application locally:

```bash
python app.py
```

Once the server is running, open the provided local URL in your web browser.

---
Built as a technical demonstration of advanced multi-agent orchestration and adversarial reasoning.
