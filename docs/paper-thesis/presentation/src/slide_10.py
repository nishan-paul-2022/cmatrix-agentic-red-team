"""
Slide 10 — Tool Risk Gate
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_PURP)

    slide_header(slide, "TOOL ADAPTER LAYER",
                 "Tool Risk Gate \u2014 Every Tool Call\u2019s Journey",
                 ACCENT_PURP, title_size=28)
    txt(slide, "No tool executes without passing this gate  \u00b7  No irreversible operation runs without Commander-level scope validation",
        Inches(0.3), Inches(0.9), Inches(12.5), Inches(0.26),
        size=10, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)
    slide_number(slide, "10", ACCENT_PURP)

    # ── LEFT: Flowchart ───────────────────────────────────────────────────────
    FL = Inches(0.3)
    FW = Inches(8.4)
    FT = Inches(1.22)
    FH = SLIDE_H - FT - Inches(0.15)

    box(slide, FL, FT, FW, FH, fill=RGBColor(0x04, 0x06, 0x12), line_color=GREY_DARK, lw=0.7)

    def flow_node(slide, label, x, y, w, h, fill, text_color=WHITE, size=9):
        box(slide, x, y, w, h, fill=fill, line_color=GREY_MID, lw=0.7)
        txt(slide, label, x, y + Inches(0.06), w, h - Inches(0.1),
            size=size, bold=True, color=text_color, align=PP_ALIGN.CENTER, wrap=True)

    def flow_lbl(slide, label, x, y, color=GREY_MID):
        txt(slide, label, x, y, Inches(1.4), Inches(0.22), size=8, color=color, align=PP_ALIGN.LEFT)

    CX = FL + Inches(2.6)
    NW = Inches(2.6)
    NH = Inches(0.42)

    # Main flow nodes
    n1_t = FT + Inches(0.14)
    flow_node(slide, "\U0001f916 Agent requests tool call\nTool: Gobuster \u00b7 Target: shopvault.io",
              CX - Inches(NW/2 - 0.0), n1_t, NW, Inches(0.52), RGBColor(0x10, 0x20, 0x38))

    n2_t = n1_t + Inches(0.68)
    flow_node(slide, "\U0001f9ff PreToolUse Hook fires\nCONTINUE / BLOCK / MODIFY",
              CX - Inches(NW/2 - 0.0), n2_t, NW, Inches(0.48), RGBColor(0x20, 0x10, 0x30),
              text_color=ACCENT_PURP)

    n3_t = n2_t + Inches(0.62)
    flow_node(slide, "\U0001f50d Scope Check\nTarget in scope? Tool authorized?",
              CX - Inches(NW/2 - 0.0), n3_t, NW, Inches(0.48), RGBColor(0x10, 0x18, 0x10),
              text_color=GREY_MID)

    n4_t = n3_t + Inches(0.62)
    flow_node(slide, "\U0001f534 Risk Classification\nLOW \u00b7 MED \u00b7 HIGH",
              CX - Inches(NW/2 - 0.0), n4_t, NW, Inches(0.42), ACCENT_RED, BG_DARK, size=10)

    # Arrows between main nodes
    for nt in [n1_t + Inches(0.52), n2_t + Inches(0.48), n3_t + Inches(0.48)]:
        arr(slide, CX, nt, CX, nt + Inches(0.12), color=GREY_MID, lw=1.0)

    # LOW branch (left)
    LOW_X = FL + Inches(0.55)
    flow_lbl(slide, "LOW", LOW_X - Inches(0.05), n4_t + Inches(0.22), ACCENT_LIME)
    arr(slide, CX - Inches(NW/2), n4_t + Inches(0.21), LOW_X + Inches(1.3), n4_t + Inches(0.21),
        color=ACCENT_LIME, lw=1.0)
    ln5_t = n4_t + Inches(0.62)
    flow_node(slide, "\u2705 Execute immediately\nScope check only",
              LOW_X, ln5_t, Inches(1.5), Inches(0.48), RGBColor(0x06, 0x20, 0x06),
              text_color=ACCENT_LIME, size=8.5)

    # MED branch (center)
    flow_lbl(slide, "MED", CX - Inches(0.2), n4_t + Inches(0.46), ACCENT_GOLD)
    mn5_t = n4_t + Inches(0.62)
    flow_node(slide, "\U0001f534 LLM Classifier\nFast filter \u2192 CoT pass",
              CX - Inches(NW/2 - 0.0), mn5_t, NW, Inches(0.48), RGBColor(0x28, 0x18, 0x00),
              text_color=ACCENT_GOLD)
    arr(slide, CX, n4_t + Inches(0.42), CX, mn5_t, color=GREY_MID, lw=1.0)

    # EXECUTE / ESCALATE after MED
    mn6_t = mn5_t + Inches(0.56)
    txt(slide, "EXECUTE", CX - Inches(NW/2 + 0.02), mn6_t - Inches(0.05), Inches(1.0), Inches(0.22),
        size=8, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
    txt(slide, "ESCALATE", CX + Inches(0.45), mn6_t - Inches(0.05), Inches(1.1), Inches(0.22),
        size=8, color=ACCENT_RED, align=PP_ALIGN.LEFT)

    exec_t = mn6_t + Inches(0.22)
    flow_node(slide, "\u2705 Proceed to\nTool Adapter",
              CX - Inches(NW/2 + 0.02), exec_t, Inches(1.5), Inches(0.52),
              RGBColor(0x04, 0x18, 0x04), text_color=ACCENT_LIME, size=8.5)
    flow_node(slide, "\u2b06 Route to\nCommander Mailbox",
              CX + Inches(0.2), exec_t, Inches(1.6), Inches(0.52),
              RGBColor(0x1A, 0x0A, 0x00), text_color=ACCENT_GOLD, size=8.5)

    # HIGH branch
    HIGH_X = FL + FW - Inches(2.8)
    flow_lbl(slide, "HIGH", HIGH_X - Inches(0.1), n4_t + Inches(0.22), ACCENT_RED)
    arr(slide, CX + Inches(NW/2), n4_t + Inches(0.21), HIGH_X, n4_t + Inches(0.21),
        color=ACCENT_RED, lw=1.0)
    hn5_t = n4_t + Inches(0.62)
    flow_node(slide, "\U0001f5a5\ufe0f Commander Mailbox\nHuman-in-the-loop slot",
              HIGH_X, hn5_t, Inches(2.55), Inches(0.48),
              RGBColor(0x28, 0x08, 0x08), text_color=WHITE, size=9)
    arr(slide, CX + Inches(NW/2), n4_t + Inches(0.21), HIGH_X, hn5_t + Inches(0.24),
        color=ACCENT_RED, lw=1.0)

    # APPROVE/REJECT/MODIFY after mailbox
    mbox_out_t = hn5_t + Inches(0.54)
    txt(slide, "\u2705 APPROVE", HIGH_X - Inches(0.05), mbox_out_t, Inches(1.0), Inches(0.22),
        size=7.5, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
    txt(slide, "\u274c REJECT", HIGH_X + Inches(0.9), mbox_out_t, Inches(0.9), Inches(0.22),
        size=7.5, color=ACCENT_RED, align=PP_ALIGN.LEFT)
    txt(slide, "\U0001f4dd MODIFY", HIGH_X + Inches(1.75), mbox_out_t, Inches(0.9), Inches(0.22),
        size=7.5, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    mbox_node_t = mbox_out_t + Inches(0.24)
    flow_node(slide, "Proceed to\nTool Adapter",
              HIGH_X - Inches(0.05), mbox_node_t, Inches(0.95), Inches(0.42),
              RGBColor(0x04, 0x16, 0x04), text_color=ACCENT_LIME, size=8)
    flow_node(slide, "Cancelled\nAnnotated to APG",
              HIGH_X + Inches(0.88), mbox_node_t, Inches(0.88), Inches(0.42),
              RGBColor(0x1A, 0x04, 0x04), text_color=ACCENT_RED, size=7.5)
    flow_node(slide, "Params adjusted\nthen approved",
              HIGH_X + Inches(1.72), mbox_node_t, Inches(0.78), Inches(0.42),
              RGBColor(0x1A, 0x10, 0x00), text_color=ACCENT_GOLD, size=7.5)

    # Tool Adapter executes
    ta_t = exec_t + Inches(0.72)
    flow_node(slide, "\u2699\ufe0f Tool Adapter executes\nRun tool \u2192 parse raw output \u2192 structured JSON\n\u2192 discard raw",
              CX - Inches(NW/2 - 0.0), ta_t, NW, Inches(0.6),
              RGBColor(0x10, 0x06, 0x22), text_color=ACCENT_PURP, size=8.5)
    arr(slide, CX - Inches(NW/2 - 0.75), exec_t + Inches(0.52), CX, ta_t, color=GREY_MID, lw=1.0)

    # PostToolUse hook
    ph_t = ta_t + Inches(0.68)
    flow_node(slide, "\U0001f9ff PostToolUse Hook fires\nlog \u00b7 alert \u00b7 validate \u00b7 block write",
              CX - Inches(NW/2 - 0.0), ph_t, NW, Inches(0.42),
              RGBColor(0x20, 0x10, 0x30), text_color=ACCENT_PURP)
    arr(slide, CX, ta_t + Inches(0.6), CX, ph_t, color=GREY_MID, lw=1.0)

    # Terminal outputs
    out_t = ph_t + Inches(0.50)
    flow_node(slide, "\u25cf Nodes + edges\nwritten to ASG",
              CX - Inches(NW/2 + 0.02), out_t, Inches(1.5), Inches(0.46),
              RGBColor(0x06, 0x20, 0x06), text_color=ACCENT_LIME, size=8)
    txt(slide, "ASG", CX - Inches(NW/2 + 0.06), out_t + Inches(0.48), Inches(0.5), Inches(0.22),
        size=7.5, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
    flow_node(slide, "\U0001f916 Agent receives\ncompact summary only",
              CX + Inches(0.1), out_t, Inches(1.7), Inches(0.46),
              RGBColor(0x04, 0x10, 0x24), text_color=ACCENT_CYAN, size=8)
    txt(slide, "Agent", CX + Inches(0.4), out_t + Inches(0.48), Inches(0.7), Inches(0.22),
        size=7.5, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
    arr(slide, CX - Inches(0.6), ph_t + Inches(0.42), CX - Inches(0.6), out_t, color=GREY_MID, lw=1.0)
    arr(slide, CX + Inches(0.5), ph_t + Inches(0.42), CX + Inches(0.5), out_t, color=GREY_MID, lw=1.0)

    # ── RIGHT PANEL ───────────────────────────────────────────────────────────
    R = Inches(8.85)
    RW = SLIDE_W - R - Inches(0.15)

    box(slide, R, FT, RW, Inches(2.28), fill=RGBColor(0x08, 0x10, 0x20), line_color=GREY_DARK, lw=0.8)
    txt(slide, "\U0001f9e0 LLM Permission Classifier \u2014 Medium-Risk Calls",
        R + Inches(0.12), FT + Inches(0.08), RW - Inches(0.2), Inches(0.26),
        size=10, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)

    # Fast filter
    box(slide, R + Inches(0.1), FT + Inches(0.38), RW - Inches(0.2), Inches(0.44),
        fill=RGBColor(0x06, 0x16, 0x06), line_color=ACCENT_LIME, lw=0.7)
    txt(slide, "Fast Filter (instant)", R + Inches(0.16), FT + Inches(0.42), RW - Inches(0.3), Inches(0.20),
        size=9, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
    txt(slide, "Obviously safe? \u2192 EXECUTE immediately\nObviously risky? \u2192 ESCALATE immediately",
        R + Inches(0.16), FT + Inches(0.6), RW - Inches(0.3), Inches(0.22),
        size=8, color=WHITE, align=PP_ALIGN.LEFT, wrap=True)

    axes = [
        ("Axis 1: SCOPE ALIGNMENT", "Is the target in declared assessment scope?", ACCENT_CYAN),
        ("Axis 2: CHAIN INTENT", "Is this call consistent with the active APG AttackChain?", ACCENT_GOLD),
        ("Axis 3: PARAMETER SAFETY", "Do params exhibit prompt injection patterns or scope drift?", ACCENT_RED),
    ]
    for k, (label, q, color) in enumerate(axes):
        at = FT + Inches(0.92) + k * Inches(0.36)
        box(slide, R + Inches(0.1), at, RW - Inches(0.2), Inches(0.30),
            fill=RGBColor(0x06, 0x08, 0x1A), line_color=GREY_DARK, lw=0.5)
        txt(slide, f"{label}  {q}", R + Inches(0.16), at + Inches(0.04),
            RW - Inches(0.3), Inches(0.22), size=7.5, color=color, align=PP_ALIGN.LEFT, wrap=True)

    # EXECUTE / ESCALATE buttons
    btn_t = FT + Inches(2.0)
    box(slide, R + Inches(0.1), btn_t, (RW - Inches(0.3)) / 2 - Inches(0.06), Inches(0.36),
        fill=RGBColor(0x04, 0x20, 0x04), line_color=ACCENT_LIME, lw=1.0)
    txt(slide, "\u2705 EXECUTE", R + Inches(0.1), btn_t + Inches(0.06),
        (RW - Inches(0.3)) / 2 - Inches(0.06), Inches(0.24), size=10, bold=True,
        color=ACCENT_LIME, align=PP_ALIGN.CENTER)
    btn2_l = R + Inches(0.1) + (RW - Inches(0.3)) / 2
    box(slide, btn2_l, btn_t, (RW - Inches(0.3)) / 2, Inches(0.36),
        fill=RGBColor(0x20, 0x04, 0x04), line_color=ACCENT_RED, lw=1.0)
    txt(slide, "\u2b06 ESCALATE", btn2_l, btn_t + Inches(0.06),
        (RW - Inches(0.3)) / 2, Inches(0.24), size=10, bold=True,
        color=ACCENT_RED, align=PP_ALIGN.CENTER)

    # Tool Risk Tier Summary
    ts_t = FT + Inches(2.5)
    txt(slide, "Tool Risk Tier Summary", R + Inches(0.1), ts_t, RW - Inches(0.2), Inches(0.26),
        size=11, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    tiers = [
        (ACCENT_LIME, "LOW  Scope check only", "Amass \u00b7 httpx \u00b7 WhatWeb \u00b7 EyeWitness"),
        (ACCENT_GOLD, "MED  LLM Classifier \u2192 exec/esc", "Nmap \u00b7 Gobuster \u00b7 ffuf \u00b7 Nuclei \u00b7 ZAP"),
        (ACCENT_RED, "HIGH  Commander Mailbox approval", "SQLMap \u00b7 Metasploit"),
    ]
    for k, (color, label, tools) in enumerate(tiers):
        tt = ts_t + Inches(0.32) + k * Inches(0.82)
        box(slide, R + Inches(0.1), tt, RW - Inches(0.2), Inches(0.76),
            fill=RGBColor(0x06, 0x08, 0x18), line_color=GREY_DARK, lw=0.6)
        box(slide, R + Inches(0.1), tt, Inches(0.22), Inches(0.76), fill=color)
        txt(slide, label, R + Inches(0.38), tt + Inches(0.06), RW - Inches(0.55), Inches(0.26),
            size=9.5, bold=True, color=color, align=PP_ALIGN.LEFT)
        txt(slide, tools, R + Inches(0.38), tt + Inches(0.34), RW - Inches(0.55), Inches(0.36),
            size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # Critical Safety Property
    csp_t = ts_t + Inches(0.32) + 3 * Inches(0.82) + Inches(0.08)
    box(slide, R + Inches(0.1), csp_t, RW - Inches(0.2), Inches(0.74),
        fill=RGBColor(0x10, 0x06, 0x00), line_color=ACCENT_GOLD, lw=0.8)
    txt(slide, "\U0001f512 Critical Safety Property", R + Inches(0.16), csp_t + Inches(0.06),
        RW - Inches(0.3), Inches(0.24), size=9.5, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
    txt(slide, "No irreversible offensive operation executes without Commander-level scope validation. "
        "No Medium-tier call executes without LLM classifier approval.",
        R + Inches(0.16), csp_t + Inches(0.32), RW - Inches(0.3), Inches(0.4),
        size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)
