from datetime import datetime


def timestamp() -> str:
    """Returns current time as a formatted string for debate labels."""
    return datetime.now().strftime("%H:%M:%S")


def format_agent_header(agent_name: str, round_label: str = "") -> str:
    """Returns a formatted header string for an agent message block."""
    ts = timestamp()
    if round_label:
        return f"[{ts}] ── {agent_name.upper()} ({round_label}) ──"
    return f"[{ts}] ── {agent_name.upper()} ──"


def truncate(text: str, max_words: int = 150) -> str:
    """Truncates text to a maximum number of words."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "…"


def validate_input(user_input: str) -> tuple[bool, str]:
    """
    Basic validation of user decision input.
    Returns (is_valid, error_message).
    """
    if not user_input or not user_input.strip():
        return False, "Please describe your decision before submitting."
    if len(user_input.strip()) < 20:
        return False, "Please provide more detail about your decision (at least 20 characters)."
    if len(user_input) > 5000:
        return False, "Input too long. Please keep your decision description under 5000 characters."
    return True, ""


def build_empty_state() -> dict:
    """Returns an empty analysis state dictionary."""
    return {
        "user_input": "",
        "context": {},
        "agent_analyses": {},
        "debate_rounds": [],
        "revised_positions": {},
        "verdict": None,
        "scores": {},
    }


AGENT_COLORS = {
    "Strategist":   "#C9A84C",   # Gold
    "Guardian":     "#E8E8E8",   # White-silver
    "Visionary":    "#D4AF37",   # Deep gold
    "Humanist":     "#F5F5F0",   # Warm white
    "Contrarian":   "#A08020",   # Muted gold
    "Psychologist": "#CFCFCF",   # Light grey
}

# Lucide icon names (rendered via CDN in HTML)
AGENT_ICONS = {
    "Strategist":   "trending-up",
    "Guardian":     "shield",
    "Visionary":    "telescope",
    "Humanist":     "heart",
    "Contrarian":   "zap",
    "Psychologist": "brain",
}
