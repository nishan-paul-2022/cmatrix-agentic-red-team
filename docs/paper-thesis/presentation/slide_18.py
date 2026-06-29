"""
Slide 18 — Evaluation Plan
============================
Shows the planned evaluation strategy for CMatrix:
  - Platforms: HackTheBox, TryHackMe, Custom Lab VMs
  - Research Questions (RQ1–RQ4)
  - Evaluation Metrics
  - Baselines + Ablation Study
Matches presentation-final.pptx Slide 18.
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_GOLD)
    slide_header(slide, "EVALUATION PLAN",
                 "How We Will Validate CMatrix Claims Empirically",
                 ACCENT_GOLD, title_size=32, divider_w=9)

    # ── Left column: Platforms + Research Questions ───────────────────────────
    LP_L, LP_W = Inches(0.22), Inches(6.4)
    LP_T = Inches(1.08)

    # Platforms
    box(slide, LP_L, LP_T, LP_W, Inches(2.5),
        fill=RGBColor(0x0C, 0x10, 0x22), line_color=ACCENT_CYAN, lw=1.4)
    box(slide, LP_L, LP_T, LP_W, Inches(0.32), fill=ACCENT_CYAN)
    txt(slide, "EVALUATION PLATFORMS", LP_L, LP_T + Inches(0.04), LP_W, Inches(0.26),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    platforms = [
        ("HackTheBox (HTB)",
         "Retired machines — Linux + Windows — known ground-truth vulnerabilities for coverage scoring."),
        ("TryHackMe (THM)",
         "Guided CTF environments with intentionally vulnerable web applications and APIs."),
        ("Custom Lab VMs",
         "Controlled WordPress + Django stack mirroring shopvault.io for repeatable A/B testing."),
    ]
    for i, (name, desc) in enumerate(platforms):
        pt = LP_T + Inches(0.38) + i * Inches(0.7)
        box(slide, LP_L + Inches(0.1), pt, LP_W - Inches(0.2), Inches(0.64),
            fill=RGBColor(0x08, 0x0E, 0x28), line_color=ACCENT_CYAN, lw=0.5)
        txt(slide, name, LP_L + Inches(0.18), pt + Inches(0.04),
            LP_W - Inches(0.3), Inches(0.22),
            size=10, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
        txt(slide, desc, LP_L + Inches(0.18), pt + Inches(0.26),
            LP_W - Inches(0.3), Inches(0.34),
            size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Research Questions
    RQ_T = LP_T + Inches(2.6)
    box(slide, LP_L, RQ_T, LP_W, Inches(3.68),
        fill=RGBColor(0x10, 0x0C, 0x02), line_color=ACCENT_GOLD, lw=1.4)
    box(slide, LP_L, RQ_T, LP_W, Inches(0.32), fill=ACCENT_GOLD)
    txt(slide, "RESEARCH QUESTIONS", LP_L, RQ_T + Inches(0.04), LP_W, Inches(0.26),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    rqs = [
        ("RQ 1",
         "Does the dual-graph architecture improve vulnerability coverage compared to a flat-memory baseline?"),
        ("RQ 2",
         "Does formal dual termination reduce false-early-stops vs timer-based termination?"),
        ("RQ 3",
         "Does cross-mission learning measurably reduce time-to-finding on repeat target-type engagements?"),
        ("RQ 4",
         "Does the risk gate reduce unintended offensive actions without significantly reducing coverage?"),
    ]
    for i, (rq, question) in enumerate(rqs):
        qt = RQ_T + Inches(0.38) + i * Inches(0.8)
        box(slide, LP_L + Inches(0.1), qt, LP_W - Inches(0.2), Inches(0.74),
            fill=RGBColor(0x16, 0x10, 0x02), line_color=ACCENT_GOLD, lw=0.5)
        txt(slide, rq, LP_L + Inches(0.18), qt + Inches(0.04),
            Inches(0.7), Inches(0.22),
            size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
        txt(slide, question, LP_L + Inches(0.92), qt + Inches(0.04),
            LP_W - Inches(1.08), Inches(0.66),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # ── Right column: Metrics + Baselines + Ablation ─────────────────────────
    RP_L = LP_L + LP_W + Inches(0.16)
    RP_W = SLIDE_W - RP_L - Inches(0.22)
    RP_T = LP_T

    # Metrics
    box(slide, RP_L, RP_T, RP_W, Inches(2.3),
        fill=RGBColor(0x04, 0x18, 0x0C), line_color=ACCENT_LIME, lw=1.4)
    box(slide, RP_L, RP_T, RP_W, Inches(0.32), fill=ACCENT_LIME)
    txt(slide, "EVALUATION METRICS", RP_L, RP_T + Inches(0.04), RP_W, Inches(0.26),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    metrics = [
        ("Vulnerability Coverage",  "% of known vulns discovered vs ground truth per machine"),
        ("Chain Precision",         "% of APG AttackChains that result in VALIDATED status"),
        ("Time-to-Finding",         "Wall-clock time from mission start to first VALIDATED chain"),
        ("False Early-Stop Rate",   "% of missions terminated before surface exhaustion"),
        ("Tool Call Efficiency",    "Mean tool calls to first VALIDATED chain per target"),
    ]
    for i, (metric, desc) in enumerate(metrics):
        mt = RP_T + Inches(0.36) + i * Inches(0.38)
        box(slide, RP_L + Inches(0.1), mt, RP_W - Inches(0.2), Inches(0.32),
            fill=RGBColor(0x06, 0x22, 0x0E), line_color=ACCENT_LIME, lw=0.4)
        txt(slide, metric, RP_L + Inches(0.18), mt + Inches(0.04),
            Inches(1.9), Inches(0.24),
            size=8.5, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
        txt(slide, desc, RP_L + Inches(2.1), mt + Inches(0.04),
            RP_W - Inches(2.24), Inches(0.24),
            size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Baselines
    bl_t = RP_T + Inches(2.4)
    box(slide, RP_L, bl_t, RP_W, Inches(1.6),
        fill=RGBColor(0x14, 0x06, 0x06), line_color=ACCENT_RED, lw=1.4)
    box(slide, RP_L, bl_t, RP_W, Inches(0.32), fill=ACCENT_RED)
    txt(slide, "BASELINES", RP_L, bl_t + Inches(0.04), RP_W, Inches(0.26),
        size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    baselines = [
        "✕  PentestGPT:  Task-tree memory, no ASG/APG graph split  →  tests RQ1",
        "✕  VulnBot:  Single unified PTG, no surface/path separation  →  tests RQ1",
        "✕  PentestAgent:  RAG-retrieval memory, no cross-mission learning  →  tests RQ3",
    ]
    for i, bl in enumerate(baselines):
        txt(slide, bl, RP_L + Inches(0.18), bl_t + Inches(0.38) + i * Inches(0.38),
            RP_W - Inches(0.3), Inches(0.32),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Ablation
    ab_t = bl_t + Inches(1.7)
    box(slide, RP_L, ab_t, RP_W, Inches(2.3),
        fill=RGBColor(0x08, 0x10, 0x22), line_color=ACCENT_PURP, lw=1.4)
    box(slide, RP_L, ab_t, RP_W, Inches(0.32), fill=ACCENT_PURP)
    txt(slide, "ABLATION STUDY", RP_L, ab_t + Inches(0.04), RP_W, Inches(0.26),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    ablations = [
        ("A1 — No dual-graph",  "CMatrix with flat history only (remove ASG + APG)"),
        ("A2 — ASG only",       "CMatrix with ASG discovery but no APG reasoning"),
        ("A3 — No compaction",  "CMatrix with unlimited raw history, no lossless context compaction"),
        ("A4 — No learning",    "CMatrix without cross-mission experience and attack strategy library"),
    ]
    for i, (variant, desc) in enumerate(ablations):
        at = ab_t + Inches(0.38) + i * Inches(0.46)
        box(slide, RP_L + Inches(0.1), at, RP_W - Inches(0.2), Inches(0.4),
            fill=RGBColor(0x0C, 0x0E, 0x26), line_color=ACCENT_PURP, lw=0.4)
        txt(slide, variant, RP_L + Inches(0.18), at + Inches(0.04), Inches(1.6), Inches(0.3),
            size=9, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)
        txt(slide, desc, RP_L + Inches(1.82), at + Inches(0.04), RP_W - Inches(1.98), Inches(0.3),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "18", ACCENT_GOLD)
