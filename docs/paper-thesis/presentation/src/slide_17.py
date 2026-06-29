"""
Slide 17 — What Makes CMatrix a Research Contribution
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_GOLD)

    # ── Header ────────────────────────────────────────────────────────────────
    txt(slide, "NOVEL CONTRIBUTION",
        Inches(0.3), Inches(0.07), Inches(8.0), Inches(0.26),
        size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
    txt(slide, "What Makes CMatrix a Research Contribution",
        Inches(0.3), Inches(0.32), Inches(12.5), Inches(0.52),
        size=32, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # ── Thesis statement banner ───────────────────────────────────────────────
    box(slide, Inches(0.3), Inches(1.20), Inches(12.733), Inches(0.56),
        fill=RGBColor(0x12, 0x10, 0x02), line_color=ACCENT_GOLD, lw=1.5)
    txt(slide, "First autonomous VAPT system to maintain two strictly separated, continuously evolving graph structures - one for discovered reality, one for inferred attack opportunity.",
        Inches(0.405), Inches(1.32), Inches(12.5), Inches(0.32),
        size=13, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    # ── Contribution cards: 3 rows × 3 cols ──────────────────────────────────
    contributions = [
        ("C1",  "Dual-Graph World Model",
         "ASG (discovered reality) & APG (inferred opportunity) are strictly separated with enforced write ownership."),
        ("C2",  "Graph-Driven Re-Planning",
         "Re-planning fires on explicit graph triggers (e.g., new vuln node seeds a chain) rather than arbitrary schedules."),
        ("C3",  "APG Attack Chain Lifecycle with Evidence Traceability",
         "Attack chains are first-class entities: risk-scored, prioritized, lifecycle-tracked. Every ChainStep links to ASG Evidence via supported_by."),
        ("C4",  "ASG-Aware Parallel Dispatch",
         "Dependency-safe concurrent tool execution using the ASG itself as the dependency graph, instead of a task scheduler."),
        ("C5",  "Tool Risk Gate + Mailbox",
         "Every tool call is risk-classified before execution. High-risk ops route to Commander for human-in-the-loop approval."),
        ("C6",  "Lossless Context Compaction",
         "ASG-backed three-layer compaction scheme reduces conversation history to near-zero without losing discovered findings."),
        ("C7",  "Methodology-as-Config",
         "Commander's planning policy is encoded as a versioned natural-language document, allowing methodology benchmarking."),
        ("C8",  "Dual-Graph Termination",
         "Mission completion is formally defined as the conjunction of ASG exhaustion (no unexplored nodes) and APG resolution."),
        ("C9",  "Live CVE Grounding",
         "Real-time vulnerability enrichment and exploit feasibility research via a scoped agent, written back into the ASG."),
        ("C10", "Cross-Mission Experience",
         "Persistent RAG-backed store of validated exploitation outcomes across missions to seed APG hypotheses at mission start."),
        ("C11", "Attack Strategy Library",
         "Crystallizes validated chains into parameterized strategies when the same target fingerprint succeeds across missions."),
        ("C12", "Trajectory Export Dataset",
         "Every mission produces a machine-readable decision log capturing ASG/APG triggers, rationale, and actions taken."),
    ]

    CARD_W = Inches(4.15)
    CARD_H = Inches(1.25)
    BADGE_W = Inches(0.55)
    BADGE_H = Inches(0.36)
    COL_GAP = Inches(0.14)
    ROW_GAP = Inches(0.12)

    col_starts = [Inches(0.30), Inches(4.58), Inches(8.86)]
    row_starts = [Inches(1.95), Inches(3.32), Inches(4.69), Inches(6.06)]

    for i, (badge, title, body) in enumerate(contributions):
        row = i // 3
        col = i % 3
        cl = col_starts[col]
        rt = row_starts[row]

        box(slide, cl, rt, CARD_W, CARD_H,
            fill=CARD_BG, line_color=ACCENT_GOLD, lw=0.8)
        # Gold badge
        box(slide, cl, rt, BADGE_W, BADGE_H, fill=ACCENT_GOLD)
        txt(slide, badge,
            cl + Inches(0.02), rt + Inches(0.02), BADGE_W - Inches(0.04), BADGE_H - Inches(0.04),
            size=11, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
        txt(slide, title,
            cl + BADGE_W + Inches(0.08), rt + Inches(0.02),
            CARD_W - BADGE_W - Inches(0.12), Inches(0.32),
            size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
        txt(slide, body,
            cl + Inches(0.12), rt + BADGE_H + Inches(0.06),
            CARD_W - Inches(0.18), Inches(0.75),
            size=10.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "17", ACCENT_GOLD)
