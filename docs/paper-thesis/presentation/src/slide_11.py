"""
Slide 11 — Autonomous Planning Cycle
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_GOLD)

    slide_header(slide, "AUTONOMOUS PLANNING CYCLE",
                 "Commander Loop \u2014 Graph-Grounded, Event-Driven, Self-Terminating",
                 ACCENT_GOLD, title_size=26)
    slide_number(slide, "11", ACCENT_GOLD)

    # ── LEFT: Planning Loop Diagram ───────────────────────────────────────────
    DL = Inches(0.3)
    DW = Inches(8.55)
    DT = Inches(1.0)
    DH = SLIDE_H - DT - Inches(0.18)

    box(slide, DL, DT, DW, DH, fill=RGBColor(0x06, 0x06, 0x14), line_color=GREY_DARK, lw=0.8)

    txt(slide, "Core Planning Loop \u2014 Commander runs this every iteration",
        DL + Inches(0.14), DT + Inches(0.08), DW - Inches(0.3), Inches(0.24),
        size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    def fnode(label, x, y, w=Inches(1.6), h=Inches(0.44), fill=CARD_BG, color=WHITE, size=8.5):
        box(slide, x, y, w, h, fill=fill, line_color=GREY_DARK, lw=0.7)
        txt(slide, label, x + Inches(0.04), y + Inches(0.04), w - Inches(0.08), h - Inches(0.08),
            size=size, color=color, align=PP_ALIGN.CENTER, wrap=True)

    # Mission Start
    ms_x = DL + Inches(3.0)
    ms_t = DT + Inches(0.4)
    box(slide, ms_x, ms_t, Inches(2.55), Inches(0.38), fill=ACCENT_GOLD)
    txt(slide, "\U0001f680  MISSION START", ms_x, ms_t + Inches(0.04), Inches(2.55), Inches(0.30),
        size=13, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    # OBSERVE ASG + APG
    obs_t = ms_t + Inches(0.58)
    obs_x_l = DL + Inches(0.55)
    obs_x_r = DL + Inches(4.35)
    fnode("\U0001f7e0 OBSERVE ASG\nUnexplored nodes? New Vulns?\nNew Technology nodes?",
          obs_x_l, obs_t, Inches(2.5), Inches(0.58), fill=RGBColor(0x16, 0x12, 0x00))
    fnode("\U0001f7e0 OBSERVE APG\nHypothesized chains?\nVALIDATED / RULED_OUT?",
          obs_x_r, obs_t, Inches(2.5), Inches(0.58), fill=RGBColor(0x10, 0x10, 0x00))

    # no — continue label
    txt(slide, "no \u2014 continue",
        DL + DW - Inches(1.5), obs_t + Inches(0.15), Inches(1.4), Inches(0.22),
        size=8, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # REASON
    reason_t = obs_t + Inches(0.78)
    reason_x = DL + Inches(2.05)
    fnode("\U0001f535 REASON\nGiven ASG + APG state:\nWhat is the best next action?",
          reason_x, reason_t, Inches(2.55), Inches(0.58), fill=RGBColor(0x00, 0x10, 0x28))

    # DECIDE
    dec_t = reason_t + Inches(0.76)
    dec_x = DL + Inches(2.35)
    box(slide, dec_x, dec_t, Inches(1.85), Inches(0.40), fill=ACCENT_GOLD)
    txt(slide, "DECIDE", dec_x, dec_t + Inches(0.04), Inches(1.85), Inches(0.32),
        size=13, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    # ASG gaps / both / APG chains labels
    txt(slide, "ASG gaps", DL + Inches(1.0), dec_t + Inches(0.12), Inches(1.0), Inches(0.22),
        size=8, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)
    txt(slide, "both", DL + Inches(2.85), dec_t + Inches(0.44), Inches(0.8), Inches(0.22),
        size=8, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)
    txt(slide, "APG chains", DL + Inches(4.35), dec_t + Inches(0.12), Inches(1.1), Inches(0.22),
        size=8, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # Branch actions
    br_t = dec_t + Inches(0.64)
    fnode("\U0001f50d EXPLORE\nSpawn Discovery\nAgent",
          DL + Inches(0.3), br_t, Inches(1.5), Inches(0.58),
          fill=RGBColor(0x06, 0x18, 0x06), color=ACCENT_LIME)
    fnode("\u26a1 PARALLEL\nWeigh priority\nboth paths",
          DL + Inches(2.05), br_t, Inches(1.55), Inches(0.58),
          fill=RGBColor(0x16, 0x14, 0x00), color=ACCENT_GOLD)
    fnode("\U0001f534 VALIDATE\nSpawn Validation\nAgent",
          DL + Inches(3.75), br_t, Inches(1.55), Inches(0.58),
          fill=RGBColor(0x20, 0x06, 0x06), color=ACCENT_RED)
    fnode("\U0001f6e1\ufe0f CYCLE GUARD\nRepeated calls?\nFixation detected?",
          DL + Inches(5.4), br_t, Inches(1.7), Inches(0.58),
          fill=RGBColor(0x10, 0x08, 0x26), color=ACCENT_PURP)

    # Guard / normal labels
    txt(slide, "guard", DL + Inches(5.2), br_t + Inches(0.26), Inches(0.7), Inches(0.22),
        size=7.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)
    txt(slide, "normal", DL + Inches(3.5), br_t + Inches(0.26), Inches(0.8), Inches(0.22),
        size=7.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)
    txt(slide, "REFLECTOR or\nFORCE RE-PLAN",
        DL + Inches(6.4), br_t + Inches(0.14), Inches(1.8), Inches(0.32),
        size=8, italic=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)

    # AGENT EXECUTES
    ae_t = br_t + Inches(0.76)
    fnode("\u26a1 AGENT EXECUTES\nTools \u2192 Risk Gate \u2192 ASG writes",
          DL + Inches(1.35), ae_t, Inches(3.6), Inches(0.42),
          fill=RGBColor(0x10, 0x0A, 0x00), color=ACCENT_GOLD)

    # UPDATE ASG / APG / TERM CHECK
    upd_t = ae_t + Inches(0.56)
    fnode("\U0001f464 UPDATE ASG\nNew nodes + edges\nfrom returning agent",
          DL + Inches(0.18), upd_t, Inches(1.8), Inches(0.56),
          fill=RGBColor(0x04, 0x16, 0x04), color=ACCENT_LIME)
    fnode("\U0001f464 UPDATE APG\nChain status changed?\nRe-prioritize queue",
          DL + Inches(2.2), upd_t, Inches(1.8), Inches(0.56),
          fill=RGBColor(0x14, 0x10, 0x00), color=ACCENT_GOLD)
    fnode("\u2705 TERM CHECK\nASG exhausted?\nAND APG resolved?",
          DL + Inches(4.22), upd_t, Inches(1.9), Inches(0.56),
          fill=RGBColor(0x04, 0x18, 0x14), color=WHITE)

    # yes — both true
    txt(slide, "yes \u2014 both true", DL + Inches(4.5), upd_t + Inches(0.58), Inches(1.5), Inches(0.22),
        size=8, italic=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # Mission complete
    mc_t = upd_t + Inches(0.82)
    box(slide, DL + Inches(5.6), mc_t, Inches(2.6), Inches(0.48), fill=RGBColor(0x04, 0x20, 0x10),
        line_color=ACCENT_LIME, lw=1.0)
    txt(slide, "\U0001f4dd Mission\ncomplete \u2014\nspawn report",
        DL + Inches(5.7), mc_t + Inches(0.04), Inches(2.4), Inches(0.40),
        size=8.5, bold=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)

    # Bottom footnote
    fn_t = DT + DH - Inches(0.28)
    txt(slide, "Every Commander decision traces to a graph event.  Every re-plan is triggered by a node write.  "
        "Mission ends only when the graph demands it \u2014 not when a timer fires.",
        DL + Inches(0.12), fn_t, DW - Inches(0.24), Inches(0.24),
        size=8, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # ── RIGHT PANEL: Triggers ─────────────────────────────────────────────────
    R = Inches(9.0)
    RW = SLIDE_W - R - Inches(0.15)

    box(slide, R, DT, RW, DH, fill=RGBColor(0x06, 0x08, 0x18), line_color=GREY_DARK, lw=0.8)
    txt(slide, "What Triggers a Re-Plan", R + Inches(0.12), DT + Inches(0.08),
        RW - Inches(0.2), Inches(0.26), size=11, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # ASG Triggers
    asg_t = DT + Inches(0.4)
    box(slide, R + Inches(0.08), asg_t, RW - Inches(0.16), Inches(0.26),
        fill=RGBColor(0x06, 0x16, 0x06))
    txt(slide, "ASG Trigger Events", R + Inches(0.14), asg_t + Inches(0.04),
        RW - Inches(0.26), Inches(0.18), size=9, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    asg_triggers = [
        "\U0001f7e9 New Vulnerability node \u2192 seed APG chain?",
        "\U0001f7e9 New Technology node \u2192 spawn Research Agent",
        "\U0001f7e9 New Endpoint node \u2192 probe with Analysis Agent",
    ]
    for k, line in enumerate(asg_triggers):
        tt = asg_t + Inches(0.30) + k * Inches(0.28)
        box(slide, R + Inches(0.08), tt, RW - Inches(0.16), Inches(0.24),
            fill=RGBColor(0x04, 0x0C, 0x04), line_color=GREY_DARK, lw=0.4)
        txt(slide, line, R + Inches(0.14), tt + Inches(0.03), RW - Inches(0.26), Inches(0.18),
            size=8, color=WHITE, align=PP_ALIGN.LEFT)

    # APG Triggers
    apg_t = asg_t + Inches(1.18)
    box(slide, R + Inches(0.08), apg_t, RW - Inches(0.16), Inches(0.26),
        fill=RGBColor(0x18, 0x14, 0x00))
    txt(slide, "APG Trigger Events", R + Inches(0.14), apg_t + Inches(0.04),
        RW - Inches(0.26), Inches(0.18), size=9, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    apg_triggers = [
        ("\u2611 Chain \u2192 PARTIALLY_VALIDATED \u2192 re-rank all", ACCENT_GOLD),
        ("\u2705 Chain \u2192 VALIDATED \u2192 pursue next chain", ACCENT_LIME),
        ("\u274c Chain \u2192 RULED_OUT \u2192 remove, re-prioritize", ACCENT_RED),
    ]
    for k, (line, color) in enumerate(apg_triggers):
        tt = apg_t + Inches(0.30) + k * Inches(0.28)
        box(slide, R + Inches(0.08), tt, RW - Inches(0.16), Inches(0.24),
            fill=RGBColor(0x0C, 0x08, 0x00), line_color=GREY_DARK, lw=0.4)
        txt(slide, line, R + Inches(0.14), tt + Inches(0.03), RW - Inches(0.26), Inches(0.18),
            size=8, color=color, align=PP_ALIGN.LEFT)

    # Cycle Guard
    cg_t = apg_t + Inches(1.18)
    box(slide, R + Inches(0.08), cg_t, RW - Inches(0.16), Inches(0.26),
        fill=RGBColor(0x14, 0x08, 0x26))
    txt(slide, "Cycle Guard Events", R + Inches(0.14), cg_t + Inches(0.04),
        RW - Inches(0.26), Inches(0.18), size=9, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)

    cg_triggers = [
        "\U0001f501 Same tool call repeated \u00d73 \u2192 Force re-plan",
        "\U0001f4a5 Repeated different failures \u2192 Reflector",
    ]
    for k, line in enumerate(cg_triggers):
        tt = cg_t + Inches(0.30) + k * Inches(0.28)
        box(slide, R + Inches(0.08), tt, RW - Inches(0.16), Inches(0.24),
            fill=RGBColor(0x0A, 0x04, 0x18), line_color=GREY_DARK, lw=0.4)
        txt(slide, line, R + Inches(0.14), tt + Inches(0.03), RW - Inches(0.26), Inches(0.18),
            size=8, color=WHITE, align=PP_ALIGN.LEFT)

    # Dual Termination
    dt_t = cg_t + Inches(0.88)
    box(slide, R + Inches(0.08), dt_t, RW - Inches(0.16), Inches(0.26),
        fill=RGBColor(0x04, 0x16, 0x10))
    txt(slide, "Dual Termination Condition", R + Inches(0.14), dt_t + Inches(0.04),
        RW - Inches(0.26), Inches(0.18), size=9, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # ASG / APG boxes side by side
    half = (RW - Inches(0.28)) / 2
    asg_box_t = dt_t + Inches(0.32)
    box(slide, R + Inches(0.08), asg_box_t, half, Inches(0.82),
        fill=RGBColor(0x04, 0x14, 0x04), line_color=ACCENT_LIME, lw=0.8)
    txt(slide, "\u2705 ASG Exhausted\nEvery node investigated\nby appropriate agent",
        R + Inches(0.12), asg_box_t + Inches(0.06), half - Inches(0.08), Inches(0.72),
        size=8, color=WHITE, align=PP_ALIGN.CENTER, wrap=True)
    box(slide, R + Inches(0.08) + half + Inches(0.06), asg_box_t, half, Inches(0.82),
        fill=RGBColor(0x04, 0x14, 0x04), line_color=ACCENT_LIME, lw=0.8)
    txt(slide, "\u2705 APG Resolved\nAll chains VALIDATED\nor RULED_OUT",
        R + Inches(0.08) + half + Inches(0.1), asg_box_t + Inches(0.06), half - Inches(0.08), Inches(0.72),
        size=8, color=WHITE, align=PP_ALIGN.CENTER, wrap=True)
    # AND label
    txt(slide, "A\nN\nD", R + Inches(0.08) + half - Inches(0.08), asg_box_t + Inches(0.22),
        Inches(0.22), Inches(0.44), size=9, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.CENTER)

    both_t = asg_box_t + Inches(0.88)
    box(slide, R + Inches(0.08), both_t, RW - Inches(0.16), Inches(0.34),
        fill=RGBColor(0x04, 0x22, 0x10), line_color=ACCENT_LIME, lw=1.0)
    txt(slide, "\u2705 BOTH TRUE \u2192 Report Agent spawned \u2192 MISSION COMPLETE",
        R + Inches(0.14), both_t + Inches(0.06), RW - Inches(0.26), Inches(0.24),
        size=9, bold=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)

    txt(slide, "\u26a0\ufe0f Timer-based systems stop mid-chain.  CMatrix requires dual-graph resolution.",
        R + Inches(0.08), both_t + Inches(0.4), RW - Inches(0.16), Inches(0.26),
        size=8, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT, wrap=True)
