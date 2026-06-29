"""
Slide 8 — Context-Isolated Agent Spawn Lifecycle (sequence diagram)
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_CYAN)

    slide_header(slide, "AGENT ARCHITECTURE", "Context-Isolated Agent Spawn Lifecycle",
                 ACCENT_CYAN, title_size=30)
    txt(slide, "Every agent is born fresh \u00b7 does exactly one job \u00b7 dies clean \u00b7 leaves only structured graph state behind",
        Inches(0.3), Inches(0.9), Inches(12.5), Inches(0.26),
        size=10, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)
    slide_number(slide, "08", ACCENT_CYAN)

    # ── Sequence Diagram ───────────────────────────────────────────────────────
    DL = Inches(0.3)
    DW = Inches(8.6)
    DT = Inches(1.25)
    DH = Inches(5.95)

    box(slide, DL, DT, DW, DH, fill=RGBColor(0x06, 0x08, 0x14), line_color=GREY_DARK, lw=0.8)

    # Swimlane headers
    lanes = [
        ("Commander", Inches(0.4), ACCENT_GOLD),
        ("Agent", Inches(2.05), ACCENT_CYAN),
        ("Risk Gate", Inches(3.5), ACCENT_RED),
        ("Tool Adapter", Inches(5.1), ACCENT_PURP),
        ("ASG", Inches(7.0), ACCENT_LIME),
    ]
    for name, lx, color in lanes:
        box(slide, lx, DT + Inches(0.06), Inches(1.4), Inches(0.28), fill=color)
        txt(slide, name, lx, DT + Inches(0.08), Inches(1.4), Inches(0.24),
            size=9.5, bold=True, color=BG_DARK if color != ACCENT_PURP else WHITE, align=PP_ALIGN.CENTER)
        # Dotted vertical line
        for seg in range(12):
            box(slide, lx + Inches(0.68), DT + Inches(0.38) + seg * Inches(0.44),
                Inches(0.02), Inches(0.28), fill=GREY_DARK)

    # Sequence steps (simplified)
    steps = [
        # (from_x, to_x, y, label, label_side, label_color, dashed)
        (Inches(1.1), Inches(2.05), DT + Inches(0.58), "spawn(ASG slice + task + toolset)", "top", WHITE, False),
        (Inches(2.75), Inches(3.5), DT + Inches(0.98), "tool_call(WhatWeb) \u2014 LOW risk", "top", WHITE, False),
        (Inches(3.5), Inches(3.5), DT + Inches(1.16), "\u2192 execute immediately", "right", ACCENT_LIME, True),
        (Inches(3.5), Inches(5.1), DT + Inches(1.36), "execute(WhatWeb)", "top", GREY_MID, False),
        (Inches(5.1), Inches(2.75), DT + Inches(1.56), "structured findings [tech: WP 5.9.3]", "top", GREY_MID, True),
        (Inches(2.75), Inches(3.5), DT + Inches(1.96), "tool_call(Gobuster) \u2014 MED risk", "top", WHITE, False),
        (Inches(3.5), Inches(3.5), DT + Inches(2.14), "LLM Classif\u2026 \u2192 EXECUTE", "right", ACCENT_GOLD, True),
        (Inches(3.5), Inches(5.1), DT + Inches(2.34), "execute(Gobuster)", "top", GREY_MID, False),
        (Inches(5.1), Inches(2.75), DT + Inches(2.54), "structured findings [endpoint: /backup/\u2026]", "top", GREY_MID, True),
        (Inches(2.75), Inches(3.5), DT + Inches(2.94), "tool_call(SQLMap) \u2014 HIGH risk", "top", ACCENT_RED, False),
        (Inches(1.12), Inches(1.12), DT + Inches(3.14), "Commander Mailbox \u2014\napproval request", "left", ACCENT_GOLD, True),
        (Inches(1.12), Inches(3.5), DT + Inches(3.74), "APPROVED\n(scope valid, chain intent ok)", "top", ACCENT_LIME, False),
        (Inches(3.5), Inches(5.1), DT + Inches(4.14), "", "top", GREY_MID, False),
        (Inches(5.1), Inches(7.0), DT + Inches(4.54), "write delta [Tech node][Endpoint node][Vuln node]", "top", ACCENT_LIME, False),
        (Inches(2.75), Inches(1.12), DT + Inches(4.94), "return structured ASG delta", "top", GREY_MID, True),
    ]

    for (x1, x2, y, label, side, color, dashed) in steps:
        if dashed:
            for seg in range(6):
                sx = x1 + seg * (x2 - x1) / 6
                box(slide, sx, y, (x2 - x1) / 8, Inches(0.02), fill=color)
        else:
            arr(slide, x1, y, x2, y, color=color, lw=1.0)
        if label:
            ly = y - Inches(0.2)
            mid_x = min(x1, x2)
            lw_txt = abs(x2 - x1) + Inches(0.5)
            txt(slide, label, mid_x, ly, lw_txt, Inches(0.28),
                size=7.5, color=color, align=PP_ALIGN.LEFT, wrap=True)

    # Bottom summary boxes in diagram
    box(slide, DL + Inches(0.05), DT + DH - Inches(0.92), Inches(2.3), Inches(0.84),
        fill=RGBColor(0x06, 0x16, 0x06), line_color=ACCENT_LIME, lw=0.8)
    txt(slide, "Commander reads new Vuln nodes\n\u2192 seeds APG Chain-01",
        DL + Inches(0.1), DT + DH - Inches(0.88), Inches(2.2), Inches(0.76),
        size=8, color=ACCENT_LIME, align=PP_ALIGN.LEFT, wrap=True)
    box(slide, DL + Inches(2.5), DT + DH - Inches(0.92), Inches(3.0), Inches(0.84),
        fill=RGBColor(0x12, 0x08, 0x00), line_color=ACCENT_GOLD, lw=0.8)
    txt(slide, "\U0001f5d1\ufe0f Working context DISCARDED\nRaw tool output \u00b7 history \u00b7 reasoning \u2192 gone",
        DL + Inches(2.6), DT + DH - Inches(0.88), Inches(2.8), Inches(0.76),
        size=8, color=ACCENT_GOLD, align=PP_ALIGN.LEFT, wrap=True)

    # ── RIGHT PANEL ───────────────────────────────────────────────────────────
    R = Inches(9.15)
    RW = SLIDE_W - R - Inches(0.15)

    # Agent Spawn Package
    box(slide, R, DT, RW, Inches(2.26), fill=RGBColor(0x08, 0x10, 0x20), line_color=GREY_DARK, lw=0.8)
    txt(slide, "Agent Spawn Package", R + Inches(0.12), DT + Inches(0.08),
        RW - Inches(0.2), Inches(0.26), size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    package_items = [
        ("\u25cf ASG SLICE  Only nodes relevant to this task \u2014 not the full graph", ACCENT_LIME),
        ("\u25cf APG SLICE  Relevant AttackChains only (Validation tasks)", ACCENT_GOLD),
        ("\u25cf TOOL SET  Authorized tools only \u2014 no others available", ACCENT_RED),
        ("\u25cf TASK SPEC  Commander's current plan item \u2014 exact objective", ACCENT_CYAN),
        ("\u25cf KNOWLEDGE DOCS  Vuln-class expert docs (Analysis + Validation)", ACCENT_PURP),
    ]
    for k, (label, color) in enumerate(package_items):
        pt = DT + Inches(0.38) + k * Inches(0.34)
        box(slide, R + Inches(0.08), pt, RW - Inches(0.16), Inches(0.28),
            fill=RGBColor(0x04, 0x08, 0x1A), line_color=GREY_DARK, lw=0.5)
        txt(slide, label, R + Inches(0.12), pt + Inches(0.03), RW - Inches(0.22), Inches(0.22),
            size=8, color=color, align=PP_ALIGN.LEFT, wrap=True)

    box(slide, R + Inches(0.08), DT + Inches(2.08), RW - Inches(0.16), Inches(0.26),
        fill=RGBColor(0x02, 0x14, 0x04), line_color=ACCENT_LIME, lw=1.0)
    txt(slide, "Returns: Structured ASG Delta (new nodes + edges only)",
        R + Inches(0.12), DT + Inches(0.5) + Inches(1.62), RW - Inches(0.22), Inches(0.22),
        size=8.5, bold=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)

    txt(slide, "Raw tool output \u00b7 conversation history \u00b7 intermediate reasoning \u2192 DISCARDED",
        R + Inches(0.08), DT + Inches(2.38), RW - Inches(0.16), Inches(0.26),
        size=7.5, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)

    # Benefit cards
    benefits = [
        ("\u2611 Commander Stays Clean",
         "Commander only ever sees ASG/APG state \u2014 never thousands of lines of raw tool output. Reasoning context stays surgically focused.",
         ACCENT_CYAN),
        ("\u2611 Agents Can\u2019t Contaminate",
         "Agent A's verbose history never appears in Agent B's context. Knowledge passes only through the ASG. No shared memory. No cross-pollution.",
         ACCENT_PURP),
        ("\u2611 Rejections Don\u2019t Bias Planning",
         "When Commander rejects a High-risk tool call, that rejection never appears in the Commander's own context. Refusals don't accumulate and skew future decisions.",
         ACCENT_RED),
    ]
    for k, (title, body, color) in enumerate(benefits):
        bt = DT + Inches(2.68) + k * Inches(1.1)
        box(slide, R, bt, RW, Inches(1.04), fill=RGBColor(0x04, 0x08, 0x18), line_color=color, lw=0.8)
        txt(slide, title, R + Inches(0.1), bt + Inches(0.06), RW - Inches(0.2), Inches(0.26),
            size=10, bold=True, color=color, align=PP_ALIGN.LEFT)
        txt(slide, body, R + Inches(0.1), bt + Inches(0.34), RW - Inches(0.2), Inches(0.62),
            size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Result callout
    rt = DT + Inches(2.68) + 3 * Inches(1.1) + Inches(0.04)
    box(slide, R, rt, RW, Inches(0.5), fill=RGBColor(0x0A, 0x18, 0x0A), line_color=ACCENT_LIME, lw=0.8)
    txt(slide, "\U0001f534 Result: Long missions with many agents produce the same reasoning quality as "
        "single-agent tasks \u2014 context quality does not degrade with mission complexity.",
        R + Inches(0.1), rt + Inches(0.06), RW - Inches(0.2), Inches(0.4),
        size=8, color=ACCENT_LIME, align=PP_ALIGN.LEFT, wrap=True)
