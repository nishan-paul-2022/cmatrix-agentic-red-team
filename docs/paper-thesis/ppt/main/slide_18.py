"""
Slide 18 — What CMatrix Uniquely Introduces
=============================================
One-slide summary of the architectural gaps CMatrix fills that no prior system addresses.
Structured as a matrix: 4 areas × 2 columns (what exists vs what CMatrix adds).
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_LIME)
    slide_header(slide, "WHAT CMATRIX UNIQUELY INTRODUCES",
                 "The Architecture No Prior Autonomous VAPT System Has Built",
                 ACCENT_LIME, title_size=26, divider_w=11)

    # ── Header row ────────────────────────────────────────────────────────────
    HDR_T = Inches(1.05)
    hdrs = [
        (Inches(0.22), Inches(2.5),  "AREA",               ACCENT_LIME),
        (Inches(2.82), Inches(4.9),  "WHAT EXISTS",        GREY_DARK),
        (Inches(7.92), Inches(5.2),  "CMATRIX INTRODUCES", ACCENT_LIME),
    ]
    for hl, hw, label, clr in hdrs:
        box(slide, hl, HDR_T, hw, Inches(0.32), fill=clr)
        txt(slide, label, hl + Inches(0.08), HDR_T + Inches(0.05), hw - Inches(0.12), Inches(0.24),
            size=9.5, bold=True, color=BG_DARK if clr != GREY_DARK else WHITE, align=PP_ALIGN.CENTER)

    # ── Content rows ──────────────────────────────────────────────────────────
    rows = [
        (
            "World\nModel",
            ACCENT_CYAN,
            "Flat conversation history (PentestGPT)  ·  Task queues (VulnBot)  ·  "
            "RAG-backed untyped memory (PentestAgent)",
            "Dual typed property graphs: ASG (confirmed facts) + APG (attack reasoning).  "
            "Strict write separation enforced per agent role.  "
            "Graph edges express relationships (affected_by, starts_at) that vector similarity cannot represent.",
        ),
        (
            "Termination\nLogic",
            ACCENT_TEAL,
            "Wall-clock timeout (PentestGPT)  ·  Empty task queue (VulnBot)  ·  "
            "Ad-hoc human decision (most systems)",
            "Formal dual condition: ASG exhaustion (∀ node.status = INVESTIGATED)  AND  "
            "APG resolution (∀ chain.status ∈ {VALIDATED, RULED_OUT}).  Both required simultaneously.",
        ),
        (
            "Cross-Mission\nLearning",
            ACCENT_GOLD,
            "AutoAttacker reuses subtasks within one session.  "
            "All other prior systems reset to zero knowledge on each mission.",
            "Cross-Mission Experience Store (C10) + Attack Strategy Library (C11):  "
            "validated exploitation outcomes accumulate across every mission ever run.  "
            "Pre-ranked APG seeds at mission start for known target-type fingerprints.",
        ),
        (
            "Trajectory\nExport",
            ACCENT_PURP,
            "No prior autonomous VAPT system produces machine-readable decision logs "
            "usable for ML training.",
            "C12: every mission generates a structured decision log capturing ASG/APG triggers, "
            "Commander rationale, and actions taken.  "
            "Directly usable as SFT/RL training data for security-specialized LLMs.",
        ),
    ]

    ROW_T = HDR_T + Inches(0.36)
    ROW_H = (SLIDE_H - ROW_T - Inches(0.28)) / len(rows)

    for i, (area, clr, exists, introduces) in enumerate(rows):
        rt = ROW_T + i * ROW_H
        rh = ROW_H - Inches(0.06)
        bg = RGBColor(0x0C, 0x0C, 0x1A) if i % 2 == 0 else RGBColor(0x08, 0x08, 0x14)

        # Area column
        box(slide, Inches(0.22), rt, Inches(2.5), rh, fill=bg, line_color=clr, lw=1.0)
        box(slide, Inches(0.22), rt, Inches(0.06), rh, fill=clr)
        txt(slide, area, Inches(0.34), rt + Inches(0.1), Inches(2.3), rh - Inches(0.18),
            size=11, bold=True, color=clr, align=PP_ALIGN.CENTER, wrap=True)

        # What exists column
        box(slide, Inches(2.82), rt, Inches(4.9), rh, fill=bg, line_color=GREY_DARK, lw=0.5)
        txt(slide, exists, Inches(2.92), rt + Inches(0.06), Inches(4.7), rh - Inches(0.1),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

        # CMatrix column
        box(slide, Inches(7.92), rt, Inches(5.2), rh, fill=RGBColor(0x04, 0x14, 0x06), line_color=clr, lw=0.8)
        txt(slide, introduces, Inches(8.02), rt + Inches(0.06), Inches(5.0), rh - Inches(0.1),
            size=9, color=ACCENT_LIME, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "18", ACCENT_LIME)
