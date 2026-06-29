"""
Slide 20 — Closing Summary / Call to Action
=============================================
Crystallises: What is CMatrix, what it claims, what you are asking the supervisor for.
Clean, minimal, memorable — designed to be the last slide the supervisor sees before Q&A.
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)

    # Chrome: gradient-style (cyan left + lime top + cyan bottom)
    box(slide, Inches(0), Inches(0), Inches(0.06), SLIDE_H, fill=ACCENT_CYAN)
    box(slide, Inches(0.06), Inches(0), SLIDE_W - Inches(0.06), Inches(0.04), fill=ACCENT_LIME)
    box(slide, Inches(0.06), SLIDE_H - Inches(0.04), SLIDE_W - Inches(0.06), Inches(0.04), fill=ACCENT_CYAN)

    # Title
    txt(slide, "SUMMARY", Inches(0.3), Inches(0.08), Inches(5), Inches(0.26),
        size=10, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
    txt(slide, "CMatrix — What We Built, What We Claim, What We Need",
        Inches(0.3), Inches(0.34), Inches(12.5), Inches(0.52),
        size=28, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    box(slide, Inches(0.3), Inches(0.92), Inches(11), Inches(0.03), fill=GREY_MID)

    # Left: One-paragraph summary
    SUM_L, SUM_W = Inches(0.3), Inches(5.5)
    SUM_T = Inches(1.08)

    box(slide, SUM_L, SUM_T, SUM_W, Inches(1.65),
        fill=RGBColor(0x04, 0x12, 0x22), line_color=ACCENT_CYAN, lw=1.6)
    txt(slide, "WHAT CMATRIX IS", SUM_L + Inches(0.12), SUM_T + Inches(0.06),
        SUM_W - Inches(0.2), Inches(0.22), size=10, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
    txt(slide,
        "A dual-graph-guided, LLM-orchestrated multi-agent framework for autonomous Vulnerability "
        "Assessment and Penetration Testing.  It maintains two strictly separated graph structures — "
        "the ASG (what the target is) and the APG (what can be done to it) — and uses both to "
        "plan, dispatch, validate, and formally terminate a complete VAPT engagement without human intervention.",
        SUM_L + Inches(0.14), SUM_T + Inches(0.34), SUM_W - Inches(0.24), Inches(1.26),
        size=10.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # 12 contributions summary
    box(slide, SUM_L, SUM_T + Inches(1.78), SUM_W, Inches(4.48),
        fill=RGBColor(0x08, 0x10, 0x04), line_color=ACCENT_LIME, lw=1.4)
    txt(slide, "12 ORIGINAL RESEARCH CONTRIBUTIONS", SUM_L + Inches(0.12), SUM_T + Inches(1.84),
        SUM_W - Inches(0.2), Inches(0.22), size=10, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    contribs = [
        "C1  Dual-Graph World Model (ASG + APG, strictly separated)",
        "C2  Graph-Driven Re-Planning (trigger: new Vulnerability node)",
        "C3  APG Chain Lifecycle with Evidence Traceability",
        "C4  ASG-Aware Parallel Dispatch",
        "C5  Tool Risk Gate + Commander Mailbox",
        "C6  Lossless Context Compaction (3-layer)",
        "C7  Methodology-as-Config (VAPT Protocol Prompt)",
        "C8  Dual Termination (ASG exhausted ∧ APG resolved)",
        "C9  Live CVE Grounding (Research Agent)",
        "C10 Cross-Mission Experience Store",
        "C11 Attack Strategy Library (crystallization)",
        "C12 Trajectory Export Dataset (SFT/RL ready)",
    ]
    for i, c in enumerate(contribs):
        ct = SUM_T + Inches(2.12) + i * Inches(0.34)
        clr = ACCENT_LIME if i % 2 == 0 else ACCENT_CYAN
        txt(slide, c, SUM_L + Inches(0.2), ct, SUM_W - Inches(0.28), Inches(0.3),
            size=9.5, bold=(i % 2 == 0), color=clr, align=PP_ALIGN.LEFT)

    # Right: Claims + What we need
    RP_L = SUM_L + SUM_W + Inches(0.22)
    RP_W = SLIDE_W - RP_L - Inches(0.22)
    RP_T = SUM_T

    # Claims
    box(slide, RP_L, RP_T, RP_W, Inches(3.04),
        fill=RGBColor(0x16, 0x12, 0x02), line_color=ACCENT_GOLD, lw=1.4)
    txt(slide, "WHAT WE CLAIM", RP_L + Inches(0.12), RP_T + Inches(0.06),
        RP_W - Inches(0.2), Inches(0.22), size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    claims = [
        "CMatrix is the first autonomous VAPT system to maintain two strictly separated, "
        "continuously evolving graph structures for simultaneous discovery and attack reasoning.",
        "Formal dual termination provides a theoretically sound, verifiable completion criterion "
        "that prior systems cannot express.",
        "Cross-mission learning accumulates validated exploitation outcomes across all missions — "
        "a capability no prior published VAPT system demonstrates.",
        "The architecture produces a machine-readable decision trace usable for training "
        "security-specialized LLMs (C12 — novel in the VAPT domain).",
    ]
    for i, claim in enumerate(claims):
        ct = RP_T + Inches(0.34) + i * Inches(0.64)
        box(slide, RP_L + Inches(0.1), ct, RP_W - Inches(0.2), Inches(0.58),
            fill=RGBColor(0x1E, 0x16, 0x02), line_color=ACCENT_GOLD, lw=0.5)
        txt(slide, f"→  {claim}", RP_L + Inches(0.18), ct + Inches(0.04),
            RP_W - Inches(0.3), Inches(0.5), size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # What we need
    wn_t = RP_T + Inches(3.16)
    box(slide, RP_L, wn_t, RP_W, Inches(3.1),
        fill=RGBColor(0x04, 0x14, 0x10), line_color=ACCENT_TEAL, lw=1.6)
    box(slide, RP_L, wn_t, RP_W, Inches(0.32), fill=ACCENT_TEAL)
    txt(slide, "WHAT WE ARE ASKING FOR", RP_L + Inches(0.12), wn_t + Inches(0.04),
        RP_W - Inches(0.2), Inches(0.26), size=10, bold=True, color=BG_DARK)

    asks = [
        ("Feedback on Scope", "Are the 12 contributions appropriately scoped for a PhD thesis?"),
        ("Evaluation Guidance", "Is the HTB/THM ablation plan sufficient to prove the core claims?"),
        ("Implementation Priority", "Which of C1–C12 should be fully implemented vs theoretically validated?"),
        ("Publication Venue", "USENIX Security / IEEE S&P / ACSAC — which tier matches the contribution level?"),
    ]
    for i, (heading, question) in enumerate(asks):
        at = wn_t + Inches(0.38) + i * Inches(0.68)
        box(slide, RP_L + Inches(0.1), at, RP_W - Inches(0.2), Inches(0.62),
            fill=RGBColor(0x06, 0x1C, 0x16), line_color=ACCENT_TEAL, lw=0.6)
        txt(slide, heading, RP_L + Inches(0.2), at + Inches(0.04), RP_W - Inches(0.32), Inches(0.22),
            size=10, bold=True, color=ACCENT_TEAL, align=PP_ALIGN.LEFT)
        txt(slide, question, RP_L + Inches(0.2), at + Inches(0.28), RP_W - Inches(0.32), Inches(0.3),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "20", ACCENT_CYAN)
