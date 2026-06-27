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
        "First autonomous VAPT system to maintain two strictly separated, "
        "continuously evolving graph structures - one for discovered reality, one for inferred attack opportunity.",
        Inches(0.55), Inches(1.28), SLIDE_W - Inches(1.0), Inches(0.44),
        size=13, italic=True, color=ACCENT_GOLD, wrap=True, align=PP_ALIGN.LEFT)

    # ── 12 contribution cards  3 × 4 ─────────────────────────────────────────
    contributions = [
        ("C1", "Dual-Graph World Model",
         "ASG (discovered reality) & APG (inferred opportunity) are strictly separated with enforced write ownership."),
        ("C2", "Graph-Driven Re-Planning",
         "Re-planning fires on explicit graph triggers (e.g., new vuln node seeds a chain) rather than arbitrary schedules."),
        ("C3", "APG Attack Chain Lifecycle with Evidence Traceability",
         "Attack chains are first-class entities: risk-scored, prioritized, lifecycle-tracked. Every ChainStep links to ASG Evidence via supported_by."),
        ("C4", "ASG-Aware Parallel Dispatch",
         "Dependency-safe concurrent tool execution using the ASG itself as the dependency graph, instead of a task scheduler."),
        ("C5", "Tool Risk Gate + Mailbox",
         "Every tool call is risk-classified before execution. High-risk ops route to Commander for human-in-the-loop approval."),
        ("C6", "Lossless Context Compaction",
         "ASG-backed three-layer compaction scheme reduces conversation history to near-zero without losing discovered findings."),
        ("C7", "Methodology-as-Config",
         "Commander's planning policy is encoded as a versioned natural-language document, allowing methodology benchmarking."),
        ("C8", "Dual-Graph Termination",
         "Mission completion is formally defined as the conjunction of ASG exhaustion (no unexplored nodes) and APG resolution."),
        ("C9", "Live CVE Grounding",
         "Real-time vulnerability enrichment and exploit feasibility research via a scoped agent, written back into the ASG."),
        ("C10", "Cross-Mission Experience",
         "Persistent RAG-backed store of validated exploitation outcomes across missions to seed APG hypotheses at mission start."),
        ("C11", "Attack Strategy Library",
         "Crystallizes validated chains into parameterized strategies when the same target fingerprint succeeds across missions."),
        ("C12", "Trajectory Export Dataset",
         "Every mission produces a machine-readable decision log capturing ASG/APG triggers, rationale, and actions taken.")
    ]

    card_w = Inches(4.15)
    card_h = Inches(1.25)
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
        box(slide, l, t, Inches(0.55), Inches(0.36), fill=ACCENT_GOLD)
        txt(slide, cnum, l + Inches(0.02), t + Inches(0.02), Inches(0.52), Inches(0.32),
            size=11, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
        txt(slide, title, l + Inches(0.62), t + Inches(0.04), card_w - Inches(0.7), Inches(0.32),
            size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
        txt(slide, body, l + Inches(0.12), t + Inches(0.42), card_w - Inches(0.2), Inches(0.75),
            size=10.5, color=GREY_MID, wrap=True, align=PP_ALIGN.LEFT)



    slide_number(slide, "17", ACCENT_GOLD)
