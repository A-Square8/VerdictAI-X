"""
VerdictAI X Verdict Engine
"""



# Verdict Engine Prompt


VERDICT_SYSTEM_PROMPT = """You are the VerdictAI Verdict Engine. 
You are not an agent with a persona — you are the final synthesis system.
You have read all agent analyses, the full debate, and revised positions.

Your job:
1. Find the consensus clusters (what agents agree on)
2. Identify unresolved conflicts (what they still disagree about)
3. Determine the single deciding factor
4. Commit to one clear recommendation — no hedging
5. Explain exactly why this option wins
6. List trade-offs accepted
7. List risks to monitor
8. List Decision Trigger Points (What future signals would change the recommendation)
9. Assign confidence score (0-100)
10. Detect dominant emotional bias in user framing
11. Propose an alternative path if key conditions change

IMPORTANT RULE: The user base is predominantly Indian. All synthesis, logic, and action plans MUST assume an Indian context (Indian societal norms, INR financial realities, local corporate logic, and family dynamics). 

Be direct. Be specific. No hedging language. No "it depends" without resolution.
"""


SCORING_PROMPT = """Based on all the analysis and debate, score the recommended option:

Risk Score /100 (0 = very safe, 100 = extremely risky)
Growth Score /100 (0 = no growth potential, 100 = transformative upside)
Lifestyle Fit /100 (0 = poor fit, 100 = perfect fit)
Reversibility /100 (0 = irreversible, 100 = fully reversible)
Regret Probability /100 (0 = unlikely to regret, 100 = very likely to regret)

Return as JSON:
{
  "risk": <int>,
  "growth": <int>,
  "lifestyle": <int>,
  "reversibility": <int>,
  "regret": <int>,
  "confidence": <int>
}
"""




class VerdictEngine:
    """
    Final synthesis engine for VerdictAI X.
    To be fully wired to Gemini Pro in later stages.

    Attributes:
        user_decision: Original user input.
        analyses: First-pass agent analyses.
        transcript: Full debate transcript.
        revisions: Post-debate revised positions.
    """

    def __init__(
        self,
        user_decision: str,
        analyses: dict,
        transcript: list,
        revisions: dict,
    ):
        self.user_decision = user_decision
        self.analyses = analyses
        self.transcript = transcript
        self.revisions = revisions

    def build_synthesis_prompt(self) -> str:
        """Assembles all agent outputs into a single synthesis prompt."""
        lines = ["## USER DECISION\n", self.user_decision, "\n"]

        lines.append("## FIRST-PASS ANALYSES\n")
        for agent, analysis in self.analyses.items():
            lines.append(f"### {agent}\n{analysis}\n")

        lines.append("## DEBATE TRANSCRIPT\n")
        for msg in self.transcript:
            lines.append(f"{msg['agent']} [{msg['round']}]:\n{msg['text']}\n")

        lines.append("## REVISED POSITIONS\n")
        for agent, revision in self.revisions.items():
            lines.append(f"### {agent}\n{revision}\n")

        lines.append("\nNow synthesize everything above into the final verdict.")
        return "\n".join(lines)

    def generate_verdict(self, generate_fn) -> str:
        """
        Generates the final verdict using Gemini Pro.

        Args:
            generate_fn: Callable(prompt, system_prompt, use_pro=True) -> str
        """
        prompt = self.build_synthesis_prompt()
        return generate_fn(prompt, VERDICT_SYSTEM_PROMPT, use_pro=True)

    def generate_scores(self, generate_fn) -> dict:
        """
        Generates the scoring module output.

        Returns:
            Dict with risk, growth, lifestyle, reversibility, regret, confidence keys.
        """
        prompt = self.build_synthesis_prompt() + "\n\n" + SCORING_PROMPT
        raw = generate_fn(prompt, VERDICT_SYSTEM_PROMPT, use_pro=True)

        # Attempt JSON parse; return dummy scores if it fails
        import json
        try:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            return json.loads(raw[start:end])
        except Exception:
            return {
                "risk": 50,
                "growth": 50,
                "lifestyle": 50,
                "reversibility": 50,
                "regret": 50,
                "confidence": 50,
            }

    @staticmethod
    def format_scores_display(scores: dict) -> str:
        """Returns a formatted string representation of scores."""
        return (
            f" Risk: {scores.get('risk', '?')}/100  "
            f" Growth: {scores.get('growth', '?')}/100  "
            f" Lifestyle Fit: {scores.get('lifestyle', '?')}/100  "
            f" Reversibility: {scores.get('reversibility', '?')}/100  "
            f" Regret Probability: {scores.get('regret', '?')}/100  "
            f" Confidence: {scores.get('confidence', '?')}/100"
        )
