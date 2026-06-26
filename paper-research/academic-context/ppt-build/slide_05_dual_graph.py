"""
Slide 5 — Dual-Graph World Model (Deep Dive Visual Diagram)
Shows ASG node/edge types and APG node/edge types side-by-side
with the separation principle highlighted.
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

def arrow(slide, x1, y1, x2, y2, color=GREY_MID, lw=1.2):
    c = slide.shapes.add_connector(
        pptx.enum.shapes.MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    c.line.color.rgb = color; c.line.width = Pt(lw)
    ln = c.line._ln
    he = etree.SubElement(ln, qn('a:headEnd'))
    he.set('type', 'arrow'); he.set('w', 'med'); he.set('len', 'med')
    te = etree.SubElement(ln, qn('a:tailEnd'))
    te.set('type', 'none')
    return c

prs = Presentation(PPTX_PATH)
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

# ── Chrome ────────────────────────────────────────────────────────────────────
box(slide, Inches(0), Inches(0), Inches(0.06), SLIDE_H, fill=ACCENT_LIME)
box(slide, Inches(0.06), Inches(0), SLIDE_W-Inches(0.06), Inches(0.04), fill=ACCENT_LIME)
box(slide, Inches(0.06), SLIDE_H-Inches(0.04), SLIDE_W-Inches(0.06), Inches(0.04), fill=ACCENT_LIME)

txt(slide, "DUAL-GRAPH WORLD MODEL", Inches(0.3), Inches(0.08), Inches(8), Inches(0.3),
    size=11, bold=True, color=ACCENT_LIME)
txt(slide, "The Architectural Core — Two Knowledge Layers, One World",
    Inches(0.3), Inches(0.38), Inches(12), Inches(0.62),
    size=30, bold=True, color=WHITE)
box(slide, Inches(0.3), Inches(1.0), Inches(5), Inches(0.03), fill=ACCENT_LIME)

# ── Central separator label ────────────────────────────────────────────────────
sep_l = Inches(6.32)
box(slide, sep_l, Inches(1.1), Inches(0.7), Inches(5.6), fill=RGBColor(0x0D,0x12,0x22), line_color=GREY_MID, lw=0.5)
txt(slide, "STRICT\nSEPARATION", sep_l+Inches(0.04), Inches(2.2), Inches(0.65), Inches(1.0),
    size=9, bold=True, italic=False, color=GREY_MID, align=PP_ALIGN.CENTER)
txt(slide, "No agent\ncrosses\nthis boundary", sep_l+Inches(0.04), Inches(3.3), Inches(0.65), Inches(0.85),
    size=8, bold=False, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════
# LEFT — ASG
# ═══════════════════════════════════════════════
asg_l = Inches(0.3)
asg_col_w = Inches(5.85)

# Header
box(slide, asg_l, Inches(1.1), asg_col_w, Inches(0.52),
    fill=RGBColor(0x04,0x1C,0x0E), line_color=ACCENT_LIME, lw=2.0)
txt(slide, "🕸️  ATTACK SURFACE GRAPH  (ASG)", asg_l+Inches(0.15), Inches(1.14),
    asg_col_w-Inches(0.25), Inches(0.45), size=15, bold=True, color=ACCENT_LIME)

# Question banner
box(slide, asg_l, Inches(1.65), asg_col_w, Inches(0.38),
    fill=RGBColor(0x08,0x28,0x14), line_color=ACCENT_LIME, lw=0.8)
txt(slide, "What does the target look like?  (Discovered Reality)",
    asg_l+Inches(0.15), Inches(1.68), asg_col_w-Inches(0.25), Inches(0.32),
    size=12, bold=False, italic=True, color=ACCENT_LIME)

# Node types section
box(slide, asg_l, Inches(2.1), asg_col_w, Inches(0.28),
    fill=RGBColor(0x10,0x30,0x18))
txt(slide, "NODE TYPES", asg_l+Inches(0.15), Inches(2.12), asg_col_w, Inches(0.24),
    size=10, bold=True, color=ACCENT_LIME)

node_types = [
    ("Domain",        "Root domain + discovered subdomains"),
    ("Host",          "IP address, OS fingerprint, liveness"),
    ("Port",          "Open port with protocol"),
    ("Service",       "Service name, version, banner"),
    ("Technology",    "Framework, CMS, server software, version"),
    ("Endpoint",      "Web or API route"),
    ("Parameter",     "Request param, header, or input field"),
    ("Vulnerability", "CVE / misconfiguration — enriched with live intel"),
    ("Evidence",      "Screenshot, capture, exploitation artifact"),
]
node_h = Inches(0.3)
node_t_start = Inches(2.42)
for i, (ntype, desc) in enumerate(node_types):
    t = node_t_start + i * (node_h + Inches(0.03))
    bg = RGBColor(0x06,0x20,0x10) if i % 2 == 0 else CARD_BG
    box(slide, asg_l, t, asg_col_w, node_h, fill=bg)
    txt(slide, ntype, asg_l+Inches(0.12), t+Inches(0.04), Inches(1.35), node_h-Inches(0.06),
        size=10, bold=True, color=ACCENT_LIME)
    txt(slide, desc, asg_l+Inches(1.5), t+Inches(0.04), asg_col_w-Inches(1.6), node_h-Inches(0.06),
        size=9.5, color=GREY_MID)

# Edge types
edge_t_start = node_t_start + len(node_types) * (node_h + Inches(0.03)) + Inches(0.08)
box(slide, asg_l, edge_t_start, asg_col_w, Inches(0.26),
    fill=RGBColor(0x10,0x30,0x18))
txt(slide, "EDGE TYPES", asg_l+Inches(0.15), edge_t_start+Inches(0.03), asg_col_w, Inches(0.22),
    size=10, bold=True, color=ACCENT_LIME)
edges_asg = "has_host  ·  has_port  ·  runs  ·  uses  ·  has_endpoint  ·  has_parameter  ·  affected_by  ·  validated_by"
txt(slide, edges_asg, asg_l+Inches(0.12), edge_t_start+Inches(0.3),
    asg_col_w-Inches(0.2), Inches(0.35), size=9, italic=True, color=GREY_MID)

# ═══════════════════════════════════════════════
# RIGHT — APG
# ═══════════════════════════════════════════════
apg_l = Inches(7.18)
apg_col_w = Inches(5.88)

# Header
box(slide, apg_l, Inches(1.1), apg_col_w, Inches(0.52),
    fill=RGBColor(0x20,0x12,0x04), line_color=ACCENT_GOLD, lw=2.0)
txt(slide, "🛣️  ATTACK PATH GRAPH  (APG)", apg_l+Inches(0.15), Inches(1.14),
    apg_col_w-Inches(0.25), Inches(0.45), size=15, bold=True, color=ACCENT_GOLD)

# Question banner
box(slide, apg_l, Inches(1.65), apg_col_w, Inches(0.38),
    fill=RGBColor(0x28,0x18,0x04), line_color=ACCENT_GOLD, lw=0.8)
txt(slide, "What can be done to it?  (Inferred Attack Opportunity)",
    apg_l+Inches(0.15), Inches(1.68), apg_col_w-Inches(0.25), Inches(0.32),
    size=12, bold=False, italic=True, color=ACCENT_GOLD)

# Node types
box(slide, apg_l, Inches(2.1), apg_col_w, Inches(0.28),
    fill=RGBColor(0x30,0x18,0x08))
txt(slide, "NODE TYPES", apg_l+Inches(0.15), Inches(2.12), apg_col_w, Inches(0.24),
    size=10, bold=True, color=ACCENT_GOLD)

apg_nodes = [
    ("AttackChain",  "Ordered exploitation sequence from entry → impact"),
    ("ChainStep",    "Single action on a specific ASG node"),
    ("Impact",       "Business / technical consequence at chain end"),
]
for i, (ntype, desc) in enumerate(apg_nodes):
    t = Inches(2.42) + i * Inches(0.34)
    bg = RGBColor(0x28,0x18,0x06) if i % 2 == 0 else CARD_BG
    box(slide, apg_l, t, apg_col_w, Inches(0.32), fill=bg)
    txt(slide, ntype, apg_l+Inches(0.12), t+Inches(0.04), Inches(1.5), Inches(0.26),
        size=10, bold=True, color=ACCENT_GOLD)
    txt(slide, desc, apg_l+Inches(1.65), t+Inches(0.04), apg_col_w-Inches(1.75), Inches(0.26),
        size=9.5, color=GREY_MID)

# AttackChain properties box
ac_t = Inches(3.48)
box(slide, apg_l, ac_t, apg_col_w, Inches(1.05),
    fill=RGBColor(0x18,0x10,0x02), line_color=ACCENT_GOLD, lw=0.8)
txt(slide, "Each AttackChain carries:", apg_l+Inches(0.15), ac_t+Inches(0.05),
    apg_col_w-Inches(0.25), Inches(0.25), size=10, bold=True, color=ACCENT_GOLD)
ac_props = [
    "risk_score  — CVSS severity + exploitability + impact class",
    "validation_status  — HYPOTHESIZED → PARTIALLY_VALIDATED → VALIDATED / RULED_OUT",
    "priority  — Commander-assigned chain pursuit order",
]
for i, prop in enumerate(ac_props):
    txt(slide, f"• {prop}", apg_l+Inches(0.2), ac_t+Inches(0.3)+i*Inches(0.23),
        apg_col_w-Inches(0.3), Inches(0.23), size=9.5, color=GREY_MID)

# Edge types
edge_apg_t = Inches(4.6)
box(slide, apg_l, edge_apg_t, apg_col_w, Inches(0.28),
    fill=RGBColor(0x30,0x18,0x08))
txt(slide, "EDGE TYPES", apg_l+Inches(0.15), edge_apg_t+Inches(0.03), apg_col_w, Inches(0.24),
    size=10, bold=True, color=ACCENT_GOLD)
txt(slide, "starts_at  ·  next_step  ·  achieves  ·  supported_by",
    apg_l+Inches(0.12), edge_apg_t+Inches(0.32), apg_col_w-Inches(0.2), Inches(0.3),
    size=9.5, italic=True, color=GREY_MID)

# Write-ownership table
own_t = Inches(5.05)
box(slide, apg_l, own_t, apg_col_w, Inches(0.28),
    fill=RGBColor(0x30,0x18,0x08))
txt(slide, "WRITE OWNERSHIP (Separation Principle)",
    apg_l+Inches(0.15), own_t+Inches(0.03), apg_col_w, Inches(0.24),
    size=10, bold=True, color=ACCENT_GOLD)
rows_own = [
    ("Discovery Agents", "Write → ASG only",  "Never reason about chains"),
    ("Commander Agent",  "Write → APG only",  "Never runs tools"),
]
for i, (agent, writes, note) in enumerate(rows_own):
    t2 = own_t + Inches(0.32) + i * Inches(0.38)
    bg = RGBColor(0x18,0x10,0x02) if i % 2 == 0 else CARD_BG
    box(slide, apg_l, t2, apg_col_w, Inches(0.36), fill=bg)
    txt(slide, agent, apg_l+Inches(0.12), t2+Inches(0.05), Inches(1.6), Inches(0.28), size=9.5, bold=True, color=WHITE)
    txt(slide, writes, apg_l+Inches(1.75), t2+Inches(0.05), Inches(1.8), Inches(0.28), size=9.5, bold=True, color=ACCENT_GOLD)
    txt(slide, note, apg_l+Inches(3.6), t2+Inches(0.05), Inches(2.1), Inches(0.28), size=8.5, italic=True, color=GREY_MID)

# ── Bottom principle bar ───────────────────────────────────────────────────────
box(slide, Inches(0.3), Inches(6.12), SLIDE_W-Inches(0.6), Inches(0.72),
    fill=RGBColor(0x06,0x14,0x20), line_color=ACCENT_CYAN, lw=1.5)
txt(slide,
    "No agent conflates facts with hypotheses  ·  The ASG never contains hypotheses  ·  "
    "The APG never contains raw scan data  ·  This dual-layer separation is the property "
    "no prior VAPT system implements.",
    Inches(0.55), Inches(6.2), SLIDE_W-Inches(1.0), Inches(0.58),
    size=12, bold=False, italic=True, color=ACCENT_CYAN, wrap=True)

txt(slide, "05", SLIDE_W-Inches(0.4), SLIDE_H-Inches(0.55),
    Inches(0.35), Inches(0.45), size=13, bold=True, color=ACCENT_LIME, align=PP_ALIGN.RIGHT)

prs.save(PPTX_PATH)
print("✅  Slide 5 added.")
