"""
VerdictAI X Main Application
"""

import gradio as gr
from datetime import datetime

from agents import AGENT_PERSONAS, build_analysis_prompt, build_debate_prompt
from gemini_client import generate_stream, generate
from engine import VerdictEngine, VERDICT_SYSTEM_PROMPT
from utils import validate_input, truncate



STAGE2_AGENTS = ["Strategist", "Guardian", "Visionary", "Humanist", "Contrarian"]

# Agent badges
AGENT_BADGE_STYLES = {
    "Strategist": "background:rgba(30,58,138,0.3); color:#60a5fa; border:1px solid rgba(96,165,250,0.2);",
    "Guardian":   "background:rgba(120,53,15,0.3); color:#fbbf24; border:1px solid rgba(251,191,36,0.2);",
    "Visionary":  "background:rgba(88,28,135,0.3); color:#c084fc; border:1px solid rgba(192,132,252,0.2);",
    "Humanist":   "background:rgba(136,19,55,0.3); color:#fb7185; border:1px solid rgba(251,113,133,0.2);",
    "Contrarian": "background:rgba(64,64,64,0.3); color:#a3a3a3; border:1px solid rgba(163,163,163,0.2);",
}

AGENT_CIRCLE_COLORS = {
    "Strategist": "#2563eb",
    "Guardian":   "#d97706",
    "Visionary":  "#7c3aed",
    "Humanist":   "#dc2626",
    "Contrarian": "#4b5563",
}



CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }
html, body { height: 100%; overflow-x: hidden; }

body,
.gradio-container,
.gradio-container > .main,
.gradio-container > .main > .wrap {
    background: #050505 !important;
    color: #eae1d4 !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 100vh !important;
}

.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Hide Gradio chrome */
footer { display: none !important; }
.gr-prose { display: none !important; }
#component-0 { padding: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.2); border-radius: 10px; }

/* ══════════════════════════════════════════
   DASHBOARD ROW
══════════════════════════════════════════ */
#dashboard-row {
    max-width: 1440px !important;
    margin: 0 auto !important;
    padding: 0 32px 48px 32px !important;
    gap: 24px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    align-items: stretch !important;
}

#dashboard-row > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ── Left: Input Panel ── */
#input-col {
    background: #111111 !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
    border-radius: 16px !important;
    padding: 8px !important;
    box-shadow: 0 0 20px -5px rgba(212,175,55,0.2) !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
}

/* ── Center: Debate Panel ── */
#debate-col {
    background: transparent !important;
    padding: 0 !important;
    overflow: hidden !important;
}

/* ── Right: Metrics Panel ── */
#metrics-col {
    background: transparent !important;
    padding: 0 !important;
}

/* ══════════════════════════════════════════
   GRADIO COMPONENT OVERRIDES
══════════════════════════════════════════ */

/* Decision textbox */
#decision-input { background: transparent !important; }
#decision-input label > span { display: none !important; }
#decision-input textarea {
    background: #080808 !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
    padding: 16px !important;
    resize: none !important;
    transition: border-color 0.2s !important;
    min-height: 260px !important;
    box-shadow: none !important;
    pointer-events: auto !important;
}
#decision-input textarea:focus {
    border-color: #D4AF37 !important;
    outline: none !important;
    box-shadow: 0 0 0 1px #D4AF37 !important;
}
#decision-input textarea::placeholder { color: #6b7280 !important; }

/* Buttons */
#btn-submit {
    background: #D4AF37 !important;
    color: #050505 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    padding: 16px 24px !important;
    cursor: pointer !important;
    width: 100% !important;
    transition: all 0.2s !important;
    min-height: 52px !important;
}
#btn-submit:hover {
    filter: brightness(1.1) !important;
    box-shadow: 0 4px 20px rgba(212,175,55,0.3) !important;
}

/* Status textbox */
#vai-status > label { display: none !important; }
#vai-status { background: transparent !important; }
#vai-status textarea, #vai-status input {
    background: transparent !important;
    color: #6b7280 !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    padding: 8px 0 !important;
    min-height: unset !important;
    line-height: 1.5 !important;
}

/* Hidden components */
.agent-hidden { display: none !important; }
.agent-hidden > label { display: none !important; }
#score-out { display: none !important; }

/* ── Verdict Row ── */
#verdict-row {
    max-width: 1440px !important;
    margin: 0 auto !important;
    padding: 0 32px 0 32px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
#verdict-col {
    background: #111111 !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
    border-radius: 16px !important;
    padding: 40px !important;
    box-shadow: 0 0 20px -5px rgba(212,175,55,0.2) !important;
}

/* Markdown styling for Verdict Output */
#verdict-markdown {
    background: transparent !important;
    margin-top: 24px;
}
#verdict-markdown h1, #verdict-markdown h2, #verdict-markdown h3 {
    color: #D4AF37 !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-top: 24px !important;
    margin-bottom: 12px !important;
}
#verdict-markdown p {
    color: #d1d5db !important;
    line-height: 1.6 !important;
}
#verdict-markdown ul {
    list-style-type: none !important;
    padding-left: 0 !important;
}
#verdict-markdown li {
    position: relative !important;
    padding-left: 20px !important;
    margin-bottom: 8px !important;
    color: #9ca3af !important;
    line-height: 1.6 !important;
}
#verdict-markdown li::before {
    content: '•' !important;
    position: absolute !important;
    left: 0 !important;
    color: #D4AF37 !important;
    font-weight: 700 !important;
}

/* ── Responsive ── */
@media (max-width: 900px) {
    #dashboard-row { flex-direction: column !important; }
    .verdict-grid-inner { grid-template-columns: 1fr !important; }
}

/* ── Debate feed container ── */
#debate-feed-container { background: transparent !important; padding: 0 !important; }
#debate-feed-container > div { background: transparent !important; }
"""


NAVBAR_HTML = """
<nav style="position:fixed; top:0; z-index:50; display:flex; justify-content:space-between; align-items:center; width:100%; padding:0 48px; height:80px; background:#050505; border-bottom:1px solid rgba(212,175,55,0.3); font-family:Inter,sans-serif;">
  <div style="font-size:20px; font-weight:700; letter-spacing:0.1em; color:#D4AF37; cursor:pointer;" onclick="document.getElementById('home-view').style.display='flex'; document.getElementById('about-view').style.display='none';">VerdictAI X</div>
  <div style="display:flex; align-items:center; gap:32px;">
    <a href="#" onclick="document.getElementById('home-view').style.display='flex'; document.getElementById('about-view').style.display='none'; return false;" style="font-size:13px; text-transform:uppercase; color:#D4AF37; border-bottom:1px solid #D4AF37; padding-bottom:4px; text-decoration:none; letter-spacing:0.02em;">AI - Main</a>
    <a href="#" onclick="document.getElementById('home-view').style.display='none'; document.getElementById('about-view').style.display='flex'; return false;" style="font-size:13px; text-transform:uppercase; color:#737373; text-decoration:none; letter-spacing:0.02em;">About</a>
    <a href="https://drive.google.com/file/d/14cA0sK-uA48-u8abrEj_mDPVvclr3N6Y/view?usp=drive_link" target="_blank" style="font-size:13px; text-transform:uppercase; color:#737373; text-decoration:none; letter-spacing:0.02em;">Demo</a>
    <a href="https://github.com/A-Square8/VerdictAI-X" target="_blank" style="font-size:13px; text-transform:uppercase; color:#737373; text-decoration:none; letter-spacing:0.02em;">GitHub</a>
  </div>
  <div style="display:flex; min-width: 120px;"></div>
</nav>
"""

HERO_HTML = """
<section style="position:relative; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; overflow:hidden; font-family:Inter,sans-serif;">
  <div style="position:absolute; inset:0; z-index:0; opacity:0.2; pointer-events:none; background:radial-gradient(circle at 50% 50%, rgba(212,175,55,0.15) 0%, transparent 70%);"></div>
  <span style="color:#a3a3a3; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:16px; background:rgba(255,255,255,0.05); padding:8px 20px; border-radius:9999px; position:relative; z-index:1;">Select desktop mode or view on large screen</span>
  <h1 style="font-size:64px; font-weight:700; line-height:1.1; max-width:900px; margin-bottom:24px; color:#D4AF37; letter-spacing:-0.02em; text-transform:uppercase; position:relative; z-index:1;">
    Watch AI Experts Debate Your Biggest Decisions
  </h1>
  <p style="font-size:18px; color:#9ca3af; max-width:640px; margin-bottom:40px; line-height:1.6; position:relative; z-index:1;">
    Five specialized AI agents analyze your choices, challenge each other live, and deliver one clear recommendation.
  </p>
</section>
"""

ABOUT_HTML = """
<section style="min-height: 100vh; padding: 140px 32px 80px 32px; font-family: Inter, sans-serif; display: flex; justify-content: center; background: radial-gradient(circle at top, rgba(212,175,55,0.05) 0%, transparent 60%);">
  <div style="max-width: 1000px; width: 100%;">
    
    <div style="text-align: center; margin-bottom: 64px;">
      <h1 style="color:#D4AF37; font-size:48px; font-weight:700; text-transform:uppercase; letter-spacing:-0.02em; margin-bottom:24px;">The Architecture of Decision</h1>
      <p style="color:#d1d5db; font-size:18px; line-height:1.8; max-width: 800px; margin: 0 auto;">
Verdict AI is a high-end decision support system designed to provide guidance for regular individuals and small groups in making realistic decisions. This tool is not your usual conversational interface because it highlights the benefits of long-context language models and multi-agent systems through its reasoning process. Unlike most other systems that provide you with a generalized solution, Verdict AI creates a panel of AI agents who examine a situation from multiple perspectives to identify hidden aspects and provide balanced advice.      </p>
    </div>

    <!-- The Pipeline -->
    <div style="background:#111111; border:1px solid rgba(212,175,55,0.2); border-radius:16px; padding:48px; box-shadow:0 0 30px -10px rgba(212,175,55,0.1); margin-bottom: 64px;">
      <h2 style="color:#D4AF37; font-size:20px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:32px; border-bottom: 1px solid rgba(212,175,55,0.2); padding-bottom: 16px;">The Reasoning Pipeline</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px;">
        <div>
          <span style="color:#f3f4f6; font-size:16px; font-weight:700; margin-bottom:8px; display:block;">1. High-Context Ingestion</span>
          <p style="color:#9ca3af; font-size:14px; line-height:1.6; margin:0;">Parsing user dilemmas, constraints, and implicit goals to establish a baseline analytical state.</p>
        </div>
        <div>
          <span style="color:#f3f4f6; font-size:16px; font-weight:700; margin-bottom:8px; display:block;">2. Multi-Agent Orchestration</span>
          <p style="color:#9ca3af; font-size:14px; line-height:1.6; margin:0;">Concurrent, isolated execution of specialized system prompts via high-speed LLM routing.</p>
        </div>
        <div>
          <span style="color:#f3f4f6; font-size:16px; font-weight:700; margin-bottom:8px; display:block;">3. Adversarial Debate Layer</span>
          <p style="color:#9ca3af; font-size:14px; line-height:1.6; margin:0;">Two iterative rounds of context-building where agents challenge vulnerabilities in each other's logic.</p>
        </div>
        <div>
          <span style="color:#f3f4f6; font-size:16px; font-weight:700; margin-bottom:8px; display:block;">4. Verdict Synthesis Engine</span>
          <p style="color:#9ca3af; font-size:14px; line-height:1.6; margin:0;">A final algorithmic pass extracting consensus, resolving conflict, and generating quantified risk metrics.</p>
        </div>
      </div>
    </div>

    <!-- The Agents -->
    <div style="background:#0a0a0a; border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:48px;">
      <h2 style="color:#ffffff; font-size:20px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:40px;">The Specialized Nodes</h2>
      
      <div style="margin-bottom: 32px;">
        <span style="color:#60a5fa; font-size:16px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; display:block; margin-bottom:8px;">The Strategist</span>
        <p style="color:#9ca3af; font-size:15px; line-height:1.6; margin:0;">Optimizes for compounding returns, leverage, and long-term trajectory. This node evaluates the mathematical and career capitals at stake, ensuring the final action pathway maximizes overall ROI.</p>
      </div>

      <div style="margin-bottom: 32px;">
        <span style="color:#fbbf24; font-size:16px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; display:block; margin-bottom:8px;">The Guardian</span>
        <p style="color:#9ca3af; font-size:15px; line-height:1.6; margin:0;">The system's explicit risk-mitigation layer. It stress-tests positive assumptions, calculates financial runways, and maps worst-case scenarios to ensure decisions maintain an embedded safety margin.</p>
      </div>

      <div style="margin-bottom: 32px;">
        <span style="color:#c084fc; font-size:16px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; display:block; margin-bottom:8px;">The Visionary</span>
        <p style="color:#9ca3af; font-size:15px; line-height:1.6; margin:0;">Scans the probability space for non-linear upside and exponential growth trajectories. It forces the core engine to confront the maximum possible potential of options rather than settling for incremental gains.</p>
      </div>

      <div style="margin-bottom: 32px;">
        <span style="color:#fb7185; font-size:16px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; display:block; margin-bottom:8px;">The Humanist</span>
        <p style="color:#9ca3af; font-size:15px; line-height:1.6; margin:0;">Grounds the calculation in human reality. It evaluates psychological bandwidth, relationship impact, and alignment with core identity to prevent systemic burnout and ensure sustainable execution.</p>
      </div>

      <div>
        <span style="color:#a3a3a3; font-size:16px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; display:block; margin-bottom:8px;">The Contrarian</span>
        <p style="color:#9ca3af; font-size:15px; line-height:1.6; margin:0;">An adversarial counter-measure against analytical groupthink. It actively interrogates the initial framing, seeking hidden third options, challenging biases, and exposing systemic flaws in the overarching premise.</p>
      </div>

    </div>

  </div>
</section>
"""

INPUT_HEADER_HTML = """
<div style="padding:16px 16px 0 16px; margin-bottom:16px;">
  <span style="color:#D4AF37; font-family:Inter,sans-serif; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.1em;">Decision Input</span>
</div>
"""

def _build_metrics_html(confidence=None, risk=None, growth=None) -> str:
    def format_gauge(val, color, title):
        if val is None:
            val_str = "—"
            offset = 251.2
        else:
            val_str = str(int(val))
            offset = 251.2 * (1 - (val / 100))
        return f"""
  <div style="background:#111111; border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:24px; display:flex; flex-direction:column; align-items:center; justify-content:center; flex:1; transition:all 0.3s; position:relative;">
    <span style="color:#D4AF37; font-family:Inter,sans-serif; font-size:11px; font-weight:600; text-transform:uppercase; margin-bottom:16px; letter-spacing:0.1em;">{title}</span>
    <div style="position:relative; width:96px; height:96px; display:flex; align-items:center; justify-content:center;">
      <svg style="width:100%; height:100%; transform:rotate(-90deg);" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r="40" fill="transparent" stroke="rgba(255,255,255,0.05)" stroke-width="4"/>
        <circle cx="48" cy="48" r="40" fill="transparent" stroke="{color}" stroke-width="4" stroke-dasharray="251.2" stroke-dashoffset="{offset}" style="transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1);"/>
      </svg>
      <span style="position:absolute; font-size:20px; font-weight:700; color:#ffffff; font-family:Inter,sans-serif;">{val_str}</span>
    </div>
  </div>"""

    return f"""
<div style="display:flex; flex-direction:column; gap:24px; height:100%;">
  {format_gauge(confidence, "#D4AF37", "Confidence")}
  {format_gauge(risk, "#f43f5e", "Risk Index")}
  {format_gauge(growth, "#10b981", "Growth Pot.")}
</div>
"""


def _build_verdict_top_html(confidence=None) -> str:
    conf_str = f"{confidence}%" if confidence is not None else "—"
    return f"""
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(212,175,55,0.2); padding-bottom:32px; flex-wrap:wrap; gap:16px;">
    <div>
      <span style="color:#D4AF37; font-family:Inter,sans-serif; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; display:block; margin-bottom:8px;">The Final Decision</span>
      <h2 style="font-family:Inter,sans-serif; font-weight:700; font-size:36px; color:#ffffff; text-transform:uppercase; letter-spacing:-0.01em; margin:0;">Analysis Verdict</h2>
    </div>
    <div style="display:flex; align-items:center; gap:16px;">
      <div style="text-align:right;">
        <span style="color:#737373; font-family:Inter,sans-serif; font-size:11px; font-weight:600; display:block;">EXPECTED SUCCESS</span>
        <span style="color:#D4AF37; font-size:24px; font-weight:700; font-family:Inter,sans-serif;">{conf_str}</span>
      </div>
      <span style="font-family:'Material Symbols Outlined'; font-size:36px; color:#D4AF37;">verified</span>
    </div>
  </div>
"""

FOOTER_HTML = """
<footer style="margin-top:64px; padding:48px 32px; border-top:1px solid rgba(255,255,255,0.05); background:#080808; font-family:Inter,sans-serif;">
  <div style="max-width:1440px; margin:0 auto; display:flex; justify-content:space-between; align-items:center; opacity:0.5; flex-wrap:wrap; gap:24px;">
    <div style="font-size:14px; font-weight:700; letter-spacing:0.1em; color:#D4AF37;">VerdictAI X — 2024</div>
    <div style="display:flex; gap:32px;">
      <a href="#" style="font-size:12px; text-transform:uppercase; letter-spacing:0.1em; color:#9ca3af; text-decoration:none;">Privacy Policy</a>
      <a href="#" style="font-size:12px; text-transform:uppercase; letter-spacing:0.1em; color:#9ca3af; text-decoration:none;">Terms of Service</a>
      <a href="#" style="font-size:12px; text-transform:uppercase; letter-spacing:0.1em; color:#9ca3af; text-decoration:none;">Security</a>
    </div>
  </div>
</footer>
"""




def _build_agent_bubble(agent_name: str, text: str, ts: str, is_right: bool = False) -> str:
    """Builds a single chat-bubble HTML block for an agent."""
    badge_style = AGENT_BADGE_STYLES.get(agent_name, "background:#333; color:#aaa; border:1px solid #555;")

    if is_right:
        return f"""
<div style="display:flex; flex-direction:column; align-items:flex-end; margin-left:auto; max-width:90%;">
  <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
    <span style="color:#525252; font-size:10px; font-family:Inter,sans-serif;">{ts}</span>
    <span style="padding:4px 12px; border-radius:9999px; font-size:10px; font-weight:700; text-transform:uppercase; font-family:Inter,sans-serif; {badge_style}">{agent_name}</span>
  </div>
  <div style="background:#181818; padding:16px; border-radius:16px; border-top-right-radius:0; border:1px solid rgba(255,255,255,0.05); color:#d1d5db; line-height:1.6; font-size:14px; font-family:Inter,sans-serif;">
    {text}
  </div>
</div>"""
    else:
        return f"""
<div style="display:flex; flex-direction:column; align-items:flex-start; max-width:90%;">
  <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
    <span style="padding:4px 12px; border-radius:9999px; font-size:10px; font-weight:700; text-transform:uppercase; font-family:Inter,sans-serif; {badge_style}">{agent_name}</span>
    <span style="color:#525252; font-size:10px; font-family:Inter,sans-serif;">{ts}</span>
  </div>
  <div style="background:#181818; padding:16px; border-radius:16px; border-top-left-radius:0; border:1px solid rgba(255,255,255,0.05); color:#d1d5db; line-height:1.6; font-size:14px; font-family:Inter,sans-serif;">
    {text}
  </div>
</div>"""


def _build_progress_bar(current_agent_idx: int, total: int, status_label: str) -> str:
    """Builds the bottom progress bar HTML."""
    pct = int((current_agent_idx / total) * 100) if total > 0 else 0
    circles = ""
    letters = {"Strategist": "S", "Guardian": "G", "Visionary": "V", "Humanist": "H", "Contrarian": "C"}
    for i, name in enumerate(STAGE2_AGENTS):
        color = AGENT_CIRCLE_COLORS[name]
        opacity = "1" if i <= current_agent_idx else "0.3"
        mr = "margin-right:-12px;" if i < len(STAGE2_AGENTS) - 1 else ""
        z = len(STAGE2_AGENTS) - i
        circles += f'<div style="width:32px; height:32px; border-radius:50%; background:{color}; border:2px solid #111111; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; color:#fff; {mr} position:relative; z-index:{z}; opacity:{opacity};">{letters[name]}</div>'

    return f"""
<div style="padding:16px; background:rgba(22,22,22,0.5); backdrop-filter:blur(12px); border-radius:0 0 16px 16px; flex-shrink:0;">
  <div style="display:flex; gap:16px; align-items:center;">
    <div style="display:flex;">{circles}</div>
    <div style="flex:1; height:4px; background:rgba(255,255,255,0.05); border-radius:9999px; overflow:hidden;">
      <div style="height:100%; background:#D4AF37; width:{pct}%; box-shadow:0 0 10px #D4AF37; transition:width 0.3s;"></div>
    </div>
    <span style="font-size:10px; color:#737373; font-weight:700; font-family:Inter,sans-serif;">{status_label}</span>
  </div>
</div>"""


def _build_feed_html(bubbles_html: str, progress_html: str, active_count: int = 5,
                     status_color: str = "#10b981", status_text: str = "5 AGENTS ACTIVE") -> str:
    """Wraps bubbles + progress into the full debate feed container."""
    return f"""
<style>@keyframes vai-pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}</style>
<div style="background:#111111; border:1px solid rgba(255,255,255,0.05); border-radius:16px; min-height:600px; max-height:800px; height:75vh; display:flex; flex-direction:column; position:relative; overflow:hidden;">
  <!-- Header -->
  <div style="padding:24px; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items:center; background:#161616; border-radius:16px 16px 0 0; flex-shrink:0;">
    <h2 style="color:#D4AF37; font-family:Inter,sans-serif; font-weight:600; text-transform:uppercase; font-size:18px; letter-spacing:0.1em; margin:0;">Live Debate Feed</h2>
    <div style="display:flex; align-items:center; gap:8px;">
      <span style="width:8px; height:8px; background:{status_color}; border-radius:50%; display:inline-block; animation:vai-pulse 2s infinite;"></span>
      <span style="color:{status_color}; font-family:Inter,sans-serif; font-size:11px; font-weight:600;">{status_text}</span>
    </div>
  </div>
  <!-- Messages -->
  <div id="vai-debate-scroller" style="flex:1; overflow-y:auto; padding:24px; display:flex; flex-direction:column; gap:24px;">
    {bubbles_html}
    <img src="x" onerror="var el=document.getElementById('vai-debate-scroller'); if(el)el.scrollTop=el.scrollHeight; this.remove();" style="display:none;"/>
  </div>
  <!-- Progress -->
  {progress_html}
</div>"""


def _build_idle_feed() -> str:
    """Returns the default idle state of the debate feed."""
    bubbles = ""
    idle_messages = {
        "Strategist": "Awaiting decision input. The Strategist will analyze returns, opportunity cost, and competitive positioning of your options.",
        "Guardian": "Standing by to map worst-case scenarios and hidden risks in your decision landscape.",
        "Humanist": "Ready to evaluate how each option aligns with your values, wellbeing, and day-to-day happiness.",
        "Visionary": "Prepared to identify the maximum upside and bold moves that could change your trajectory entirely.",
        "Contrarian": "Will challenge assumptions and explore unconventional alternatives hiding in plain sight.",
    }
    for i, name in enumerate(STAGE2_AGENTS):
        is_right = i % 2 == 1
        bubbles += _build_agent_bubble(name, idle_messages[name], "--:--:--", is_right)
    progress = _build_progress_bar(-1, len(STAGE2_AGENTS), "WAITING")
    return _build_feed_html(bubbles, progress)


# Debate html helpers


def _build_debate_bubble(agent_name: str, text: str, ts: str, round_label: str, is_right: bool = False) -> str:
    """Builds a debate-round chat bubble with a round indicator."""
    badge_style = AGENT_BADGE_STYLES.get(agent_name, "background:#333; color:#aaa; border:1px solid #555;")
    round_color = "#D4AF37" if "1" in round_label else "#10b981"
    border_rgba = "rgba(212,175,55,0.15)" if "1" in round_label else "rgba(16,185,129,0.15)"

    if is_right:
        return f"""
<div style="display:flex; flex-direction:column; align-items:flex-end; margin-left:auto; max-width:90%;">
  <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
    <span style="color:{round_color}; font-size:9px; font-family:Inter,sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:0.1em;">{round_label}</span>
    <span style="color:#525252; font-size:10px; font-family:Inter,sans-serif;">{ts}</span>
    <span style="padding:4px 12px; border-radius:9999px; font-size:10px; font-weight:700; text-transform:uppercase; font-family:Inter,sans-serif; {badge_style}">{agent_name}</span>
  </div>
  <div style="background:#181818; padding:16px; border-radius:16px; border-top-right-radius:0; border:1px solid {border_rgba}; color:#d1d5db; line-height:1.6; font-size:14px; font-family:Inter,sans-serif;">
    {text}
  </div>
</div>"""
    else:
        return f"""
<div style="display:flex; flex-direction:column; align-items:flex-start; max-width:90%;">
  <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
    <span style="padding:4px 12px; border-radius:9999px; font-size:10px; font-weight:700; text-transform:uppercase; font-family:Inter,sans-serif; {badge_style}">{agent_name}</span>
    <span style="color:#525252; font-size:10px; font-family:Inter,sans-serif;">{ts}</span>
    <span style="color:{round_color}; font-size:9px; font-family:Inter,sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:0.1em;">{round_label}</span>
  </div>
  <div style="background:#181818; padding:16px; border-radius:16px; border-top-left-radius:0; border:1px solid {border_rgba}; color:#d1d5db; line-height:1.6; font-size:14px; font-family:Inter,sans-serif;">
    {text}
  </div>
</div>"""


def _build_debate_separator(label: str) -> str:

    return f"""
<div style="display:flex; align-items:center; gap:16px; padding:8px 0;">
  <div style="flex:1; height:1px; background:rgba(212,175,55,0.3);"></div>
  <span style="color:#D4AF37; font-family:Inter,sans-serif; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.15em; white-space:nowrap;">{label}</span>
  <div style="flex:1; height:1px; background:rgba(212,175,55,0.3);"></div>
</div>"""


def _build_debate_progress(round_num: int, agent_idx: int, total_agents: int, status_label: str) -> str:
    """Progress bar for debate rounds (shared across both rounds)."""
    # Overall progress: round 1 = 0-50%, round 2 = 50-100%
    round_base = 0 if round_num == 1 else 50
    agent_pct = int((agent_idx / total_agents) * 50) if total_agents > 0 else 0
    pct = round_base + agent_pct

    circles = ""
    letters = {"Strategist": "S", "Guardian": "G", "Visionary": "V", "Humanist": "H", "Contrarian": "C"}
    for i, name in enumerate(STAGE2_AGENTS):
        color = AGENT_CIRCLE_COLORS[name]
        mr = "margin-right:-12px;" if i < len(STAGE2_AGENTS) - 1 else ""
        z = len(STAGE2_AGENTS) - i
        circles += f'<div style="width:32px; height:32px; border-radius:50%; background:{color}; border:2px solid #111111; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; color:#fff; {mr} position:relative; z-index:{z};">{letters[name]}</div>'

    return f"""
<div style="padding:16px; background:rgba(22,22,22,0.5); backdrop-filter:blur(12px); border-radius:0 0 16px 16px; flex-shrink:0;">
  <div style="display:flex; gap:16px; align-items:center;">
    <div style="display:flex;">{circles}</div>
    <div style="flex:1; height:4px; background:rgba(255,255,255,0.05); border-radius:9999px; overflow:hidden;">
      <div style="height:100%; background:#D4AF37; width:{pct}%; box-shadow:0 0 10px #D4AF37; transition:width 0.3s;"></div>
    </div>
    <span style="font-size:10px; color:#737373; font-weight:700; font-family:Inter,sans-serif;">{status_label}</span>
  </div>
</div>"""


# Streaming handler

def handle_submit(decision_text: str):

    is_valid, error_msg = validate_input(decision_text)
    if not is_valid:
        yield (
            "⚠  " + error_msg,
            _build_idle_feed(),
            _build_metrics_html(),
            _build_verdict_top_html(),
            ""
        )
        return

    yield (
        "◈  Starting Analysis...",
        _build_idle_feed(),
        _build_metrics_html(),
        _build_verdict_top_html(),
        ""
    )

    # first pass
    completed_bubbles = []   
    agent_results = {}      

    for idx, agent_name in enumerate(STAGE2_AGENTS):
        ts = datetime.now().strftime("%H:%M:%S")
        is_right = idx % 2 == 1
        status = f"◈  Analyzing — {agent_name} ({idx + 1}/{len(STAGE2_AGENTS)})"

        system_prompt = AGENT_PERSONAS[agent_name]
        prompt = build_analysis_prompt(decision_text, agent_name)

        accumulated = ""
        for chunk in generate_stream(prompt, system_prompt, use_pro=False):
            accumulated += chunk
            current_bubble = _build_agent_bubble(agent_name, accumulated + "▍", ts, is_right)
            all_bubbles = "\n".join(completed_bubbles + [current_bubble])
            progress = _build_progress_bar(idx, len(STAGE2_AGENTS), f"{agent_name.upper()}")
            feed_html = _build_feed_html(
                all_bubbles, progress,
                status_color="#D4AF37",
                status_text=f"ANALYZING — {agent_name.upper()}"
            )
            yield (status, feed_html, _build_metrics_html(), _build_verdict_top_html(), "")

        final_text = accumulated.strip()
        agent_results[agent_name] = final_text
        finished_bubble = _build_agent_bubble(agent_name, final_text, ts, is_right)
        completed_bubbles.append(finished_bubble)

        all_bubbles = "\n".join(completed_bubbles)
        progress = _build_progress_bar(idx + 1, len(STAGE2_AGENTS),
                                       "ANALYSIS DONE" if idx == len(STAGE2_AGENTS) - 1 else f"NEXT: {STAGE2_AGENTS[idx + 1].upper()}")
        feed_html = _build_feed_html(
            all_bubbles, progress,
            status_color="#D4AF37" if idx < len(STAGE2_AGENTS) - 1 else "#10b981",
            status_text=f"NEXT: {STAGE2_AGENTS[idx + 1].upper()}" if idx < len(STAGE2_AGENTS) - 1 else "ANALYSIS COMPLETE"
        )
        done_status = f"✓  {agent_name} complete" if idx < len(STAGE2_AGENTS) - 1 else "✓  All 5 agents complete — starting debate"
        yield (done_status, feed_html, _build_metrics_html(), _build_verdict_top_html(), "")

    # STAGE 3 — Live debate 
    # Build initial debate context from first-pass analyses
    debate_transcript = []  

    def _build_debate_context():
        """Formats analyses + debate transcript into context string for prompts."""
        lines = []
        for agent, analysis in agent_results.items():
            lines.append(f"{agent} (Analysis):\n{analysis}\n")
        for msg in debate_transcript:
            lines.append(f"{msg['agent']} [{msg['round']}]:\n{msg['text']}\n")
        return "\n".join(lines)

    round_labels = {1: "Round 1 — Challenge", 2: "Round 2 — Defend"}

    for round_num in range(1, 3):
        round_label = round_labels[round_num]


        separator = _build_debate_separator(round_label)
        completed_bubbles.append(separator)


        all_bubbles = "\n".join(completed_bubbles)
        progress = _build_debate_progress(round_num, 0, len(STAGE2_AGENTS), f"ROUND {round_num}")
        feed_html = _build_feed_html(
            all_bubbles, progress,
            status_color="#D4AF37",
            status_text=f"DEBATE ROUND {round_num}"
        )
        yield (f"◈  Debate {round_label}", feed_html, _build_metrics_html(), _build_verdict_top_html(), "")

        for idx, agent_name in enumerate(STAGE2_AGENTS):
            ts = datetime.now().strftime("%H:%M:%S")
            is_right = idx % 2 == 1
            status = f"◈  {round_label} — {agent_name} ({idx + 1}/{len(STAGE2_AGENTS)})"

            # Build debate prompt using current context
            debate_context = _build_debate_context()
            system_prompt = AGENT_PERSONAS[agent_name]
            prompt = build_debate_prompt(
                decision_text,
                agent_name,
                debate_context,
                round_num,
            )

            # Stream debate response
            accumulated = ""
            for chunk in generate_stream(prompt, system_prompt, use_pro=False):
                accumulated += chunk
                current_bubble = _build_debate_bubble(agent_name, accumulated + "▍", ts, f"R{round_num}", is_right)
                all_bubbles = "\n".join(completed_bubbles + [current_bubble])
                progress = _build_debate_progress(round_num, idx, len(STAGE2_AGENTS), f"{agent_name.upper()}")
                feed_html = _build_feed_html(
                    all_bubbles, progress,
                    status_color="#D4AF37",
                    status_text=f"ROUND {round_num} — {agent_name.upper()}"
                )
                yield (status, feed_html, _build_metrics_html(), _build_verdict_top_html(), "")

            # Finalize debate message directly without artificial truncation
            final_text = accumulated.strip()
            debate_transcript.append({
                "agent": agent_name,
                "round": f"Round {round_num}",
                "text": final_text,
            })
            finished_bubble = _build_debate_bubble(agent_name, final_text, ts, f"R{round_num}", is_right)
            completed_bubbles.append(finished_bubble)

            # Determine next status
            is_last_agent = idx == len(STAGE2_AGENTS) - 1
            is_last_round = round_num == 2
            if is_last_agent and is_last_round:
                next_label = "DEBATE COMPLETE"
                next_color = "#10b981"
            elif is_last_agent:
                next_label = "ROUND 2 STARTING"
                next_color = "#D4AF37"
            else:
                next_label = f"NEXT: {STAGE2_AGENTS[idx + 1].upper()}"
                next_color = "#D4AF37"

            all_bubbles = "\n".join(completed_bubbles)
            progress = _build_debate_progress(round_num, idx + 1, len(STAGE2_AGENTS), next_label)
            feed_html = _build_feed_html(
                all_bubbles, progress,
                status_color=next_color,
                status_text=next_label,
            )

            if is_last_agent and is_last_round:
                done_status = "✓  Debate complete — all rounds finished"
            elif is_last_agent:
                done_status = f"✓  Round {round_num} complete — starting Round {round_num + 1}"
            else:
                done_status = f"✓  {agent_name} (R{round_num}) done"
            yield (done_status, feed_html, _build_metrics_html(), _build_verdict_top_html(), "")

    # STAGE 4 — Final verdict engine
    engine = VerdictEngine(
        user_decision=decision_text,
        analyses=agent_results,
        transcript=debate_transcript,
        revisions={}
    )

    verdict_prompt = engine.build_synthesis_prompt()
    accumulated_verdict = ""
    for chunk in generate_stream(verdict_prompt, VERDICT_SYSTEM_PROMPT, use_pro=True):
        accumulated_verdict += chunk
        yield (
            "◈  Synthesizing final verdict (Pro)...",
            feed_html,
            _build_metrics_html(),
            _build_verdict_top_html(),
            accumulated_verdict + "▍"
        )
    
    yield (
        "◈  Calculating decision metrics...",
        feed_html,
        _build_metrics_html(),
        _build_verdict_top_html(),
        accumulated_verdict
    )

    scores_dict = engine.generate_scores(generate)
    confidence = scores_dict.get("confidence", 85)
    risk = scores_dict.get("risk", 50)
    growth = scores_dict.get("growth", 50)

    yield (
        "✓  Verdict complete",
        feed_html,
        _build_metrics_html(confidence, risk, growth),
        _build_verdict_top_html(confidence),
        accumulated_verdict
    )



# UI 


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="VerdictAI X | Decision Intelligence", css=CSS) as app:

    
        gr.HTML(NAVBAR_HTML)

      
        with gr.Column(elem_id="home-view"):
            # Hero Section 
            gr.HTML(HERO_HTML)

            #  Dashboard: 3-column layout 
            with gr.Row(elem_id="dashboard-row"):

                #  LEFT: Input Panel 
                with gr.Column(scale=1, min_width=280, elem_id="input-col"):
                    gr.HTML(INPUT_HEADER_HTML)

                    decision_input = gr.Textbox(
                        label="Decision",
                        placeholder="Should I join a startup at 8 LPA or prepare for GATE for one year?",
                        lines=10,
                        max_lines=16,
                        elem_id="decision-input",
                    )

                    status_bar = gr.Textbox(
                        value="◯  Waiting for input…",
                        label="Status",
                        interactive=False,
                        elem_id="vai-status",
                        show_label=False,
                        lines=1,
                        max_lines=1,
                    )

                    submit_btn = gr.Button(
                        "✦ Run Analysis",
                        variant="primary",
                        elem_id="btn-submit",
                    )

                #  CENTER: Live Debate Feed 
                with gr.Column(scale=2, min_width=400, elem_id="debate-col"):
                    debate_feed = gr.HTML(
                        value=_build_idle_feed(),
                        elem_id="debate-feed-container",
                    )

                #  RIGHT: Metrics 
                with gr.Column(scale=1, min_width=240, elem_id="metrics-col"):
                    metrics_html_cmp = gr.HTML(_build_metrics_html())

            #  Verdict Card (full width) 
            with gr.Row(elem_id="verdict-row"):
                with gr.Column(elem_id="verdict-col"):
                    verdict_top_cmp = gr.HTML(_build_verdict_top_html())
                    verdict_markdown_cmp = gr.Markdown(
                        value="*The AI council's final recommendation will appear here after the debate concludes.*",
                        elem_id="verdict-markdown"
                    )

            gr.HTML(FOOTER_HTML)

        #  About view
        with gr.Column(elem_id="about-view", visible=True):
            gr.HTML(ABOUT_HTML)
            gr.HTML(FOOTER_HTML)

        gr.HTML("<style>#about-view { display: none; flex-direction: column; }</style>")

   
        submit_btn.click(
            fn=handle_submit,
            inputs=[decision_input],
            outputs=[status_bar, debate_feed, metrics_html_cmp, verdict_top_cmp, verdict_markdown_cmp],
        )

    return app



if __name__ == "__main__":
    app = build_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )
