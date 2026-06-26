"""
Slide 6 — The 6 AI Agents (Roles + Tools + Key Behaviors)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BG_DARK     = RGBColor(0x0A, 0x0D, 0x1A)
ACCENT_CYAN = RGBColor(0x00, 0xE5, 0xFF)
ACCENT_LIME = RGBColor(0x39, 0xFF, 0x14)
ACCENT_GOLD = RGBColor(0xFF, 0xD7, 0x00)
ACCENT_RED  = RGBColor(0xFF, 0x45, 0x45)
ACCENT_PURP = RGBColor(0xBD, 0x93, 0xF9)
ACCENT_TEAL = RGBColor(0x00, 0xBF, 0xD8)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
GREY_MID    = RGBColor(0xA0, 0xAA, 0xB8)
CARD_BG     = RGBColor(0x10, 0x16, 0x2B)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
PPTX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CMatrix_Presentation.pptx")

def set_bg(slide, color):
    fill = slide.background.fill; fill.solid(); fill.fore_color.rgb = color

def box(slide, l, t, w, h, fill=None, line_color=None, lw=1.0):
    shp = slide.shapes.add_shape(1, l, t, w, h)
    if fill: shp.fill.solid(); shp.fill.fore_color.rgb = fill
    else: shp.fill.background()
    if line_color: shp.line.color.rgb = line_color; shp.line.width = Pt(lw)
    else: shp.line.fill.background()
    shp.shadow.inherit = False
    return shp

def txt(slide, text, l, t, w, h, size=11, bold=False, italic=False,
        color=WHITE, align=PP_ALIGN.LEFT, wrap=True):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.name = "Calibri"; run.font.size = Pt(size)
    run.font.bold = bold; run.font.italic = italic; run.font.color.rgb = color
    return tb

def multiline(slide, lines, l, t, w, h):
    """lines: list of (text, size, bold, color)"""
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    for i, (text, size, bold, color) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run(); run.text = text
        run.font.name = "Calibri"; run.font.size = Pt(size)
        run.font.bold = bold; run.font.color.rgb = color

prs = Presentation(PPTX_PATH)
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

# ── Chrome ─────────────────────────────────────────────────────────────────────
box(slide, Inches(0), Inches(0), Inches(0.06), SLIDE_H, fill=ACCENT_PURP)
box(slide, Inches(0.06), Inches(0), SLIDE_W-Inches(0.06), Inches(0.04), fill=ACCENT_PURP)
box(slide, Inches(0.06), SLIDE_H-Inches(0.04), SLIDE_W-Inches(0.06), Inches(0.04), fill=ACCENT_PURP)

txt(slide, "AGENT ARCHITECTURE", Inches(0.3), Inches(0.08), Inches(8), Inches(0.3),
    size=11, bold=True, color=ACCENT_PURP)
txt(slide, "The 6 Specialized AI Agents — Roles, Tools, Behaviors",
    Inches(0.3), Inches(0.38), Inches(12), Inches(0.62), size=30, bold=True, color=WHITE)
box(slide, Inches(0.3), Inches(1.0), Inches(5), Inches(0.03), fill=ACCENT_PURP)

# ── Agent definitions ─────────────────────────────────────────────────────────
# Each: (emoji+name, accent_color, phase_tag, role_1line, tools_str, key_behavior)
agents_def = [
    (
        "👑  Commander Agent",
        ACCENT_CYAN,
        "ORCHESTRATION",
        "Reads the dual graph. Plans. Delegates. Never runs tools.",
        "No tools — reasons over ASG + APG",
        "The only agent that writes to the APG. Approves High-risk ops via mailbox. "
        "Governs the Observe → Reason → Plan → Execute loop.",
    ),
    (
        "🕵️  Recon Agent",
        ACCENT_LIME,
        "PHASE 1",
        "External reconnaissance and host discovery.",
        "Amass  ·  httpx  ·  Nmap",
        "Discovers subdomains, validates live hosts, identifies open ports and services. "
        "Writes Domain, Host, Port, Service nodes to ASG.",
    ),
    (
        "🔬  Analysis Agent",
        ACCENT_TEAL,
        "PHASE 2",
        "Deep enumeration and vulnerability discovery.",
        "WhatWeb  ·  Gobuster  ·  ffuf  ·  Nuclei  ·  OWASP ZAP",
        "Fingerprints technologies, discovers hidden resources, finds API routes/params, "
        "runs automated vuln checks. Writes Technology, Endpoint, Parameter, Vulnerability nodes.",
    ),
    (
        "🔍  Research Agent",
        ACCENT_GOLD,
        "INTELLIGENCE",
        "Live vulnerability intelligence grounding.",
        "NVD API  ·  Exploit-DB  ·  GitHub  ·  Vendor Advisories",
        "The ONLY agent authorized for outbound internet requests. Closes the stale-knowledge gap "
        "by enriching ASG Vulnerability nodes with real-time CVE data, CVSS scores, and PoC status.",
    ),
    (
        "🎯  Validation Agent",
        ACCENT_RED,
        "PHASE 3",
        "Proves that discovered vulnerabilities are real and exploitable.",
        "SQLMap  ·  Metasploit",
        "Executes controlled exploitation to validate each APG ChainStep. "
        "Self-debugging loop: Diagnose → Contextualize → Adapt → Retry (cap: 3). "
        "Advances ChainStep status to VALIDATED or RULED_OUT.",
    ),
    (
        "📸  Evidence Agent",
        ACCENT_PURP,
        "PHASE 3",
        "Captures proof artifacts for every validated finding.",
        "EyeWitness",
        "Screenshots exposed panels, API responses, exploitation results. "
        "Links all Evidence nodes to corresponding ASG nodes via validated_by edges — "
        "every finding is traceable to its proof.",
    ),
]

# Layout: 2 rows × 3 columns
card_w = Inches(4.1)
card_h = Inches(2.55)
gap_x  = Inches(0.12)
gap_y  = Inches(0.12)
start_l = Inches(0.3)
start_t = Inches(1.1)

for idx, (name, clr, phase, role, tools, behavior) in enumerate(agents_def):
    col = idx % 3
    row = idx // 3
    l = start_l + col * (card_w + gap_x)
    t = start_t + row * (card_h + gap_y)

    # Card body
    box(slide, l, t, card_w, card_h, fill=CARD_BG, line_color=clr, lw=1.5)
    # Phase tag (top-right pill)
    tag_w = Inches(1.1)
    box(slide, l + card_w - tag_w, t, tag_w, Inches(0.3),
        fill=clr)
    txt(slide, phase, l + card_w - tag_w + Inches(0.04), t + Inches(0.03),
        tag_w - Inches(0.06), Inches(0.24), size=8, bold=True,
        color=BG_DARK, align=PP_ALIGN.CENTER)
    # Agent name
    txt(slide, name, l+Inches(0.12), t+Inches(0.08), card_w-tag_w-Inches(0.18),
        Inches(0.34), size=13, bold=True, color=clr)
    # Divider
    box(slide, l+Inches(0.12), t+Inches(0.46), card_w-Inches(0.24), Inches(0.025), fill=clr)
    # Role line
    txt(slide, role, l+Inches(0.12), t+Inches(0.5), card_w-Inches(0.2), Inches(0.32),
        size=10, bold=False, italic=True, color=WHITE)
    # Tools badge
    box(slide, l+Inches(0.12), t+Inches(0.86), card_w-Inches(0.24), Inches(0.32),
        fill=RGBColor(0x08,0x10,0x20), line_color=clr, lw=0.6)
    txt(slide, tools, l+Inches(0.2), t+Inches(0.89), card_w-Inches(0.36), Inches(0.26),
        size=9, bold=True, color=clr)
    # Key behavior
    txt(slide, behavior, l+Inches(0.12), t+Inches(1.25), card_w-Inches(0.2), Inches(1.22),
        size=9.5, bold=False, color=GREY_MID, wrap=True)

# ── Context isolation note ─────────────────────────────────────────────────────
box(slide, Inches(0.3), Inches(7.0), SLIDE_W-Inches(0.6), Inches(0.38),
    fill=RGBColor(0x0E,0x14,0x28), line_color=ACCENT_PURP, lw=1.0)
txt(slide,
    "Context-Isolated Spawning:  Each agent receives only the ASG/APG slice it needs + its authorized toolset. "
    "Working context discarded on return.  Agents cannot contaminate each other's reasoning.",
    Inches(0.55), Inches(7.04), SLIDE_W-Inches(0.9), Inches(0.32),
    size=10, bold=False, color=ACCENT_PURP, wrap=False)

txt(slide, "06", SLIDE_W-Inches(0.4), SLIDE_H-Inches(0.55),
    Inches(0.35), Inches(0.45), size=13, bold=True, color=ACCENT_PURP, align=PP_ALIGN.RIGHT)

prs.save(PPTX_PATH)
print("✅  Slide 6 added.")
