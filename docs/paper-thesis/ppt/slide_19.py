"""
Slide 19 — Summary (Closing Slide)
=====================================
Crystallises: What is CMatrix, what it claims, what you are asking the supervisor for,
and a current status snapshot.
Matches presentation-final.pptx Slide 19.
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)

    # Chrome: cyan left + lime top + cyan bottom
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

    # ── Left column ───────────────────────────────────────────────────────────
    SUM_L, SUM_W = Inches(0.3), Inches(5.5)
    SUM_T = Inches(1.08)

    # What CMatrix Is
    box(slide, SUM_L, SUM_T, SUM_W, Inches(1.65),
        fill=RGBColor(0x04, 0x12, 0x22), line_color=ACCENT_CYAN, lw=1.6)
    txt(slide, "WHAT CMATRIX IS", SUM_L + Inches(0.12), SUM_T + Inches(0.06),
        SUM_W - Inches(0.2), Inches(0.22),
        size=10, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
    txt(slide,
        "A dual-graph-guided, LLM-orchestrated multi-agent framework for autonomous Vulnerability "
        "Assessment and Penetration Testing.  It maintains two strictly separated graph structures — "
        "the ASG (what the target is) and the APG (what can be done to it) — and uses both to "
        "plan, dispatch, validate, and formally terminate a complete VAPT engagement without human intervention.",
        SUM_L + Inches(0.14), SUM_T + Inches(0.34), SUM_W - Inches(0.24), Inches(1.26),
        size=10.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Current Status
    STATUS_T = SUM_T + Inches(1.78)
    box(slide, SUM_L, STATUS_T, SUM_W, Inches(4.49),
        fill=RGBColor(0x04, 0x18, 0x0C), line_color=ACCENT_LIME, lw=1.4)
    txt(slide, "CURRENT STATUS", SUM_L + Inches(0.12), STATUS_T + Inches(0.06),
        SUM_W - Inches(0.2), Inches(0.22),
        size=10, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
    txt(slide,
        "We are currently in the architecture proposal phase, prior to implementation.",
        SUM_L + Inches(0.14), STATUS_T + Inches(0.34), SUM_W - Inches(0.24), Inches(0.32),
        size=10.5, bold=True, color=WHITE, align=PP_ALIGN.LEFT, wrap=True)

    status_bullets = [
        "→  All 12 contributions are fully specified at the architecture level - no implementation has begun.",
        "→  Some contributions are more load-bearing than others - prioritization hasn't been finalized.",
        "→  HTB/THM evaluation plan is outlined but not yet run.",
        "→  This meeting is seeking scope and direction sign-off before implementation work starts.",
    ]
    for i, bullet in enumerate(status_bullets):
        txt(slide, bullet,
            SUM_L + Inches(0.14), STATUS_T + Inches(0.74) + i * Inches(0.38),
            SUM_W - Inches(0.24), Inches(0.34),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # Stat boxes
    stat_t = STATUS_T + Inches(3.22)
    for j, (num, label, clr) in enumerate([
        ("12 / 12", "Contributions specified", ACCENT_LIME),
        ("0 / 12",  "Contributions implemented", RGBColor(0x8A, 0x8A, 0x8A)),
    ]):
        sl = SUM_L + Inches(0.14) + j * Inches(2.62)
        box(slide, sl, stat_t, Inches(2.55), Inches(1.2),
            fill=RGBColor(0x06, 0x22, 0x10) if j == 0 else RGBColor(0x14, 0x14, 0x14),
            line_color=clr, lw=1.0)
        txt(slide, num, sl + Inches(0.1), stat_t + Inches(0.06),
            Inches(2.35), Inches(0.6),
            size=32, bold=True, color=clr, align=PP_ALIGN.CENTER)
        txt(slide, label, sl + Inches(0.1), stat_t + Inches(0.72),
            Inches(2.35), Inches(0.3),
            size=9, color=GREY_MID, align=PP_ALIGN.CENTER)

    # ── Right column: Claims + What We Need ──────────────────────────────────
    RP_L = SUM_L + SUM_W + Inches(0.22)
    RP_W = SLIDE_W - RP_L - Inches(0.22)
    RP_T = SUM_T

    # What We Claim
    box(slide, RP_L, RP_T, RP_W, Inches(3.04),
        fill=RGBColor(0x16, 0x12, 0x02), line_color=ACCENT_GOLD, lw=1.4)
    txt(slide, "WHAT WE CLAIM", RP_L + Inches(0.12), RP_T + Inches(0.06),
        RP_W - Inches(0.2), Inches(0.22),
        size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    claims = [
        ("→  CMatrix is the first autonomous VAPT system to maintain two strictly separated, \n"
         "      continuously evolving graph structures for simultaneous discovery and attack reasoning."),
        "→  Formal dual termination provides a theoretically sound, verifiable completion criterion that prior systems cannot express.",
        ("→  Cross-mission learning accumulates validated exploitation outcomes across all missions — \n"
         "      a capability no prior published VAPT system demonstrates."),
        "→  The architecture produces a machine-readable decision trace usable for training security-specialized LLMs.",
    ]
    for i, claim in enumerate(claims):
        ct = RP_T + Inches(0.34) + i * Inches(0.64)
        box(slide, RP_L + Inches(0.1), ct, RP_W - Inches(0.2), Inches(0.58),
            fill=RGBColor(0x1E, 0x16, 0x02), line_color=ACCENT_GOLD, lw=0.5)
        txt(slide, claim, RP_L + Inches(0.18), ct + Inches(0.04),
            RP_W - Inches(0.3), Inches(0.5),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # What We Are Asking For
    wn_t = RP_T + Inches(3.16)
    box(slide, RP_L, wn_t, RP_W, Inches(3.1),
        fill=RGBColor(0x04, 0x14, 0x10), line_color=ACCENT_CYAN, lw=1.6)
    box(slide, RP_L, wn_t, RP_W, Inches(0.32), fill=RGBColor(0x0A, 0x0D, 0x1A))
    txt(slide, "WHAT WE ARE ASKING FOR", RP_L + Inches(0.12), wn_t + Inches(0.04),
        RP_W - Inches(0.2), Inches(0.26),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    asks = [
        ("Feedback on Scope",
         "Are the 12 contributions appropriately scoped for our thesis?"),
        ("Evaluation Guidance",
         "Is the HTB/THM ablation plan sufficient to prove the core claims?"),
        ("Implementation Priority",
         "Which of the 12 contributions should be fully implemented vs theoretically validated?"),
        ("Publication Venue",
         "USENIX Security / IEEE S&P / ACSAC — which tier matches the contribution level?"),
    ]
    for i, (heading, question) in enumerate(asks):
        at = wn_t + Inches(0.38) + i * Inches(0.68)
        box(slide, RP_L + Inches(0.1), at, RP_W - Inches(0.2), Inches(0.62),
            fill=RGBColor(0x06, 0x1C, 0x16), line_color=ACCENT_CYAN, lw=0.6)
        txt(slide, heading, RP_L + Inches(0.2), at + Inches(0.04),
            RP_W - Inches(0.32), Inches(0.22),
            size=10, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
        txt(slide, question, RP_L + Inches(0.2), at + Inches(0.28),
            RP_W - Inches(0.32), Inches(0.3),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "19", ACCENT_CYAN)
