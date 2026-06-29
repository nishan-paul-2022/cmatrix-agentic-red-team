"""
Slide 5 — System Architecture
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_CYAN)

    slide_header(slide, "SYSTEM ARCHITECTURE", "CMatrix \u2014 Three-Tier Architecture Overview",
                 ACCENT_CYAN, title_size=30)
    slide_number(slide, "05", ACCENT_CYAN)

    # ── TIER 1: ORCHESTRATION ─────────────────────────────────────────────────
    T1_T = Inches(1.0)
    T1_H = Inches(1.6)
    FULL_W = SLIDE_W - Inches(0.6)

    box(slide, Inches(0.3), T1_T, FULL_W, T1_H, fill=RGBColor(0x06, 0x0E, 0x22),
        line_color=ACCENT_CYAN, lw=1.0)
    txt(slide, "\u2460 ORCHESTRATION", Inches(0.42), T1_T + Inches(0.06),
        Inches(3), Inches(0.22), size=9, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    # Operator box
    op_l, op_w = Inches(0.42), Inches(2.1)
    box(slide, op_l, T1_T + Inches(0.28), op_w, Inches(1.18), fill=GREY_DARK, line_color=GREY_MID, lw=0.8)
    txt(slide, "OPERATOR", op_l, T1_T + Inches(0.38), op_w, Inches(0.25),
        size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, "Target \u00b7 Scope \u00b7 Mode", op_l, T1_T + Inches(0.65), op_w, Inches(0.30),
        size=9.5, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)

    # mission config arrow label
    txt(slide, "mission config", Inches(2.65), T1_T + Inches(0.78), Inches(1.2), Inches(0.22),
        size=8, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)
    arr(slide, Inches(2.52), T1_T + Inches(0.88), Inches(2.72), T1_T + Inches(0.88),
        color=GREY_MID, lw=1.2)

    # Commander Agent box
    cmd_l, cmd_w = Inches(2.72), Inches(3.85)
    box(slide, cmd_l, T1_T + Inches(0.28), cmd_w, Inches(1.18),
        fill=RGBColor(0x00, 0x28, 0x38), line_color=ACCENT_CYAN, lw=1.5)
    txt(slide, "COMMANDER AGENT", cmd_l, T1_T + Inches(0.34), cmd_w, Inches(0.26),
        size=11, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.CENTER)
    cmd_bullets = [
        "\u2022 Reads ASG + APG state",
        "\u2022 Plans & delegates tasks",
        "\u2022 Seeds APG AttackChains from Vulnerability nodes",
        "\u2022 Approves High-risk ops",
        "\u2022 Writes to APG only",
    ]
    for j, line in enumerate(cmd_bullets):
        txt(slide, line, cmd_l + Inches(0.12), T1_T + Inches(0.6) + j * Inches(0.16),
            cmd_w - Inches(0.2), Inches(0.18), size=8.5, color=WHITE, align=PP_ALIGN.LEFT)

    # VAPT Protocol Prompt box
    vp_l, vp_w = Inches(6.77), Inches(6.28)
    box(slide, vp_l, T1_T + Inches(0.28), vp_w, Inches(1.18),
        fill=RGBColor(0x0A, 0x10, 0x2C), line_color=ACCENT_PURP, lw=1.0)
    txt(slide, "VAPT PROTOCOL PROMPT", vp_l, T1_T + Inches(0.34), vp_w, Inches(0.24),
        size=10, bold=True, color=ACCENT_PURP, align=PP_ALIGN.CENTER)
    txt(slide, "Phase rules \u00b7 Re-plan triggers \u00b7 Termination conditions \u00b7 Methodology-as-config (C7)",
        vp_l + Inches(0.12), T1_T + Inches(0.65), vp_w - Inches(0.22), Inches(0.55),
        size=9.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # ── TIER 2: DUAL-GRAPH WORLD MODEL ────────────────────────────────────────
    T2_T = T1_T + T1_H + Inches(0.12)
    T2_H = Inches(1.85)
    box(slide, Inches(0.3), T2_T, FULL_W, T2_H, fill=RGBColor(0x04, 0x10, 0x04),
        line_color=ACCENT_LIME, lw=1.0)
    txt(slide, "\u2461 DUAL-GRAPH WORLD MODEL", Inches(0.42), T2_T + Inches(0.06),
        Inches(4), Inches(0.22), size=9, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # ASG box
    asg_l, asg_w = Inches(0.42), Inches(6.05)
    box(slide, asg_l, T2_T + Inches(0.28), asg_w, Inches(1.48),
        fill=RGBColor(0x06, 0x1A, 0x06), line_color=ACCENT_LIME, lw=1.0)
    txt(slide, "ATTACK SURFACE GRAPH  (ASG)", asg_l, T2_T + Inches(0.33), asg_w, Inches(0.26),
        size=10, bold=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)

    asg_nodes = ["Domain", "Host", "Port", "Service", "Technology"]
    asg_nodes2 = ["Endpoint", "Parameter", "Vulnerability", "Evidence"]
    nw = Inches(1.08)
    ngap = Inches(0.06)
    for j, n in enumerate(asg_nodes):
        nl = asg_l + Inches(0.08) + j * (nw + ngap)
        box(slide, nl, T2_T + Inches(0.62), nw, Inches(0.28), fill=ACCENT_LIME)
        txt(slide, n, nl, T2_T + Inches(0.64), nw, Inches(0.24),
            size=8.5, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    nw2 = Inches(1.2)
    for j, n in enumerate(asg_nodes2):
        nl = asg_l + Inches(0.08) + j * (nw2 + ngap)
        box(slide, nl, T2_T + Inches(0.96), nw2, Inches(0.28), fill=ACCENT_LIME)
        txt(slide, n, nl, T2_T + Inches(0.98), nw2, Inches(0.24),
            size=8.5, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    txt(slide, "Discovered Reality \u2014 confirmed facts only. Never contains hypotheses.",
        asg_l + Inches(0.08), T2_T + Inches(1.3), asg_w - Inches(0.15), Inches(0.22),
        size=8.5, italic=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # STRICT SEPARATION label
    sep_l = Inches(6.6)
    txt(slide, "STRICT\nSEPARATION", sep_l, T2_T + Inches(0.7), Inches(0.8), Inches(0.6),
        size=7.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # APG box
    apg_l, apg_w = Inches(7.6), Inches(5.45)
    box(slide, apg_l, T2_T + Inches(0.28), apg_w, Inches(1.48),
        fill=RGBColor(0x1A, 0x14, 0x00), line_color=ACCENT_GOLD, lw=1.0)
    txt(slide, "ATTACK PATH GRAPH  (APG)", apg_l, T2_T + Inches(0.33), apg_w, Inches(0.26),
        size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.CENTER)

    apg_nodes = ["AttackChain", "ChainStep", "Impact"]
    anw = Inches(1.55)
    for j, n in enumerate(apg_nodes):
        nl = apg_l + Inches(0.1) + j * (anw + Inches(0.08))
        box(slide, nl, T2_T + Inches(0.62), anw, Inches(0.28), fill=ACCENT_GOLD)
        txt(slide, n, nl, T2_T + Inches(0.64), anw, Inches(0.24),
            size=8.5, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    txt(slide, "risk_score  \u00b7  validation_status  \u00b7  priority",
        apg_l + Inches(0.1), T2_T + Inches(0.97), apg_w - Inches(0.18), Inches(0.22),
        size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT)
    txt(slide, "Inferred Opportunity \u2014 attack reasoning only. Never contains raw scan data.",
        apg_l + Inches(0.1), T2_T + Inches(1.2), apg_w - Inches(0.18), Inches(0.22),
        size=8.5, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    # ── TIER 3: SPECIALIZED AGENTS ────────────────────────────────────────────
    T3_T = T2_T + T2_H + Inches(0.12)
    T3_H = SLIDE_H - T3_T - Inches(0.18)
    box(slide, Inches(0.3), T3_T, FULL_W, T3_H, fill=RGBColor(0x04, 0x04, 0x10),
        line_color=ACCENT_PURP, lw=1.0)
    txt(slide, "\u2462 SPECIALIZED AGENTS  +  TOOL ADAPTER LAYER", Inches(0.42), T3_T + Inches(0.05),
        Inches(6), Inches(0.22), size=9, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)

    agents = [
        ("Recon", ACCENT_LIME, "\u00b7 Amass \n\u00b7 httpx \n\u00b7 Nmap"),
        ("Analysis", ACCENT_CYAN, "\u00b7 WhatWeb\n \u00b7 Gobuster \n\u00b7 ffuf \n\u00b7 Nuclei\n \u00b7 ZAP"),
        ("Research", ACCENT_GOLD, "\u00b7 NVD\n\u00b7 Exploit-DB \n\u00b7 GitHub"),
        ("Validation", ACCENT_RED, "\u00b7 SQLMap\n \u00b7 Metasploit"),
        ("Evidence", ACCENT_PURP, "EyeWitness"),
        ("Report", GREY_MID, "Reads ASG + APG"),
    ]

    ag_w = Inches(1.5)
    ag_gap = Inches(0.06)
    ag_t = T3_T + Inches(0.28)
    ag_h = T3_H - Inches(0.34)

    for j, (name, color, tools) in enumerate(agents):
        al = Inches(0.42) + j * (ag_w + ag_gap)
        box(slide, al, ag_t, ag_w, ag_h, fill=RGBColor(0x08, 0x10, 0x20),
            line_color=color, lw=1.0)
        box(slide, al, ag_t, ag_w, Inches(0.26), fill=color)
        txt(slide, name, al, ag_t + Inches(0.02), ag_w, Inches(0.22),
            size=10, bold=True, color=BG_DARK if color != GREY_MID else WHITE, align=PP_ALIGN.CENTER)
        txt(slide, tools, al + Inches(0.08), ag_t + Inches(0.30), ag_w - Inches(0.14), ag_h - Inches(0.35),
            size=8.5, color=color, align=PP_ALIGN.LEFT, wrap=True)

    # TOOL ADAPTER LAYER panel
    tal_l = Inches(0.42) + 6 * (ag_w + ag_gap)
    tal_w = SLIDE_W - Inches(0.6) - tal_l + Inches(0.3)
    box(slide, tal_l, ag_t, tal_w, ag_h, fill=RGBColor(0x10, 0x08, 0x24),
        line_color=ACCENT_PURP, lw=1.0)
    txt(slide, "TOOL ADAPTER LAYER", tal_l, ag_t + Inches(0.04), tal_w, Inches(0.24),
        size=9.5, bold=True, color=ACCENT_PURP, align=PP_ALIGN.CENTER)

    tiers = [
        ("LOW", ACCENT_LIME, "Passive", "Execute immediately"),
        ("MED", ACCENT_GOLD, "Active", "LLM Classifier \u2192 exec/escalate"),
        ("HIGH", ACCENT_RED, "Exploit", "Commander Mailbox approval"),
    ]
    tier_h = Inches(0.72)
    tier_gap = Inches(0.06)
    for k, (label, color, sublabel, desc) in enumerate(tiers):
        tt = ag_t + Inches(0.32) + k * (tier_h + tier_gap)
        # Badge
        box(slide, tal_l + Inches(0.08), tt, Inches(0.52), tier_h, fill=color)
        txt(slide, label, tal_l + Inches(0.08), tt + Inches(0.22), Inches(0.52), Inches(0.28),
            size=9, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
        # Desc panel
        box(slide, tal_l + Inches(0.65), tt, tal_w - Inches(0.75), tier_h,
            fill=RGBColor(0x08, 0x06, 0x18), line_color=color, lw=0.7)
        txt(slide, sublabel, tal_l + Inches(0.72), tt + Inches(0.06),
            tal_w - Inches(0.85), Inches(0.22), size=9.5, bold=True, color=color, align=PP_ALIGN.LEFT)
        txt(slide, desc, tal_l + Inches(0.72), tt + Inches(0.3),
            tal_w - Inches(0.85), Inches(0.36), size=8.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)
