"""
Slide 18 — Evaluation Plan
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_GOLD)

    # ── Header ────────────────────────────────────────────────────────────────
    txt(slide, "EVALUATION PLAN",
        Inches(0.3), Inches(0.07), Inches(8.0), Inches(0.27),
        size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
    txt(slide, "How We Will Validate CMatrix Claims Empirically",
        Inches(0.3), Inches(0.32), Inches(12.5), Inches(0.64),
        size=32, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # ═══════════════════════════════════════════════════════
    # LEFT COLUMN
    # ═══════════════════════════════════════════════════════

    # EVALUATION PLATFORMS block
    box(slide, Inches(0.22), Inches(1.08), Inches(6.40), Inches(2.50),
        fill=RGBColor(0x0C, 0x10, 0x22), line_color=ACCENT_CYAN, lw=1.4)
    box(slide, Inches(0.22), Inches(1.08), Inches(6.40), Inches(0.32), fill=ACCENT_CYAN)
    txt(slide, "EVALUATION PLATFORMS",
        Inches(0.22), Inches(1.12), Inches(6.40), Inches(0.27),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    platforms = [
        ("HackTheBox (HTB)", ACCENT_CYAN,
         "Retired machines — Linux + Windows — known ground-truth vulnerabilities for coverage scoring."),
        ("TryHackMe (THM)", ACCENT_LIME,
         "Guided CTF environments with intentionally vulnerable web applications and APIs."),
        ("Custom Lab VMs", ACCENT_GOLD,
         "Controlled WordPress + Django stack mirroring shopvault.io for repeatable A/B testing."),
    ]
    plat_tops = [Inches(1.46), Inches(2.14), Inches(2.82)]
    plat_line_colors = [ACCENT_CYAN, ACCENT_LIME, ACCENT_GOLD]

    for (name, color, desc), pt, lc in zip(platforms, plat_tops, plat_line_colors):
        box(slide, Inches(0.32), pt, Inches(6.20), Inches(0.62),
            fill=RGBColor(0x08, 0x14, 0x24), line_color=lc, lw=0.8)
        txt(slide, name,
            Inches(0.42), pt + Inches(0.04), Inches(6.08), Inches(0.27),
            size=10, bold=True, color=color, align=PP_ALIGN.LEFT)
        txt(slide, desc,
            Inches(0.42), pt + Inches(0.32), Inches(6.08), Inches(0.25),
            size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # RESEARCH QUESTIONS block
    box(slide, Inches(0.22), Inches(3.68), Inches(6.40), Inches(3.60),
        fill=RGBColor(0x0E, 0x0C, 0x04), line_color=ACCENT_GOLD, lw=1.4)
    box(slide, Inches(0.22), Inches(3.68), Inches(6.40), Inches(0.32), fill=ACCENT_GOLD)
    txt(slide, "RESEARCH QUESTIONS",
        Inches(0.22), Inches(3.72), Inches(6.40), Inches(0.27),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    rqs = [
        ("RQ 1", "Does the dual-graph architecture improve vulnerability coverage compared to a flat-memory baseline?",
         Inches(4.06)),
        ("RQ 2", "Does formal dual termination reduce false-early-stops vs timer-based termination?",
         Inches(4.88)),
        ("RQ 3", "Does cross-mission learning measurably reduce time-to-finding on repeat target-type engagements?",
         Inches(5.70)),
        ("RQ 4", "Does the risk gate reduce unintended offensive actions without significantly reducing coverage?",
         Inches(6.52)),
    ]
    for rq_label, rq_text, rq_top in rqs:
        box(slide, Inches(0.32), rq_top, Inches(0.568), Inches(0.70),
            fill=ACCENT_GOLD)
        txt(slide, rq_label,
            Inches(0.345), rq_top + Inches(0.18), Inches(0.53), Inches(0.27),
            size=10, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)
        txt(slide, rq_text,
            Inches(0.84), rq_top + Inches(0.04), Inches(5.66), Inches(0.64),
            size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # ═══════════════════════════════════════════════════════
    # RIGHT COLUMN
    # ═══════════════════════════════════════════════════════

    # EVALUATION METRICS block
    box(slide, Inches(6.76), Inches(1.08), Inches(6.353), Inches(2.30),
        fill=RGBColor(0x06, 0x14, 0x08), line_color=ACCENT_LIME, lw=1.4)
    box(slide, Inches(6.76), Inches(1.08), Inches(6.353), Inches(0.32), fill=ACCENT_LIME)
    txt(slide, "EVALUATION METRICS",
        Inches(6.76), Inches(1.12), Inches(6.353), Inches(0.27),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    metrics = [
        ("Vulnerability Coverage", "% of known vulns discovered vs ground truth per machine"),
        ("Chain Precision",         "% of APG AttackChains that result in VALIDATED status"),
        ("Time-to-Finding",         "Wall-clock time from mission start to first VALIDATED chain"),
        ("False Early-Stop Rate",   "% of missions terminated before surface exhaustion"),
        ("Tool Call Efficiency",    "Mean tool calls to first VALIDATED chain per target"),
    ]
    met_tops = [Inches(1.46), Inches(1.84), Inches(2.22), Inches(2.60), Inches(2.98)]
    for (met_name, met_desc), mt in zip(metrics, met_tops):
        box(slide, Inches(6.86), mt, Inches(6.153), Inches(0.34),
            fill=RGBColor(0x06, 0x1C, 0x0A), line_color=ACCENT_LIME, lw=0.8)
        txt(slide, met_name,
            Inches(6.94), mt + Inches(0.04), Inches(1.85), Inches(0.25),
            size=9.0, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
        txt(slide, met_desc,
            Inches(8.84), mt + Inches(0.04), Inches(4.153), Inches(0.25),
            size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT)

    # BASELINES block
    box(slide, Inches(6.76), Inches(3.48), Inches(6.353), Inches(1.60),
        fill=RGBColor(0x18, 0x08, 0x08), line_color=ACCENT_RED, lw=1.4)
    box(slide, Inches(6.76), Inches(3.48), Inches(6.353), Inches(0.32), fill=ACCENT_RED)
    txt(slide, "BASELINES",
        Inches(6.76), Inches(3.52), Inches(6.353), Inches(0.27),
        size=10, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    baselines = [
        "✕  PentestGPT:  Task-tree memory, no ASG/APG graph split  →  tests RQ1",
        "✕  VulnBot:  Single unified PTG, no surface/path separation  →  tests RQ1",
        "✕  PentestAgent:  RAG-retrieval memory, no cross-mission learning  →  tests RQ3",
    ]
    for bi, bline in enumerate(baselines):
        txt(slide, bline,
            Inches(6.92), Inches(3.86) + bi * Inches(0.40), Inches(6.073), Inches(0.25),
            size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT)

    # ABLATION STUDY block
    box(slide, Inches(6.76), Inches(5.18), Inches(6.353), Inches(2.10),
        fill=RGBColor(0x08, 0x10, 0x22), line_color=ACCENT_PURP, lw=1.4)
    box(slide, Inches(6.76), Inches(5.18), Inches(6.353), Inches(0.32), fill=ACCENT_PURP)
    txt(slide, "ABLATION STUDY",
        Inches(6.76), Inches(5.22), Inches(6.353), Inches(0.27),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    ablations = [
        ("A1 — No dual-graph",   "CMatrix with flat history only (remove ASG + APG)"),
        ("A2 — ASG only",        "CMatrix with ASG discovery but no APG reasoning"),
        ("A3 — No compaction",   "CMatrix with unlimited raw history, no lossless context compaction"),
        ("A4 — No learning",     "CMatrix without cross-mission experience and attack strategy library"),
    ]
    abl_tops = [Inches(5.56), Inches(6.02), Inches(6.48), Inches(6.80)]
    for (abl_name, abl_desc), at in zip(ablations, abl_tops):
        box(slide, Inches(6.86), at, Inches(6.153), Inches(0.40),
            fill=RGBColor(0x0C, 0x0E, 0x26), line_color=ACCENT_PURP, lw=0.8)
        txt(slide, abl_name,
            Inches(6.94), at + Inches(0.06), Inches(1.60), Inches(0.25),
            size=9.0, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)
        txt(slide, abl_desc,
            Inches(8.58), at + Inches(0.06), Inches(4.373), Inches(0.40),
            size=9.0, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "18", ACCENT_GOLD)
