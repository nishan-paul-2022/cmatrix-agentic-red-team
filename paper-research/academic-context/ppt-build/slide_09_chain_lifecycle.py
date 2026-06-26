"""
Slide 9 — Attack Chain Lifecycle
Visual showing HYPOTHESIZED → PARTIALLY_VALIDATED → VALIDATED / RULED_OUT
with the Validation Agent self-debugging loop.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
import pptx.enum.shapes

BG_DARK     = RGBColor(0x0A, 0x0D, 0x1A)
ACCENT_CYAN = RGBColor(0x00, 0xE5, 0xFF)
ACCENT_LIME = RGBColor(0x39, 0xFF, 0x14)
ACCENT_GOLD = RGBColor(0xFF, 0xD7, 0x00)
ACCENT_RED  = RGBColor(0xFF, 0x45, 0x45)
ACCENT_PURP = RGBColor(0xBD, 0x93, 0xF9)
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

def arrow_h(slide, x1, y, x2, color=GREY_MID, lw=2.0):
    c = slide.shapes.add_connector(pptx.enum.shapes.MSO_CONNECTOR.STRAIGHT, x1, y, x2, y)
    c.line.color.rgb = color; c.line.width = Pt(lw)
    ln = c.line._ln
    he = etree.SubElement(ln, qn('a:headEnd'))
    he.set('type', 'arrow'); he.set('w', 'med'); he.set('len', 'med')
    etree.SubElement(ln, qn('a:tailEnd')).set('type', 'none')
    return c

def arrow_v(slide, x, y1, y2, color=GREY_MID, lw=1.5):
    c = slide.shapes.add_connector(pptx.enum.shapes.MSO_CONNECTOR.STRAIGHT, x, y1, x, y2)
    c.line.color.rgb = color; c.line.width = Pt(lw)
    ln = c.line._ln
    he = etree.SubElement(ln, qn('a:headEnd'))
    he.set('type', 'arrow'); he.set('w', 'med'); he.set('len', 'med')
    etree.SubElement(ln, qn('a:tailEnd')).set('type', 'none')
    return c

prs = Presentation(PPTX_PATH)
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

# ── Chrome ─────────────────────────────────────────────────────────────────────
box(slide, Inches(0), Inches(0), Inches(0.06), SLIDE_H, fill=ACCENT_GOLD)
box(slide, Inches(0.06), Inches(0), SLIDE_W-Inches(0.06), Inches(0.04), fill=ACCENT_GOLD)
box(slide, Inches(0.06), SLIDE_H-Inches(0.04), SLIDE_W-Inches(0.06), Inches(0.04), fill=ACCENT_GOLD)

txt(slide, "ATTACK CHAIN LIFECYCLE", Inches(0.3), Inches(0.08), Inches(8), Inches(0.3),
    size=11, bold=True, color=ACCENT_GOLD)
txt(slide, "From Hypothesis to Validated Exploit — APG Chain State Machine",
    Inches(0.3), Inches(0.38), Inches(12), Inches(0.62), size=28, bold=True, color=WHITE)
box(slide, Inches(0.3), Inches(1.0), Inches(6), Inches(0.03), fill=ACCENT_GOLD)

# ══════════════════════════════════════════════
#  TOP: LINEAR STATE MACHINE
# ══════════════════════════════════════════════
sm_top = Inches(1.12)
states = [
    ("HYPOTHESIZED",         RGBColor(0x50,0x40,0x00), ACCENT_GOLD,
     "Commander has inferred\na possible chain from\nASG Vulnerability nodes.\nNot yet tested."),
    ("PARTIALLY\nVALIDATED", RGBColor(0x30,0x40,0x10), ACCENT_LIME,
     "One or more ChainSteps\nconfirmed. Chain not\ncomplete end-to-end."),
    ("VALIDATED",            RGBColor(0x08,0x30,0x10), ACCENT_LIME,
     "All ChainSteps confirmed\nwith Evidence. Impact\ndemonstrated. Mission\nsuccess."),
    ("RULED_OUT",            RGBColor(0x30,0x08,0x08), ACCENT_RED,
     "A required ChainStep\nfailed after retry cap.\nChain is not exploitable\nas hypothesized."),
]
state_w = Inches(2.55)
state_h = Inches(2.2)
state_gap = Inches(0.25)
state_l_start = Inches(0.3)
arrow_y = sm_top + state_h / 2 + Inches(0.1)

for i, (label, bg, clr, desc) in enumerate(states):
    l = state_l_start + i * (state_w + state_gap)
    box(slide, l, sm_top, state_w, state_h, fill=bg, line_color=clr, lw=2.0)
    txt(slide, label, l+Inches(0.12), sm_top+Inches(0.1),
        state_w-Inches(0.2), Inches(0.5), size=13, bold=True, color=clr, align=PP_ALIGN.CENTER)
    box(slide, l+Inches(0.15), sm_top+Inches(0.62), state_w-Inches(0.3), Inches(0.03), fill=clr)
    txt(slide, desc, l+Inches(0.12), sm_top+Inches(0.72),
        state_w-Inches(0.2), Inches(1.4), size=10, color=GREY_MID,
        align=PP_ALIGN.CENTER, wrap=True)
    # Arrow to next state (except last)
    if i < len(states) - 1:
        clr_arrow = clr if i < 2 else ACCENT_RED
        x1_a = l + state_w
        x2_a = l + state_w + state_gap
        arrow_h(slide, x1_a, arrow_y, x2_a, clr_arrow)

# Branch label for VALIDATED vs RULED_OUT
txt(slide, "Chain succeeds",
    state_l_start + 2*(state_w+state_gap) + state_w/2 - Inches(0.6),
    sm_top + state_h/2 - Inches(0.7), Inches(1.2), Inches(0.28),
    size=8.5, italic=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)
txt(slide, "Step fails\nafter cap",
    state_l_start + 2*(state_w+state_gap) + state_w + state_gap - Inches(0.05),
    sm_top + state_h/2 + Inches(0.2), Inches(1.0), Inches(0.4),
    size=8.5, italic=True, color=ACCENT_RED, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════
#  BOTTOM LEFT: SELF-DEBUGGING LOOP
# ══════════════════════════════════════════════
loop_l = Inches(0.3)
loop_t = Inches(3.55)
loop_w = Inches(5.8)
loop_h = Inches(3.48)
box(slide, loop_l, loop_t, loop_w, loop_h,
    fill=RGBColor(0x08,0x0E,0x20), line_color=ACCENT_RED, lw=1.5)
txt(slide, "🎯  Validation Agent — Self-Debugging Loop",
    loop_l+Inches(0.15), loop_t+Inches(0.08), loop_w-Inches(0.25), Inches(0.3),
    size=13, bold=True, color=ACCENT_RED)
box(slide, loop_l+Inches(0.15), loop_t+Inches(0.42), loop_w-Inches(0.3), Inches(0.025), fill=ACCENT_RED)

steps_loop = [
    ("1. Diagnose",     "Analyze why the attempt failed:\nwrong param · auth required · version mismatch · encoding issue",  ACCENT_GOLD),
    ("2. Contextualize","Query the ASG for additional node attributes\nthat may resolve the diagnosis",                        ACCENT_CYAN),
    ("3. Adapt",        "Modify tool invocation based on diagnosis + context.\nRetry with corrected approach.",                ACCENT_LIME),
    ("4. Cap",          "After configurable max retries (default: 3),\nmark ChainStep RULED_OUT · write failure to ASG",       ACCENT_RED),
]
for i, (step, desc, clr) in enumerate(steps_loop):
    t = loop_t + Inches(0.55) + i * Inches(0.7)
    box(slide, loop_l+Inches(0.15), t, loop_w-Inches(0.3), Inches(0.65),
        fill=RGBColor(0x10,0x14,0x28), line_color=clr, lw=0.8)
    txt(slide, step, loop_l+Inches(0.25), t+Inches(0.06),
        Inches(1.5), Inches(0.25), size=11, bold=True, color=clr)
    txt(slide, desc, loop_l+Inches(1.8), t+Inches(0.06),
        loop_w-Inches(2.0), Inches(0.5), size=9.5, color=GREY_MID, wrap=True)
    if i < 3:
        arrow_v(slide, loop_l + loop_w/2, t+Inches(0.65), t+Inches(0.7), color=clr, lw=1.2)

# ══════════════════════════════════════════════
#  BOTTOM RIGHT: RISK SCORING + PRIORITY
# ══════════════════════════════════════════════
rs_l = Inches(6.35)
rs_t = Inches(3.55)
rs_w = Inches(6.75)
rs_h = Inches(1.55)
box(slide, rs_l, rs_t, rs_w, rs_h,
    fill=RGBColor(0x12,0x0E,0x04), line_color=ACCENT_GOLD, lw=1.5)
txt(slide, "Risk Scoring Formula",
    rs_l+Inches(0.15), rs_t+Inches(0.08), rs_w-Inches(0.25), Inches(0.3),
    size=13, bold=True, color=ACCENT_GOLD)
txt(slide,
    "risk_score  =  CVSS Severity  ×  Exploitability  ×  Impact Classification\n\n"
    "Priority = risk_score rank across all HYPOTHESIZED + PARTIALLY_VALIDATED chains\n"
    "Commander pursues highest-priority chain first — re-ranks after every status change.",
    rs_l+Inches(0.15), rs_t+Inches(0.42), rs_w-Inches(0.25), Inches(1.05),
    size=10.5, color=GREY_MID, wrap=True)

# Chain example in shopvault
ex_l = Inches(6.35)
ex_t = Inches(5.22)
ex_w = Inches(6.75)
ex_h = Inches(1.8)
box(slide, ex_l, ex_t, ex_w, ex_h,
    fill=RGBColor(0x08,0x14,0x20), line_color=ACCENT_CYAN, lw=1.2)
txt(slide, "shopvault.io — APG Chain Priorities",
    ex_l+Inches(0.15), ex_t+Inches(0.08), ex_w-Inches(0.25), Inches(0.28),
    size=12, bold=True, color=ACCENT_CYAN)
chains_ex = [
    ("Chain-01", "CVE-2022-21661 SQL injection → RCE",             "8.8", ACCENT_RED),
    ("Chain-03", "Blind SQLi on staging → credential extraction",  "8.1", ACCENT_GOLD),
    ("Chain-02", "IDOR on /api/v1/orders → customer data",         "7.5", ACCENT_GOLD),
    ("Chain-04", "Direct DB backup download → full PII",           "trivial", ACCENT_PURP),
]
for i, (cid, desc, score, clr) in enumerate(chains_ex):
    t = ex_t + Inches(0.4) + i * Inches(0.34)
    txt(slide, f"{i+1}.  {cid}  —  {desc}",
        ex_l+Inches(0.2), t, ex_w-Inches(1.5), Inches(0.3),
        size=9.5, color=GREY_MID)
    txt(slide, f"risk: {score}",
        ex_l+ex_w-Inches(1.3), t, Inches(1.2), Inches(0.3),
        size=9.5, bold=True, color=clr, align=PP_ALIGN.RIGHT)

txt(slide, "09", SLIDE_W-Inches(0.4), SLIDE_H-Inches(0.55),
    Inches(0.35), Inches(0.45), size=13, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.RIGHT)

prs.save(PPTX_PATH)
print("✅  Slide 9 added.")
