"""
VerdictAI X Debate Engine
"""

from agents import AGENT_NAMES, build_debate_prompt, build_revision_prompt, AGENT_PERSONAS
from utils import format_agent_header, truncate




class DebateOrchestrator:
   

    def __init__(self, user_decision: str, analyses: dict):
        self.user_decision = user_decision
        self.analyses = analyses
        self.transcript: list[dict] = []
        self.revisions: dict = {}

    def _build_debate_context(self) -> str:
        if not self.transcript:
            lines = []
            for agent, analysis in self.analyses.items():
                lines.append(f"{agent}:\n{analysis}\n")
            return "\n".join(lines)

        lines = []
        for msg in self.transcript:
            lines.append(f"{msg['agent']} [{msg['round']}]:\n{msg['text']}\n")
        return "\n".join(lines)

    def run_debate_round(self, round_num: int, generate_fn) -> list[dict]:
        
        round_messages = []
        debate_context = self._build_debate_context()

        for agent_name in AGENT_NAMES:
            prompt = build_debate_prompt(
                self.user_decision,
                agent_name,
                debate_context,
                round_num,
            )
            system_prompt = AGENT_PERSONAS[agent_name]
            text = generate_fn(prompt, system_prompt)
            text = truncate(text, max_words=80)

            msg = {
                "agent": agent_name,
                "round": f"Round {round_num}",
                "text": text,
                "header": format_agent_header(agent_name, f"Round {round_num}"),
            }
            self.transcript.append(msg)
            round_messages.append(msg)

           
            debate_context = self._build_debate_context()

        return round_messages

    def run_revision_round(self, generate_fn) -> dict:
        """
        Asks each agent to state their revised position after debate.

        Args:
            generate_fn: Callable(prompt, system_prompt) -> str

        Returns:
            Dict mapping agent_name -> revision text.
        """
        full_debate = self._build_debate_context()

        for agent_name in AGENT_NAMES:
            original = self.analyses.get(agent_name, "No original analysis.")
            prompt = build_revision_prompt(
                self.user_decision,
                agent_name,
                original,
                full_debate,
            )
            system_prompt = AGENT_PERSONAS[agent_name]
            revision = generate_fn(prompt, system_prompt)
            self.revisions[agent_name] = truncate(revision, max_words=60)

        return self.revisions

    def get_full_transcript(self) -> list[dict]:
        return self.transcript

    def get_revisions(self) -> dict:
        return self.revisions
