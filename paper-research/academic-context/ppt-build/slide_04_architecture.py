"""
Slide 4 — System Architecture (Live Visual Diagram)
Draws the full Commander + Agents + Dual-Graph + Tool Layer architecture
using native python-pptx shapes, connectors, and text — no images.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

BG_DARK      = RGBColor(0x0A, 0x0D, 0x1A)
ACCENT_CYAN  = RGBColor(0x00, 0xE5, 0xFF)
ACCENT_LIME  = RGBColor(0x39, 0xFF, 0x14)
ACCENT_GOLD  = RGBColor(0xFF, 0xD7, 0x00)
ACCENT_RED   = RGBColor(0xFF, 0x45, 0x45)
ACCENT_PURP  = RGBColor(0xBD, 0x93, 0xF9)
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
GREY_MID     = RGBColor(0xA0, 0xAA, 0xB8)
CARD_BG      = RGBColor(0x10, 0x16, 0x2B)
CARD_AGENT   = RGBColor(0x0D, 0x1E, 0x2E)
CARD_GRAPH   = RGBColor(0x08, 0x1C, 0x12)
CARD_TOOL    = RGBColor(0x1A, 0x12, 0x28)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
PPTX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CMatrix_Presentation.pptx")

def set_bg(slide, color):
    fill = slide.background.fill; fill.solid(); fill.fore_color.rgb = color

def box(slide, l, t, w, h, fill=None, line_color=None, lw=1.0, radius=False):
    shp = slide.shapes.add_shape(1, l, t, w, h)   # 1=RECTANGLE
    if fill: shp.fill.solid(); shp.fill.fore_color.rgb = fill
    else: shp.fill.background()
    if line_color: shp.line.color.rgb = line_color; shp.line.width = Pt(lw)
    else: shp.line.fill.background()
    shp.shadow.inherit = False
    return shp

def txt(slide, text, l, t, w, h, size=11, bold=False, italic=False,
        color=WHITE, align=PP_ALIGN.CENTER, wrap=True, font="Calibri"):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.name = font; run.font.size = Pt(size)
    run.font.bold = bold; run.font.italic = italic; run.font.color.rgb = color
    return tb

def arrow(slide, x1, y1, x2, y2, color=GREY_MID, lw=1.2):
    """Draw a connector line with an arrowhead."""
    from pptx.util import Emu
    connector = slide.shapes.add_connector(
        pptx.enum.shapes.MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    connector.line.color.rgb = color
    connector.line.width = Pt(lw)
    # Add arrowhead via XML
    ln = connector.line._ln
    tailEnd = etree.SubElement(ln, qn('a:tailEnd'))
    tailEnd.set('type', 'none')
    headEnd = etree.SubElement(ln, qn('a:headEnd'))
    headEnd.set('type', 'arrow')
    headEnd.set('w', 'med')
    headEnd.set('len', 'med')
    return connector

import pptx.enum.shapes

prs = Presentation(PPTX_PATH)
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)
set_bg(slide, BG_DARK)

# ── Chrome bars ───────────────────────────────────────────────────────────────
box(slide, Inches(0), Inches(0), Inches(0.06), SLIDE_H, fill=ACCENT_CYAN)
box(slide, Inches(0.06), Inches(0), SLIDE_W-Inches(0.06), Inches(0.04), fill=ACCENT_CYAN)
box(slide, Inches(0.06), SLIDE_H-Inches(0.04), SLIDE_W-Inches(0.06), Inches(0.04), fill=ACCENT_CYAN)

# ── Slide label + title ───────────────────────────────────────────────────────
txt(slide, "SYSTEM ARCHITECTURE", Inches(0.3), Inches(0.08), Inches(8), Inches(0.3),
    size=11, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
txt(slide, "How CMatrix Works — Full Architecture",
    Inches(0.3), Inches(0.38), Inches(10), Inches(0.62),
    size=30, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
box(slide, Inches(0.3), Inches(1.0), Inches(5), Inches(0.035), fill=ACCENT_CYAN)

# ══════════════════════════════════════════════════════════════════
#  LAYOUT:
#  Left side (0.15 → 4.5):  OPERATOR → COMMANDER + VAPT PROTOCOL
#  Centre (4.6 → 8.8):       DUAL GRAPH (ASG on top, APG below)
#  Right side (9.0 → 13.0): AGENTS column (6 agents)
#  Bottom strip:             TOOL ADAPTER LAYER + 11 TOOLS
# ══════════════════════════════════════════════════════════════════

# ── OPERATOR block ─────────────────────────────────────────────────────────────
op_l, op_t, op_w, op_h = Inches(0.18), Inches(1.12), Inches(2.4), Inches(0.72)
box(slide, op_l, op_t, op_w, op_h, fill=RGBColor(0x0E,0x1A,0x2E), line_color=GREY_MID, lw=0.8)
txt(slide, "👤  OPERATOR", op_l, op_t+Inches(0.04), op_w, Inches(0.32),
    size=12, bold=True, color=GREY_MID, align=PP_ALIGN.CENTER)
txt(slide, "Defines target · scope · mode",
    op_l, op_t+Inches(0.36), op_w, Inches(0.3),
    size=9, color=GREY_MID, align=PP_ALIGN.CENTER)

# ── COMMANDER block ────────────────────────────────────────────────────────────
cmd_l, cmd_t = Inches(0.18), Inches(2.1)
cmd_w, cmd_h = Inches(2.4), Inches(1.55)
box(slide, cmd_l, cmd_t, cmd_w, cmd_h, fill=RGBColor(0x08,0x18,0x2C), line_color=ACCENT_CYAN, lw=2.0)
txt(slide, "👑  COMMANDER AGENT", cmd_l, cmd_t+Inches(0.07), cmd_w, Inches(0.3),
    size=12, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.CENTER)
box(slide, cmd_l+Inches(0.12), cmd_t+Inches(0.4), cmd_w-Inches(0.24), Inches(0.03), fill=ACCENT_CYAN)
details = [
    "Reads dual graph",
    "Plans & delegates",
    "Approves high-risk ops",
    "Writes to APG only",
]
for i, d in enumerate(details):
    txt(slide, f"• {d}", cmd_l+Inches(0.15), cmd_t+Inches(0.5)+i*Inches(0.24),
        cmd_w-Inches(0.25), Inches(0.24), size=9.5, color=GREY_MID, align=PP_ALIGN.LEFT)

# ── VAPT PROTOCOL block ────────────────────────────────────────────────────────
vp_l, vp_t = Inches(0.18), Inches(3.85)
vp_w, vp_h = Inches(2.4), Inches(1.05)
box(slide, vp_l, vp_t, vp_w, vp_h, fill=RGBColor(0x10,0x10,0x1C), line_color=ACCENT_PURP, lw=1.0)
txt(slide, "📜  VAPT PROTOCOL", vp_l, vp_t+Inches(0.06), vp_w, Inches(0.28),
    size=11, bold=True, color=ACCENT_PURP, align=PP_ALIGN.CENTER)
txt(slide, "Phase rules · Re-plan triggers\nTermination conditions\nMethodology-as-config",
    vp_l+Inches(0.1), vp_t+Inches(0.36), vp_w-Inches(0.15), Inches(0.65),
    size=9, color=GREY_MID, align=PP_ALIGN.LEFT)

# Arrows: Operator → Commander
arrow(slide, op_l+op_w/2, op_t+op_h, op_l+op_w/2, cmd_t, color=ACCENT_CYAN, lw=1.5)
# Commander ↔ VAPT Protocol
arrow(slide, cmd_l+cmd_w/2, cmd_t+cmd_h, cmd_l+cmd_w/2, vp_t, color=ACCENT_PURP, lw=1.2)

# ── DUAL GRAPH zone ────────────────────────────────────────────────────────────
dg_l = Inches(2.88)

# ASG box
asg_l, asg_t = dg_l, Inches(1.12)
asg_w, asg_h = Inches(3.55), Inches(2.4)
box(slide, asg_l, asg_t, asg_w, asg_h, fill=RGBColor(0x04,0x18,0x0E), line_color=ACCENT_LIME, lw=2.0)
txt(slide, "🕸️  ATTACK SURFACE GRAPH  (ASG)",
    asg_l, asg_t+Inches(0.06), asg_w, Inches(0.3),
    size=11, bold=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)
box(slide, asg_l+Inches(0.15), asg_t+Inches(0.4), asg_w-Inches(0.3), Inches(0.025), fill=ACCENT_LIME)
asg_nodes = ["Domain · Host · Port · Service", "Technology · Endpoint · Parameter",
             "Vulnerability · Evidence"]
for i, n in enumerate(asg_nodes):
    txt(slide, n, asg_l+Inches(0.15), asg_t+Inches(0.5)+i*Inches(0.24),
        asg_w-Inches(0.25), Inches(0.24), size=9.5, color=WHITE, align=PP_ALIGN.CENTER)
box(slide, asg_l+Inches(0.15), asg_t+Inches(1.25), asg_w-Inches(0.3), Inches(0.025), fill=RGBColor(0x30,0x60,0x40))
txt(slide, "Discovered Reality — confirmed facts only",
    asg_l+Inches(0.15), asg_t+Inches(1.33), asg_w-Inches(0.25), Inches(0.28),
    size=9, italic=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)
txt(slide, "has_host · has_port · runs · uses\nhas_endpoint · has_parameter\naffected_by · validated_by",
    asg_l+Inches(0.15), asg_t+Inches(1.65), asg_w-Inches(0.25), Inches(0.68),
    size=8.5, color=GREY_MID, align=PP_ALIGN.CENTER)

# APG box
apg_l, apg_t = dg_l, Inches(3.7)
apg_w, apg_h = Inches(3.55), Inches(2.1)
box(slide, apg_l, apg_t, apg_w, apg_h, fill=RGBColor(0x18,0x0C,0x04), line_color=ACCENT_GOLD, lw=2.0)
txt(slide, "🛣️  ATTACK PATH GRAPH  (APG)",
    apg_l, apg_t+Inches(0.06), apg_w, Inches(0.3),
    size=11, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.CENTER)
box(slide, apg_l+Inches(0.15), apg_t+Inches(0.4), apg_w-Inches(0.3), Inches(0.025), fill=ACCENT_GOLD)
txt(slide, "AttackChain · ChainStep · Impact",
    apg_l+Inches(0.15), apg_t+Inches(0.5), apg_w-Inches(0.25), Inches(0.28),
    size=9.5, color=WHITE, align=PP_ALIGN.CENTER)
txt(slide, "risk_score · priority · validation_status",
    apg_l+Inches(0.15), apg_t+Inches(0.78), apg_w-Inches(0.25), Inches(0.25),
    size=9, color=GREY_MID, align=PP_ALIGN.CENTER)
box(slide, apg_l+Inches(0.15), apg_t+Inches(1.05), apg_w-Inches(0.3), Inches(0.025), fill=RGBColor(0x60,0x40,0x10))
txt(slide, "Inferred Opportunity — attack reasoning only",
    apg_l+Inches(0.15), apg_t+Inches(1.12), apg_w-Inches(0.25), Inches(0.28),
    size=9, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.CENTER)
txt(slide, "HYPOTHESIZED → PARTIALLY_VALIDATED\n→ VALIDATED / RULED_OUT",
    apg_l+Inches(0.15), apg_t+Inches(1.45), apg_w-Inches(0.25), Inches(0.55),
    size=9, color=GREY_MID, align=PP_ALIGN.CENTER)

# ASG → APG arrow (Commander derives chains)
arrow(slide, asg_l+asg_w/2, asg_t+asg_h, apg_l+apg_w/2, apg_t, color=ACCENT_GOLD, lw=1.8)
txt(slide, "Commander derives chains", asg_l+asg_w/2+Inches(0.08), asg_t+asg_h+Inches(0.02),
    Inches(1.5), Inches(0.24), size=8, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

# Commander → ASG arrow
arrow(slide, cmd_l+cmd_w, cmd_t+Inches(0.5), asg_l, asg_t+Inches(0.5), color=ACCENT_CYAN, lw=1.5)
# APG → Commander (feedback)
arrow(slide, apg_l, apg_t+Inches(0.6), cmd_l+cmd_w, cmd_t+Inches(1.1), color=ACCENT_GOLD, lw=1.2)

# ── AGENTS column ──────────────────────────────────────────────────────────────
ag_l = Inches(6.7)
agents = [
    ("🕵️  Recon Agent",    "Amass · httpx · Nmap",             ACCENT_LIME),
    ("🔬  Analysis Agent", "WhatWeb · Gobuster · ffuf\nNuclei · OWASP ZAP", ACCENT_CYAN),
    ("🔍  Research Agent", "NVD · Exploit-DB · GitHub",         ACCENT_GOLD),
    ("🎯  Validation Agt", "SQLMap · Metasploit",               ACCENT_RED),
    ("📸  Evidence Agent", "EyeWitness",                        ACCENT_PURP),
    ("📝  Report Agent",   "Reads full ASG + APG",              GREY_MID),
]
ag_w, ag_h = Inches(2.35), Inches(0.88)
ag_gap     = Inches(0.08)
ag_start_t = Inches(1.12)

for i, (name, tools, clr) in enumerate(agents):
    t = ag_start_t + i * (ag_h + ag_gap)
    box(slide, ag_l, t, ag_w, ag_h, fill=CARD_AGENT, line_color=clr, lw=1.0)
    txt(slide, name, ag_l+Inches(0.1), t+Inches(0.06), ag_w-Inches(0.15), Inches(0.3),
        size=10.5, bold=True, color=clr, align=PP_ALIGN.LEFT)
    txt(slide, tools, ag_l+Inches(0.1), t+Inches(0.4), ag_w-Inches(0.15), Inches(0.43),
        size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT)
    # Arrow from Commander to each agent
    arrow(slide, cmd_l+cmd_w, cmd_t+Inches(0.5), ag_l, t+ag_h/2, color=clr, lw=0.8)
    # Arrow from agent back to ASG
    if name != "📝  Report Agent":
        arrow(slide, ag_l, t+ag_h/2, asg_l+asg_w, asg_t+asg_h/2, color=RGBColor(0x30,0x50,0x30), lw=0.6)

# ── TOOL ADAPTER LAYER strip ───────────────────────────────────────────────────
tool_strip_t = Inches(6.18)
tool_strip_h = Inches(0.55)
box(slide, Inches(0.18), tool_strip_t, SLIDE_W-Inches(0.36), tool_strip_h,
    fill=RGBColor(0x08,0x0C,0x1E), line_color=ACCENT_PURP, lw=1.2)

txt(slide, "🔌  TOOL ADAPTER LAYER  ·  Risk Gate: Low → execute · Medium → LLM Classifier · High → Commander Mailbox",
    Inches(0.35), tool_strip_t+Inches(0.04), SLIDE_W-Inches(0.6), Inches(0.45),
    size=9.5, bold=False, color=ACCENT_PURP, align=PP_ALIGN.LEFT)

# ── 11 TOOL badges ────────────────────────────────────────────────────────────
tools_list = ["Amass","httpx","Nmap","WhatWeb","Gobuster","ffuf","Nuclei","OWASP ZAP","SQLMap","Metasploit","EyeWitness"]
tool_colors = [ACCENT_LIME,ACCENT_LIME,ACCENT_LIME,ACCENT_CYAN,ACCENT_CYAN,ACCENT_CYAN,ACCENT_CYAN,ACCENT_CYAN,ACCENT_RED,ACCENT_RED,ACCENT_PURP]
tbadge_w = Inches(1.12)
tbadge_h = Inches(0.35)
tbadge_t = Inches(6.84)
tbadge_gap = Inches(0.065)
tbadge_start_l = Inches(0.18)
for i, (tool, clr) in enumerate(zip(tools_list, tool_colors)):
    l = tbadge_start_l + i * (tbadge_w + tbadge_gap)
    box(slide, l, tbadge_t, tbadge_w, tbadge_h, fill=CARD_TOOL, line_color=clr, lw=0.7)
    txt(slide, tool, l+Inches(0.04), tbadge_t+Inches(0.04), tbadge_w-Inches(0.06), tbadge_h-Inches(0.07),
        size=8.5, bold=True, color=clr, align=PP_ALIGN.CENTER)

# ── Slide number ──────────────────────────────────────────────────────────────
txt(slide, "04", SLIDE_W-Inches(0.4), SLIDE_H-Inches(0.55),
    Inches(0.35), Inches(0.45), size=13, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.RIGHT)

prs.save(PPTX_PATH)
print("✅  Slide 4 added.")
