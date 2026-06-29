"""
Slide 19 — Evaluation Plan
============================
Shows the planned evaluation strategy:
- Platforms: HackTheBox, TryHackMe, custom lab VMs
- Metrics: Vulnerability coverage, chain precision, time-to-finding vs baseline
- Baseline: PentestGPT (flat history), manual VAPT (timed expert), random tool agent
- Research questions
- Expected deliverable: ablation comparing dual-graph vs single-graph vs no-graph
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
        size=10, bold=True, color=BG_DARK)

    platforms = [
        ("HackTheBox (HTB)", "Retired machines — Linux + Windows — known ground-truth vulnerabilities for coverage scoring.", ACCENT_CYAN),
        ("TryHackMe (THM)", "Guided CTF environments with intentionally vulnerable web applications and APIs.", ACCENT_LIME),
        ("Custom Lab VMs",  "Controlled WordPress + Django stack mirroring shopvault.io for repeatable A/B testing.", ACCENT_GOLD),
    ]
    for i, (name, detail, clr) in enumerate(platforms):
        pt = LP_T + Inches(0.38) + i * Inches(0.68)
        box(slide, LP_L + Inches(0.1), pt, LP_W - Inches(0.2), Inches(0.62),
            fill=RGBColor(0x08, 0x14, 0x24), line_color=clr, lw=0.6)
        txt(slide, name, LP_L + Inches(0.2), pt + Inches(0.04), LP_W - Inches(0.32), Inches(0.22),
            size=10, bold=True, color=clr, align=PP_ALIGN.LEFT)
        txt(slide, detail, LP_L + Inches(0.2), pt + Inches(0.28), LP_W - Inches(0.32), Inches(0.3),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Research Questions
    rq_t = LP_T + Inches(2.6)
    box(slide, LP_L, rq_t, LP_W, Inches(3.76),
        fill=RGBColor(0x0E, 0x0C, 0x04), line_color=ACCENT_GOLD, lw=1.4)
    box(slide, LP_L, rq_t, LP_W, Inches(0.32), fill=ACCENT_GOLD)
    txt(slide, "RESEARCH QUESTIONS", LP_L, rq_t + Inches(0.04), LP_W, Inches(0.26),
        size=10, bold=True, color=BG_DARK)

    rqs = [
        ("RQ1", "Does the dual-graph architecture improve vulnerability coverage compared to a flat-memory baseline?"),
        ("RQ2", "Does formal dual termination reduce false-early-stops vs timer-based termination?"),
        ("RQ3", "Does cross-mission learning measurably reduce time-to-finding on repeat target-type engagements?"),
        ("RQ4", "Does the risk gate reduce unintended offensive actions without significantly reducing coverage?"),
    ]
    for i, (rq, text) in enumerate(rqs):
        qt = rq_t + Inches(0.38) + i * Inches(0.82)
        box(slide, LP_L + Inches(0.1), qt, Inches(0.45), Inches(0.7), fill=ACCENT_GOLD)
        txt(slide, rq, LP_L + Inches(0.12), qt + Inches(0.18), Inches(0.42), Inches(0.32),
            size=10, bold=True, color=BG_DARK)
        txt(slide, text, LP_L + Inches(0.62), qt + Inches(0.04), LP_W - Inches(0.74), Inches(0.64),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # ── Right column: Metrics + Baseline + Ablation ───────────────────────────
    RP_L = LP_L + LP_W + Inches(0.14)
    RP_W = SLIDE_W - RP_L - Inches(0.22)
    RP_T = LP_T

    # Metrics
    box(slide, RP_L, RP_T, RP_W, Inches(2.3),
        fill=RGBColor(0x06, 0x14, 0x08), line_color=ACCENT_LIME, lw=1.4)
    box(slide, RP_L, RP_T, RP_W, Inches(0.32), fill=ACCENT_LIME)
    txt(slide, "EVALUATION METRICS", RP_L, RP_T + Inches(0.04), RP_W, Inches(0.26),
        size=10, bold=True, color=BG_DARK)

    metrics = [
        ("Vulnerability Coverage", "% of known vulns discovered vs ground truth per machine"),
        ("Chain Precision",         "% of APG AttackChains that result in VALIDATED status"),
        ("Time-to-Finding",         "Wall-clock time from mission start to first VALIDATED chain"),
        ("False Early-Stop Rate",   "% of missions terminated before surface exhaustion"),
        ("Tool Call Efficiency",    "Mean tool calls to first VALIDATED chain per target"),
    ]
    for i, (name, desc) in enumerate(metrics):
        mt = RP_T + Inches(0.38) + i * Inches(0.38)
        box(slide, RP_L + Inches(0.1), mt, RP_W - Inches(0.2), Inches(0.34),
            fill=RGBColor(0x06, 0x1C, 0x0A), line_color=ACCENT_LIME, lw=0.4)
        txt(slide, name, RP_L + Inches(0.18), mt + Inches(0.04),
            Inches(1.85), Inches(0.26), size=9, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
        txt(slide, desc, RP_L + Inches(2.08), mt + Inches(0.04),
            RP_W - Inches(2.2), Inches(0.26), size=9, color=GREY_MID, align=PP_ALIGN.LEFT)

    # Baselines
    bl_t = RP_T + Inches(2.4)
    box(slide, RP_L, bl_t, RP_W, Inches(1.6),
        fill=RGBColor(0x18, 0x08, 0x08), line_color=ACCENT_RED, lw=1.4)
    box(slide, RP_L, bl_t, RP_W, Inches(0.32), fill=ACCENT_RED)
    txt(slide, "BASELINES", RP_L, bl_t + Inches(0.04), RP_W, Inches(0.26),
        size=10, bold=True, color=WHITE)

    baselines = [
        ("PentestGPT", "Flat conversation history — no structured world model"),
        ("Random Tool Agent", "Same tool set, random action selection — no planning"),
        ("Manual Expert", "Timed human VAPT expert on same targets for ground truth"),
    ]
    for i, (name, desc) in enumerate(baselines):
        bt = bl_t + Inches(0.38) + i * Inches(0.4)
        txt(slide, f"✕  {name}:  {desc}",
            RP_L + Inches(0.16), bt, RP_W - Inches(0.28), Inches(0.36),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Ablation
    ab_t = bl_t + Inches(1.7)
    box(slide, RP_L, ab_t, RP_W, Inches(2.3),
        fill=RGBColor(0x08, 0x10, 0x22), line_color=ACCENT_PURP, lw=1.4)
    box(slide, RP_L, ab_t, RP_W, Inches(0.32), fill=ACCENT_PURP)
    txt(slide, "ABLATION STUDY", RP_L, ab_t + Inches(0.04), RP_W, Inches(0.26),
        size=10, bold=True, color=BG_DARK)

    ablations = [
        ("A1 — No dual-graph",   "CMatrix with flat history only (remove ASG + APG)"),
        ("A2 — ASG only",        "CMatrix with ASG discovery but no APG reasoning"),
        ("A3 — No compaction",   "CMatrix with unlimited raw history (no C6)"),
        ("A4 — No learning",     "CMatrix without C10/C11 cross-mission store"),
    ]
    for i, (variant, desc) in enumerate(ablations):
        at = ab_t + Inches(0.38) + i * Inches(0.46)
        box(slide, RP_L + Inches(0.1), at, RP_W - Inches(0.2), Inches(0.4),
            fill=RGBColor(0x0C, 0x0E, 0x26), line_color=ACCENT_PURP, lw=0.4)
        txt(slide, variant, RP_L + Inches(0.18), at + Inches(0.04), Inches(1.6), Inches(0.3),
            size=9, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)
        txt(slide, desc, RP_L + Inches(1.82), at + Inches(0.04), RP_W - Inches(1.98), Inches(0.3),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "19", ACCENT_GOLD)
