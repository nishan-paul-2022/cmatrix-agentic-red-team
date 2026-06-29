"""
Slide 7 — Agent Architecture
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_PURP)

    slide_header(slide, "AGENT ARCHITECTURE",
                 "Context-Isolated Agents \u2014 Spawn \u00b7 Execute \u00b7 Return \u00b7 Discard",
                 ACCENT_PURP, title_size=28)
    slide_number(slide, "07", ACCENT_PURP)

    # ── LEFT: Context Isolation Model ─────────────────────────────────────────
    L, LW = Inches(0.3), Inches(5.05)
    LT = Inches(1.0)
    LH = Inches(6.28)

    box(slide, L, LT, LW, LH, fill=RGBColor(0x08, 0x06, 0x18), line_color=ACCENT_PURP, lw=1.0)
    txt(slide, "CONTEXT ISOLATION MODEL", L, LT + Inches(0.08), LW, Inches(0.24),
        size=10, bold=True, color=ACCENT_PURP, align=PP_ALIGN.CENTER)

    # Commander Agent
    box(slide, L + Inches(0.15), LT + Inches(0.36), LW - Inches(0.3), Inches(0.28),
        fill=ACCENT_CYAN)
    txt(slide, "COMMANDER AGENT", L + Inches(0.15), LT + Inches(0.37), LW - Inches(0.3), Inches(0.24),
        size=9.5, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    box(slide, L + Inches(0.15), LT + Inches(0.64), LW - Inches(0.3), Inches(0.28),
        fill=RGBColor(0x00, 0x24, 0x38), line_color=ACCENT_CYAN, lw=0.8)
    txt(slide, "Reads ASG + APG \u2192 decides next action",
        L + Inches(0.18), LT + Inches(0.66), LW - Inches(0.36), Inches(0.22),
        size=9, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

    txt(slide, "spawn with scoped context",
        L + Inches(0.15), LT + Inches(0.97), LW - Inches(0.3), Inches(0.18),
        size=8, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)
    arr(slide, L + LW/2, LT + Inches(1.12), L + LW/2, LT + Inches(1.3),
        color=GREY_MID, lw=1.0)

    # Isolated context box
    iso_t = LT + Inches(1.32)
    iso_h = Inches(3.3)
    box(slide, L + Inches(0.12), iso_t, LW - Inches(0.24), iso_h,
        fill=RGBColor(0x04, 0x04, 0x14), line_color=GREY_DARK, lw=0.8)
    txt(slide, "ISOLATED AGENT CONTEXT  (fresh per task)",
        L + Inches(0.18), iso_t + Inches(0.06), LW - Inches(0.36), Inches(0.22),
        size=8.5, bold=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    context_items = [
        ("ASG SLICE", ACCENT_LIME, "Only nodes relevant to this task"),
        ("APG SLICE", ACCENT_GOLD, "Relevant AttackChains (if any)"),
        ("TOOL SET", ACCENT_RED, "Authorized tools only \u2014 no others"),
        ("TASK SPEC", ACCENT_CYAN, "Commander's current plan item"),
    ]
    for k, (label, color, desc) in enumerate(context_items):
        ct = iso_t + Inches(0.34) + k * Inches(0.72)
        box(slide, L + Inches(0.18), ct, LW - Inches(0.36), Inches(0.6),
            fill=RGBColor(0x0A, 0x0A, 0x20), line_color=color, lw=0.8)
        txt(slide, label, L + Inches(0.24), ct + Inches(0.06), Inches(1.2), Inches(0.22),
            size=9, bold=True, color=color, align=PP_ALIGN.LEFT)
        txt(slide, desc, L + Inches(1.5), ct + Inches(0.06), LW - Inches(1.7), Inches(0.22),
            size=8.5, italic=True, color=WHITE, align=PP_ALIGN.LEFT)

    # Returns box
    ret_t = iso_t + iso_h + Inches(0.1)
    box(slide, L + Inches(0.12), ret_t, LW - Inches(0.24), Inches(0.62),
        fill=RGBColor(0x04, 0x14, 0x04), line_color=ACCENT_LIME, lw=1.0)
    txt(slide, "RETURNS: Structured ASG Delta (new nodes + edges only)",
        L + Inches(0.18), ret_t + Inches(0.06), LW - Inches(0.36), Inches(0.24),
        size=9.5, bold=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)
    txt(slide, "Working context discarded \u2014 no raw history passes to Commander",
        L + Inches(0.18), ret_t + Inches(0.3), LW - Inches(0.36), Inches(0.22),
        size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)

    # Benefit badges
    benefits = [
        ("\u2713 Commander context stays clean", ACCENT_LIME),
        ("\u2713 Agents can\u2019t contaminate each other", ACCENT_LIME),
        ("\u2713 High-risk refusals don\u2019t bias planning", ACCENT_RED),
    ]
    for k, (label, color) in enumerate(benefits):
        bt = ret_t + Inches(0.72) + k * Inches(0.36)
        box(slide, L + Inches(0.12), bt, LW - Inches(0.24), Inches(0.30),
            fill=RGBColor(0x06, 0x10, 0x06) if color == ACCENT_LIME else RGBColor(0x18, 0x06, 0x06),
            line_color=color, lw=0.7)
        txt(slide, label, L + Inches(0.2), bt + Inches(0.04), LW - Inches(0.38), Inches(0.22),
            size=9, color=color, align=PP_ALIGN.LEFT)

    # ── RIGHT: Agent Cards ────────────────────────────────────────────────────
    R = Inches(5.55)
    RW1 = Inches(3.8)
    RW2 = Inches(3.8)
    RSTART = R
    RCOL2 = R + RW1 + Inches(0.08)

    agent_cards = [
        # (col, row, title, accent, badge_text, badge_color, subtitle, tools, tools_bg, body)
        (0, 0, "Commander", ACCENT_GOLD, "ORCHESTRATION", ACCENT_CYAN,
         "Reads the dual graph. Plans. Delegates. Never runs tools.",
         "No tools \u2014 reasons over ASG + APG", RGBColor(0x00, 0x30, 0x30),
         "Only agent that writes to APG. Approves High-risk ops via mailbox."),
        (1, 0, "Recon", ACCENT_LIME, "PHASE 1", ACCENT_LIME,
         "External reconnaissance and host discovery.",
         "Amass \u00b7 httpx \u00b7 Nmap", RGBColor(0x00, 0x28, 0x08),
         "Writes Domain, Host, Port, Service nodes to ASG."),
        (0, 1, "Analysis", ACCENT_CYAN, "PHASE 2", ACCENT_CYAN,
         "Deep enumeration and vulnerability discovery.",
         "WhatWeb \u00b7 Gobuster \u00b7 ffuf \u00b7 Nuclei \u00b7 ZAP", RGBColor(0x00, 0x22, 0x30),
         "Writes Technology, Endpoint, Parameter, Vulnerability nodes."),
        (1, 1, "Research", ACCENT_GOLD, "INTELLIGENCE", ACCENT_GOLD,
         "Live CVE grounding \u2014 only agent with outbound internet access.",
         "NVD \u00b7 Exploit-DB \u00b7 GitHub \u00b7 Vendor Advisories", RGBColor(0x26, 0x18, 0x00),
         "Enriches ASG Vulnerability nodes with real-time CVSS + PoC data."),
        (0, 2, "Validation", ACCENT_RED, "PHASE 3", ACCENT_RED,
         "Proves vulnerabilities are real and exploitable.",
         "SQLMap \u00b7 Metasploit", RGBColor(0x28, 0x04, 0x04),
         "Self-debugging loop: Diagnose \u2192 Contextualize \u2192 Adapt \u2192 Cap (\u00d73)."),
        (1, 2, "Evidence", ACCENT_PURP, "PHASE 3", ACCENT_PURP,
         "Captures proof artifacts for every validated finding.",
         "EyeWitness", RGBColor(0x18, 0x0A, 0x28),
         "Links Evidence nodes to ASG findings via validated_by edges."),
    ]

    card_h = Inches(1.96)
    card_gap = Inches(0.09)

    for col, row, title, accent, badge, badge_bg, subtitle, tools, tools_bg, body in agent_cards:
        cx = RSTART + col * (RW1 + Inches(0.08))
        cy = Inches(1.0) + row * (card_h + card_gap)
        cw = RW1

        box(slide, cx, cy, cw, card_h, fill=RGBColor(0x08, 0x0C, 0x20), line_color=accent, lw=1.0)
        # Badge
        box(slide, cx + cw - Inches(1.4), cy + Inches(0.04), Inches(1.34), Inches(0.24),
            fill=badge_bg)
        txt(slide, badge, cx + cw - Inches(1.4), cy + Inches(0.06), Inches(1.34), Inches(0.20),
            size=7.5, bold=True, color=WHITE if badge_bg != ACCENT_LIME else BG_DARK, align=PP_ALIGN.CENTER)
        # Title
        txt(slide, f"\U0001f451 {title}" if title == "Commander" else title,
            cx + Inches(0.1), cy + Inches(0.06), cw - Inches(1.5), Inches(0.3),
            size=14, bold=True, color=accent, align=PP_ALIGN.LEFT)
        # Subtitle
        txt(slide, subtitle, cx + Inches(0.1), cy + Inches(0.38), cw - Inches(0.2), Inches(0.26),
            size=9, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)
        # Tools row
        box(slide, cx + Inches(0.08), cy + Inches(0.68), cw - Inches(0.16), Inches(0.24),
            fill=tools_bg)
        txt(slide, tools, cx + Inches(0.12), cy + Inches(0.70), cw - Inches(0.22), Inches(0.20),
            size=8.5, bold=True, color=accent, align=PP_ALIGN.LEFT)
        # Body
        txt(slide, body, cx + Inches(0.1), cy + Inches(0.98), cw - Inches(0.2), Inches(0.88),
            size=9, color=WHITE, align=PP_ALIGN.LEFT, wrap=True)
