"""
Slide 3 — Research Contributions (Novel Work)
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_GOLD)
    slide_header(slide, "NOVEL CONTRIBUTION",
                 "What Makes CMatrix a Research Contribution",
                 ACCENT_GOLD, title_size=32)

    # ── Primary insight banner ────────────────────────────────────────────────
    box(slide, Inches(0.3), Inches(1.2), SLIDE_W - Inches(0.6), Inches(0.56),
        fill=RGBColor(0x12, 0x10, 0x02), line_color=ACCENT_GOLD, lw=1.5)
    txt(slide,
        "CMatrix is the first autonomous VAPT system to maintain two strictly separated, "
        "continuously evolving graph structures — one for discovered reality, one for inferred attack opportunity.",
        Inches(0.55), Inches(1.28), SLIDE_W - Inches(1.0), Inches(0.44),
        size=13, italic=True, color=ACCENT_GOLD, wrap=True, align=PP_ALIGN.LEFT)

    # ── 6 contribution cards  3 × 2 ──────────────────────────────────────────
    contributions = [
        ("C1", "Dual-Graph World Model",
         "ASG (discovered reality) + APG (inferred opportunity) — strictly separated with enforced write ownership. "
         "No prior system maintains these as distinct structures."),
        ("C2", "Graph-State-Driven Re-Planning",
         "Re-planning fires on explicit graph triggers (new vuln node seeds a chain, chain status changes) — "
         "not fixed task completion or arbitrary schedules."),
        ("C3", "APG Attack Chain Lifecycle",
         "Attack chains are first-class entities: risk-scored, prioritized, lifecycle-tracked "
         "(HYPOTHESIZED → VALIDATED / RULED_OUT) with evidence-linked ChainSteps."),
        ("C5", "Tool Risk Gate + Commander Mailbox",
         "Every tool call is risk-classified before execution. High-risk ops route to Commander for approval — "
         "a zero-code insertion point for human-in-the-loop."),
        ("C10", "Cross-Mission Experience Store",
         "Persistent RAG-backed store of validated exploitation outcomes across missions. "
         "Commander seeds APG hypotheses from prior analogous engagements at mission start."),
        ("C11", "Attack Strategy Library",
         "Crystallizes validated chains into named, parameterized strategies when the same target fingerprint "
         "succeeds across 2+ missions. No prior system accumulates strategies across sessions."),
    ]

    card_w = Inches(4.15)
    card_h = Inches(1.75)
    gap_x  = Inches(0.13)
    gap_y  = Inches(0.12)
    start_l = Inches(0.3)
    start_t = Inches(1.95)

    for idx, (cnum, title, body) in enumerate(contributions):
        col = idx % 3
        row = idx // 3
        l = start_l + col * (card_w + gap_x)
        t = start_t + row * (card_h + gap_y)
        box(slide, l, t, card_w, card_h, fill=CARD_BG, line_color=ACCENT_GOLD, lw=0.8)
        box(slide, l, t, Inches(0.55), Inches(0.42), fill=ACCENT_GOLD)
        txt(slide, cnum, l + Inches(0.02), t + Inches(0.03), Inches(0.52), Inches(0.36),
            size=11, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
        txt(slide, title, l + Inches(0.62), t + Inches(0.07), card_w - Inches(0.7), Inches(0.38),
            size=13, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
        txt(slide, body, l + Inches(0.12), t + Inches(0.52), card_w - Inches(0.2), Inches(1.15),
            size=11, color=GREY_MID, wrap=True, align=PP_ALIGN.LEFT)

    # ── Bottom strip ──────────────────────────────────────────────────────────
    box(slide, Inches(0.3), Inches(5.7), SLIDE_W - Inches(0.6), Inches(0.5),
        fill=RGBColor(0x0D, 0x12, 0x20), line_color=ACCENT_CYAN, lw=0.8)
    txt(slide,
        "12 novel research contributions in total  ·  C4: ASG-aware parallel dispatch  ·  "
        "C6: Lossless context compaction  ·  C7: Methodology-as-config  ·  C8: Dual-graph termination  ·  "
        "C9: Live CVE grounding  ·  C12: Trajectory export dataset",
        Inches(0.55), Inches(5.77), SLIDE_W - Inches(0.9), Inches(0.38),
        size=10.5, color=GREY_MID, wrap=False, align=PP_ALIGN.LEFT)

    slide_number(slide, "03", ACCENT_GOLD)
