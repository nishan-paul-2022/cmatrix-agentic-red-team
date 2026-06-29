"""
Slide 13 — APG Chain State Machine + Validation Agent Self-Debugging Loop
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_GOLD)

    # ── Header ────────────────────────────────────────────────────────────────
    txt(slide, "ATTACK CHAIN LIFECYCLE",
        Inches(0.3), Inches(0.07), Inches(6.0), Inches(0.27),
        size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
    txt(slide, "APG Chain State Machine + Validation Agent Self-Debugging Loop",
        Inches(0.3), Inches(0.31), Inches(12.0), Inches(0.51),
        size=24, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # ═══════════════════════════════════════════════════════
    # STATE MACHINE — top row of 4 state boxes
    # ═══════════════════════════════════════════════════════
    STATE_TOP = Inches(0.88)
    STATE_H = Inches(1.95)
    STATE_W = Inches(2.55)
    HEADER_H = Inches(0.30)

    # State 1: HYPOTHESIZED
    box(slide, Inches(0.25), STATE_TOP, STATE_W, STATE_H,
        fill=RGBColor(0x50, 0x40, 0x00), line_color=ACCENT_GOLD, lw=2.0)
    box(slide, Inches(0.25), STATE_TOP, STATE_W, HEADER_H, fill=ACCENT_GOLD)
    txt(slide, "HYPOTHESIZED",
        Inches(0.25), STATE_TOP + Inches(0.04), STATE_W, Inches(0.26),
        size=9.5, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    txt(slide, "Commander inferred a possible chain from ASG Vulnerability nodes. Not yet tested.",
        Inches(0.35), STATE_TOP + HEADER_H + Inches(0.06), Inches(2.37), Inches(0.88),
        size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # State 2: PARTIALLY VALIDATED
    box(slide, Inches(3.06), STATE_TOP, STATE_W, STATE_H,
        fill=RGBColor(0x28, 0x40, 0x08), line_color=ACCENT_LIME, lw=2.0)
    box(slide, Inches(3.06), STATE_TOP, STATE_W, HEADER_H, fill=ACCENT_LIME)
    txt(slide, "PARTIALLY VALIDATED",
        Inches(3.06), STATE_TOP + Inches(0.04), STATE_W, Inches(0.26),
        size=9.5, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    txt(slide, "One or more ChainSteps confirmed. Chain not complete end-to-end. Validation in progress.",
        Inches(3.16), STATE_TOP + HEADER_H + Inches(0.06), Inches(2.37), Inches(0.88),
        size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # State 3: VALIDATED
    box(slide, Inches(7.682), STATE_TOP, STATE_W, STATE_H,
        fill=RGBColor(0x06, 0x28, 0x0E), line_color=ACCENT_LIME, lw=2.0)
    box(slide, Inches(7.682), STATE_TOP, STATE_W, HEADER_H, fill=ACCENT_LIME)
    txt(slide, "VALIDATED",
        Inches(7.682), STATE_TOP + Inches(0.04), STATE_W, Inches(0.26),
        size=9.5, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    txt(slide, "All ChainSteps confirmed with linked Evidence. Impact demonstrated. Mission success for this chain.",
        Inches(7.782), STATE_TOP + HEADER_H + Inches(0.06), Inches(2.37), Inches(0.88),
        size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # State 4: RULED_OUT
    box(slide, Inches(10.453), STATE_TOP, STATE_W, STATE_H,
        fill=RGBColor(0x28, 0x08, 0x08), line_color=ACCENT_RED, lw=2.0)
    box(slide, Inches(10.453), STATE_TOP + Inches(0.01), STATE_W, HEADER_H, fill=ACCENT_RED)
    txt(slide, "RULED_OUT",
        Inches(10.82), STATE_TOP + Inches(0.00), Inches(1.70), Inches(0.26),
        size=9.5, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)
    txt(slide, "A required ChainStep failed after max retries. Chain not exploitable as hypothesized. Commander re-plans.",
        Inches(10.543), STATE_TOP + HEADER_H + Inches(0.06), Inches(2.37), Inches(0.88),
        size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Arrows between states (horizontal flow)
    # HYPO -> PARTIAL (middle arrow at midpoint between boxes)
    arr(slide, Inches(2.80), Inches(1.855), Inches(3.06), Inches(1.855),
        color=ACCENT_GOLD, lw=1.2)
    # diamond / transfer node between PARTIAL and VALIDATED
    box(slide, Inches(5.51), Inches(1.675), Inches(0.36), Inches(0.36),
        fill=ACCENT_GOLD, line_color=GREY_MID, lw=0.8)
    arr(slide, Inches(5.87), Inches(1.855), Inches(7.682), Inches(1.855),
        color=ACCENT_LIME, lw=1.2)
    txt(slide, "chain succeeds",
        Inches(6.046), Inches(1.526), Inches(1.20), Inches(0.24),
        size=8.0, italic=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
    # PARTIAL -> RULED_OUT (diagonal arrow down to ruled_out)
    txt(slide, "step fails after cap",
        Inches(8.568), Inches(3.035), Inches(1.35), Inches(0.24),
        size=8.0, italic=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)

    # ═══════════════════════════════════════════════════════
    # LEFT PANEL — Validation Agent Self-Debugging Loop
    # ═══════════════════════════════════════════════════════
    LOOP_TOP = Inches(3.97)
    LOOP_H = Inches(1.92)
    LOOP_W = Inches(7.80)

    box(slide, Inches(0.232), LOOP_TOP, LOOP_W, LOOP_H,
        fill=RGBColor(0x08, 0x0C, 0x1E), line_color=ACCENT_RED, lw=1.4)
    box(slide, Inches(0.232), LOOP_TOP, LOOP_W, Inches(0.28), fill=ACCENT_RED)
    txt(slide, "🎯  Validation Agent — Self-Debugging Loop  (on ChainStep failure)",
        Inches(0.232), LOOP_TOP + Inches(0.04), LOOP_W, Inches(0.25),
        size=9.0, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    STEP_TOP = LOOP_TOP + Inches(0.35)
    STEP_H = Inches(1.50)

    # Steps in the loop
    steps = [
        ("ATTEMPT",      ACCENT_GOLD, Inches(0.382), Inches(1.563), ["Execute tool", "against target"]),
        ("DIAGNOSE",     ACCENT_GOLD, Inches(2.024), Inches(1.563), ["Analyze failure:", "wrong param · auth", "version mismatch"]),
        ("CONTEXTUALIZE", ACCENT_CYAN, Inches(3.667), Inches(1.563), ["Query ASG for", "additional node", "attributes"]),
        ("ADAPT",        ACCENT_LIME, Inches(5.309), Inches(1.563), ["Modify tool call", "based on diagnosis", "+ context"]),
    ]

    for step_name, step_color, step_l, step_w, body_lines in steps:
        box(slide, step_l, STEP_TOP, step_w, STEP_H,
            fill=RGBColor(0x10, 0x14, 0x28), line_color=step_color, lw=1.0)
        box(slide, step_l, STEP_TOP, step_w, Inches(0.24), fill=step_color)
        txt(slide, step_name,
            step_l, STEP_TOP + Inches(0.04), step_w, Inches(0.24),
            size=8.0, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
        for bi, line in enumerate(body_lines):
            txt(slide, line,
                step_l + Inches(0.06), STEP_TOP + Inches(0.30) + bi * Inches(0.24),
                step_w - Inches(0.08), Inches(0.22),
                size=8.0, color=GREY_MID, align=PP_ALIGN.LEFT)

    # CAP box
    CAP_L = Inches(6.952)
    box(slide, CAP_L, STEP_TOP, Inches(0.93), STEP_H,
        fill=RGBColor(0x22, 0x08, 0x08), line_color=ACCENT_RED, lw=1.4)
    box(slide, CAP_L, STEP_TOP, Inches(0.93), Inches(0.24), fill=ACCENT_RED)
    txt(slide, "CAP  (×3 max)",
        CAP_L, STEP_TOP + Inches(0.04), Inches(0.93), Inches(0.24),
        size=8.0, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    txt(slide, "→ Mark ChainStep\n   RULED_OUT\n→ Write failure\n   to ASG node",
        CAP_L + Inches(0.06), STEP_TOP + Inches(0.30), Inches(0.83), Inches(1.18),
        size=8.0, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Retry label
    txt(slide, "retry (up to cap)",
        Inches(1.944), LOOP_TOP + LOOP_H + Inches(0.02), Inches(2.50), Inches(0.23),
        size=7.5, italic=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # ═══════════════════════════════════════════════════════
    # RIGHT PANEL — Risk Score + Chain Priority
    # ═══════════════════════════════════════════════════════
    RS_L = Inches(8.132)
    RS_TOP = Inches(3.97)
    RS_W = Inches(5.053)
    RS_H = Inches(3.243)

    box(slide, RS_L, RS_TOP, RS_W, RS_H,
        fill=RGBColor(0x0E, 0x0C, 0x04), line_color=ACCENT_GOLD, lw=1.4)
    box(slide, RS_L, RS_TOP, RS_W, Inches(0.28), fill=ACCENT_GOLD)
    txt(slide, "Risk Score + Chain Priority",
        RS_L, RS_TOP + Inches(0.04), RS_W, Inches(0.25),
        size=9.0, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    # Formula
    txt(slide, "risk_score = CVSS × Exploitability × Impact",
        RS_L + Inches(0.10), RS_TOP + Inches(0.34), Inches(4.87), Inches(0.27),
        size=10.0, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
    txt(slide, "Priority = rank across all HYPOTHESIZED + PARTIALLY_VALIDATED chains. Commander pursues highest-priority chain first — re-ranks on every status change.",
        RS_L + Inches(0.10), RS_TOP + Inches(0.64), Inches(4.87), Inches(0.39),
        size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Example table header
    box(slide, RS_L + Inches(0.10), RS_TOP + Inches(1.22), Inches(4.87), Inches(0.26),
        fill=RGBColor(0x22, 0x18, 0x04))
    txt(slide, "shopvault.io  —  APG Chain Priority Order",
        RS_L + Inches(0.14), RS_TOP + Inches(1.25), Inches(4.80), Inches(0.24),
        size=8.5, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    # Table rows
    chain_rows = [
        ("1", "Chain-01  —  CVE-2022-21661 SQLi → RCE",           "9.1", ACCENT_RED,  RGBColor(0x18, 0x12, 0x02), ACCENT_RED),
        ("2", "Chain-03  —  Blind SQLi on staging → DB creds",     "8.1", ACCENT_GOLD, RGBColor(0x12, 0x0C, 0x02), ACCENT_GOLD),
        ("3", "Chain-02  —  IDOR on /api/v1/orders → PII",         "7.5", ACCENT_GOLD, RGBColor(0x18, 0x12, 0x02), ACCENT_GOLD),
        ("4", "Chain-04  —  Direct DB backup download → PII",      "N/A", ACCENT_PURP, RGBColor(0x12, 0x0C, 0x02), ACCENT_GOLD),
    ]
    row_h = Inches(0.38)
    for ri, (num, chain_txt, score, num_color, row_fill, row_line) in enumerate(chain_rows):
        row_top = RS_TOP + Inches(1.52) + ri * Inches(0.40)
        box(slide, RS_L + Inches(0.10), row_top, Inches(4.87), row_h,
            fill=row_fill, line_color=row_line, lw=0.8)
        txt(slide, num,
            RS_L + Inches(0.14), row_top + Inches(0.06), Inches(0.22), Inches(0.25),
            size=9.0, bold=True, color=num_color, align=PP_ALIGN.LEFT)
        txt(slide, chain_txt,
            RS_L + Inches(0.38), row_top + Inches(0.07), Inches(4.30), Inches(0.24),
            size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT)
        txt(slide, score,
            RS_L + Inches(4.50), row_top + Inches(0.05), Inches(0.42), Inches(0.26),
            size=9.5, bold=True, color=num_color, align=PP_ALIGN.RIGHT)

    slide_number(slide, "13", ACCENT_GOLD)
