"""
Slide 2 — The Problem CMatrix Solves
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_RED)
    slide_header(slide, "THE PROBLEM", "What Existing VAPT Systems Get Wrong",
                 ACCENT_RED, title_size=34)

    CARD_RED = RGBColor(0x2A, 0x10, 0x10)

    problems = [
        ("No Structured World Model",
         "Systems reason from flat conversation history or task queues — no graph of what the target actually is."),
        ("No Attack Path Reasoning",
         "Finished tasks are logged, not understood. Systems cannot represent which vulnerabilities chain together or why."),
        ("Fragile Re-Planning",
         "Dynamic re-planning is ad-hoc. There is no formal trigger grounded in discovered evidence."),
        ("Arbitrary Termination",
         "Missions end on time-limits or empty queues — not because the attack surface and all chains are truly exhausted."),
    ]

    card_l, card_w = Inches(0.3), Inches(5.8)
    card_h, card_gap = Inches(1.25), Inches(0.1)
    card_top = Inches(1.32)

    for i, (title, body) in enumerate(problems):
        top = card_top + i * (card_h + card_gap)
        box(slide, card_l, top, card_w, card_h, fill=CARD_RED, line_color=ACCENT_RED, lw=1.0)
        txt(slide, "✕", card_l + Inches(0.12), top + Inches(0.1), Inches(0.4), Inches(0.5),
            size=20, bold=True, color=ACCENT_RED)
        txt(slide, title, card_l + Inches(0.48), top + Inches(0.08),
            card_w - Inches(0.6), Inches(0.36), size=14, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
        txt(slide, body, card_l + Inches(0.48), top + Inches(0.44),
            card_w - Inches(0.6), Inches(0.72), size=11.5, color=GREY_MID, wrap=True, align=PP_ALIGN.LEFT)

    # ── Quote block ───────────────────────────────────────────────────────────
    ql, qt, qw = Inches(6.5), Inches(1.32), Inches(6.5)
    box(slide, ql, qt, qw, Inches(2.55), fill=CARD_BG, line_color=ACCENT_CYAN, lw=1.5)
    txt(slide, "\u201c", ql + Inches(0.15), qt + Inches(0.05), Inches(0.6), Inches(0.7),
        size=60, bold=True, color=ACCENT_CYAN)
    txt(slide,
        "They automate tool execution. CMatrix automates the reasoning of a professional penetration tester.",
        ql + Inches(0.2), qt + Inches(0.55), qw - Inches(0.4), Inches(1.6),
        size=20, italic=True, color=WHITE, wrap=True, align=PP_ALIGN.LEFT)
    txt(slide, "— CMatrix Design Philosophy",
        ql + Inches(0.2), qt + Inches(2.2), qw - Inches(0.4), Inches(0.35),
        size=12, color=GREY_MID, align=PP_ALIGN.LEFT)

    # ── Root Cause ────────────────────────────────────────────────────────────
    box(slide, ql, Inches(4.02), qw, Inches(0.38), fill=ACCENT_RED)
    txt(slide, "⚠  ROOT CAUSE", ql + Inches(0.2), Inches(4.05), qw - Inches(0.3), Inches(0.33),
        size=13, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    box(slide, ql, Inches(4.42), qw, Inches(1.42), fill=CARD_BG, line_color=ACCENT_RED, lw=1.0)
    txt(slide,
        "Existing systems have no structured model of the target environment "
        "and no structured model of what attack paths are possible.  "
        "They know what they did — not what the target is, or what can be done to it.",
        ql + Inches(0.2), Inches(4.5), qw - Inches(0.35), Inches(1.26),
        size=12.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # ── Solution teaser ───────────────────────────────────────────────────────
    box(slide, Inches(0.3), Inches(6.08), SLIDE_W - Inches(0.6), Inches(0.85),
        fill=RGBColor(0x05, 0x14, 0x20), line_color=ACCENT_CYAN, lw=1.0)
    txt(slide,
        "CMatrix Solution →  Dual-graph world model: "
        "ASG captures discovered reality  ·  APG captures inferred attack opportunity",
        Inches(0.5), Inches(6.18), SLIDE_W - Inches(1.0), Inches(0.62),
        size=14, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    slide_number(slide, "02", ACCENT_RED)
