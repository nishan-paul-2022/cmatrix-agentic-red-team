"""
Slide 15 — Real-World Scenario: shopvault.io Black-Box Assessment
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_GOLD)

    # ── Header ────────────────────────────────────────────────────────────────
    txt(slide, "REAL-WORLD SCENARIO",
        Inches(0.3), Inches(0.07), Inches(5.0), Inches(0.27),
        size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
    txt(slide, "Mission: shopvault.io — Black-Box Assessment — Zero Manual Commands",
        Inches(0.3), Inches(0.31), Inches(12.5), Inches(0.51),
        size=24, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # Scope banner
    box(slide, Inches(0.18), Inches(0.84), Inches(12.973), Inches(0.38),
        fill=RGBColor(0x10, 0x10, 0x04), line_color=ACCENT_GOLD, lw=0.8)
    txt(slide, "Scope: all subdomains · web applications · REST APIs of shopvault.io  ·  Mode: Black-Box (zero prior knowledge)  ·  Operator configures root domain + scope → presses start.",
        Inches(0.35), Inches(0.90), Inches(12.683), Inches(0.25),
        size=9.0, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    # ═══════════════════════════════════════════════════════
    # PHASE COLUMNS
    # ═══════════════════════════════════════════════════════
    PHASE_TOP = Inches(1.30)
    PHASE_H = Inches(5.48)
    HEADER_H = Inches(0.50)

    # ── PHASE 1: Reconnaissance ───────────────────────────
    P1_L = Inches(0.18)
    P1_W = Inches(2.62)
    box(slide, P1_L, PHASE_TOP, P1_W, PHASE_H,
        fill=RGBColor(0x04, 0x14, 0x08), line_color=ACCENT_LIME, lw=1.2)
    box(slide, P1_L, PHASE_TOP, P1_W, HEADER_H,
        fill=RGBColor(0x08, 0x10, 0x1C), line_color=ACCENT_LIME, lw=1.2)
    txt(slide, "PHASE 1\nReconnaissance",
        Inches(0.26), PHASE_TOP + Inches(0.06), Inches(2.50), Inches(0.44),
        size=10, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # Agent label
    txt(slide, "🕵️ Recon Agent",
        Inches(0.26), PHASE_TOP + Inches(0.58), Inches(2.50), Inches(0.24),
        size=8.5, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # Tools strip
    box(slide, Inches(0.26), PHASE_TOP + Inches(0.80), Inches(2.46), Inches(0.20),
        fill=RGBColor(0x08, 0x10, 0x22), line_color=ACCENT_LIME, lw=0.8)
    txt(slide, "Amass  ·  httpx  ·  Nmap",
        Inches(0.30), PHASE_TOP + Inches(0.81), Inches(2.42), Inches(0.22),
        size=7.0, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # Tool result blocks
    p1_tools = [
        ("Amass",  Inches(1.06), ["14 subdomains discovered", "api · admin · staging · pay · ..."]),
        ("httpx",  Inches(2.05), ["11 live hosts confirmed",  "staging returns unexpected 200"]),
        ("Nmap",   Inches(1.29), ["Ports 80, 443, 8080, 8443 open", "pay.shopvault.io: expired TLS"]),
    ]
    block_top = PHASE_TOP + Inches(1.06)
    for tool_name, block_h, body_lines in p1_tools:
        box(slide, Inches(0.26), block_top, Inches(2.46), block_h,
            fill=RGBColor(0x08, 0x0E, 0x1C), line_color=ACCENT_LIME, lw=0.8)
        # Left accent stripe
        box(slide, Inches(0.26), block_top, Inches(0.05), block_h, fill=ACCENT_LIME)
        txt(slide, tool_name,
            Inches(0.34), block_top + Inches(0.04), Inches(2.32), Inches(0.24),
            size=8.0, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
        for bi, line in enumerate(body_lines):
            txt(slide, line,
                Inches(0.34), block_top + Inches(0.26) + bi * Inches(0.22),
                Inches(2.32), Inches(0.22),
                size=8.0, color=GREY_MID, align=PP_ALIGN.LEFT)
        block_top += block_h + Inches(0.063)

    # ASG count footer
    box(slide, P1_L, PHASE_TOP + PHASE_H - Inches(0.44), P1_W, Inches(0.44),
        fill=RGBColor(0x06, 0x0C, 0x18), line_color=ACCENT_LIME, lw=0.8)
    txt(slide, "ASG ← 37 new nodes",
        Inches(0.28), PHASE_TOP + PHASE_H - Inches(0.38), Inches(2.47), Inches(0.24),
        size=8.5, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)

    # ── Phase arrow divider ───────────────────────────────
    arr(slide, Inches(2.80), PHASE_TOP + Inches(0.25), Inches(2.86), PHASE_TOP + Inches(0.25),
        color=ACCENT_CYAN, lw=1.8)

    # ── PHASE 2: Analysis + Intel ─────────────────────────
    P2_L = Inches(2.86)
    P2_W = Inches(3.80)
    box(slide, P2_L, PHASE_TOP, P2_W, PHASE_H,
        fill=RGBColor(0x04, 0x10, 0x18), line_color=ACCENT_CYAN, lw=1.2)
    box(slide, P2_L, PHASE_TOP, P2_W, HEADER_H,
        fill=RGBColor(0x08, 0x10, 0x1C), line_color=ACCENT_CYAN, lw=1.2)
    txt(slide, "PHASE 2\nAnalysis + Intel",
        Inches(2.94), PHASE_TOP + Inches(0.06), Inches(3.68), Inches(0.44),
        size=10, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    txt(slide, "🔬 Analysis + 🔍 Research",
        Inches(2.94), PHASE_TOP + Inches(0.58), Inches(3.68), Inches(0.24),
        size=8.5, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    box(slide, Inches(2.94), PHASE_TOP + Inches(0.80), Inches(3.64), Inches(0.20),
        fill=RGBColor(0x08, 0x10, 0x22), line_color=ACCENT_CYAN, lw=0.8)
    txt(slide, "WhatWeb  ·  Gobuster  ·  ffuf  ·  Nuclei  ·  ZAP",
        Inches(2.98), PHASE_TOP + Inches(0.81), Inches(3.60), Inches(0.22),
        size=7.0, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    p2_tools = [
        ("WhatWeb", Inches(0.91), ["WordPress 5.9.3 · Django API", "→ Research: CVE-2022-21661 (CVSS 8.8)"]),
        ("Gobuster", Inches(0.91), ["/backup/db_export_2023.sql EXPOSED", "/admin/users · /admin/login"]),
        ("ffuf",    Inches(0.91), ["IDOR: user_id param unsanitized",   "/api/v1/internal/users found"]),
        ("ZAP",     Inches(0.91), ["XSS on /search?q=",                 "SQL error on staging login"]),
    ]
    block_top = PHASE_TOP + Inches(1.06)
    for tool_name, block_h, body_lines in p2_tools:
        box(slide, Inches(2.94), block_top, Inches(3.64), block_h,
            fill=RGBColor(0x08, 0x0E, 0x1C), line_color=ACCENT_CYAN, lw=0.8)
        box(slide, Inches(2.94), block_top, Inches(0.05), block_h, fill=ACCENT_CYAN)
        txt(slide, tool_name,
            Inches(3.02), block_top + Inches(0.04), Inches(3.50), Inches(0.24),
            size=8.0, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
        for bi, line in enumerate(body_lines):
            txt(slide, line,
                Inches(3.02), block_top + Inches(0.26) + bi * Inches(0.22),
                Inches(3.50), Inches(0.22),
                size=8.0, color=GREY_MID, align=PP_ALIGN.LEFT)
        block_top += block_h + Inches(0.00)

    box(slide, P2_L, PHASE_TOP + PHASE_H - Inches(0.44), P2_W, Inches(0.44),
        fill=RGBColor(0x06, 0x0C, 0x18), line_color=ACCENT_CYAN, lw=0.8)
    txt(slide, "ASG ← 61 nodes",
        Inches(2.96), PHASE_TOP + PHASE_H - Inches(0.38), Inches(3.65), Inches(0.24),
        size=8.5, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
    txt(slide, "APG ← 3 chains seeded",
        Inches(2.96), PHASE_TOP + PHASE_H - Inches(0.17), Inches(3.65), Inches(0.20),
        size=8.5, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    # ── Phase arrow divider ───────────────────────────────
    arr(slide, Inches(6.66), PHASE_TOP + Inches(0.25), Inches(6.72), PHASE_TOP + Inches(0.25),
        color=ACCENT_RED, lw=1.8)

    # ── PHASE 3: Validation ───────────────────────────────
    P3_L = Inches(6.72)
    P3_W = Inches(3.98)
    box(slide, P3_L, PHASE_TOP, P3_W, PHASE_H,
        fill=RGBColor(0x18, 0x06, 0x06), line_color=ACCENT_RED, lw=1.2)
    box(slide, P3_L, PHASE_TOP, P3_W, HEADER_H,
        fill=RGBColor(0x08, 0x10, 0x1C), line_color=ACCENT_RED, lw=1.2)
    txt(slide, "PHASE 3\nValidation",
        Inches(6.80), PHASE_TOP + Inches(0.06), Inches(3.86), Inches(0.44),
        size=10, bold=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)

    txt(slide, "🎯 Validation + 📸 Evidence",
        Inches(6.80), PHASE_TOP + Inches(0.58), Inches(3.86), Inches(0.24),
        size=8.5, bold=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)

    box(slide, Inches(6.80), PHASE_TOP + Inches(0.80), Inches(3.82), Inches(0.20),
        fill=RGBColor(0x08, 0x10, 0x22), line_color=ACCENT_RED, lw=0.8)
    txt(slide, "SQLMap  ·  Metasploit  ·  EyeWitness",
        Inches(6.84), PHASE_TOP + Inches(0.81), Inches(3.78), Inches(0.22),
        size=7.0, bold=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)

    p3_chains = [
        ("Chain-01", "(risk 8.8)", Inches(0.935),
         ["SQLMap → SQLi confirmed", "Admin hash cracked → Metasploit → RCE", "Status: VALIDATED (escalated 9.1)"]),
        ("Chain-02", "(risk 7.5)", Inches(0.935),
         ["SQLMap on user_id → IDOR confirmed", "Any customer orders accessible"]),
        ("Chain-03", "(risk 8.1)", Inches(0.935),
         ["Blind SQLi on staging → DB creds", "Credential reuse risk flagged"]),
        ("Chain-04", "(validated instantly)", Inches(0.935),
         ["Direct GET on exposed DB backup file", "Misconfiguration → full PII exposure, no agent needed"]),
    ]
    block_top = PHASE_TOP + Inches(1.06)
    for chain_name, risk_label, block_h, body_lines in p3_chains:
        box(slide, Inches(6.80), block_top, Inches(3.82), block_h,
            fill=RGBColor(0x08, 0x0E, 0x1C), line_color=ACCENT_RED, lw=0.8)
        box(slide, Inches(6.80), block_top, Inches(0.05), block_h, fill=ACCENT_RED)
        txt(slide, chain_name,
            Inches(6.88), block_top + Inches(0.04), Inches(3.68), Inches(0.24),
            size=8.0, bold=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)
        txt(slide, risk_label,
            Inches(6.88), block_top + Inches(0.24), Inches(3.68), Inches(0.22),
            size=8.0, bold=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)
        for bi, line in enumerate(body_lines):
            txt(slide, line,
                Inches(6.88), block_top + Inches(0.44) + bi * Inches(0.22),
                Inches(3.68), Inches(0.22),
                size=8.0, color=GREY_MID, align=PP_ALIGN.LEFT)
        block_top += block_h + Inches(0.005)

    box(slide, P3_L, PHASE_TOP + PHASE_H - Inches(0.44), P3_W, Inches(0.44),
        fill=RGBColor(0x06, 0x0C, 0x18), line_color=ACCENT_RED, lw=0.8)
    txt(slide, "APG ← 4 chains VALIDATED",
        Inches(6.82), PHASE_TOP + PHASE_H - Inches(0.38), Inches(3.83), Inches(0.22),
        size=8.5, bold=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)
    txt(slide, "ASG ← Evidence nodes linked",
        Inches(6.82), PHASE_TOP + PHASE_H - Inches(0.17), Inches(3.83), Inches(0.20),
        size=8.5, bold=True, color=ACCENT_RED, align=PP_ALIGN.LEFT)

    # ── Phase arrow divider ───────────────────────────────
    arr(slide, Inches(10.70), PHASE_TOP + Inches(0.25), Inches(10.76), PHASE_TOP + Inches(0.25),
        color=ACCENT_PURP, lw=1.8)

    # ── PHASE 4: Report ───────────────────────────────────
    P4_L = Inches(10.76)
    P4_W = Inches(2.42)
    box(slide, P4_L, PHASE_TOP, P4_W, PHASE_H,
        fill=RGBColor(0x10, 0x08, 0x1C), line_color=ACCENT_PURP, lw=1.2)
    box(slide, P4_L, PHASE_TOP, P4_W, HEADER_H,
        fill=RGBColor(0x08, 0x10, 0x1C), line_color=ACCENT_PURP, lw=1.2)
    txt(slide, "PHASE 4\nReport",
        Inches(10.84), PHASE_TOP + Inches(0.06), Inches(2.32), Inches(0.44),
        size=10, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)

    txt(slide, "📝 Report Agent",
        Inches(10.84), PHASE_TOP + Inches(0.58), Inches(2.32), Inches(0.24),
        size=8.5, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)

    box(slide, Inches(10.84), PHASE_TOP + Inches(0.80), Inches(2.254), Inches(0.20),
        fill=RGBColor(0x08, 0x10, 0x22), line_color=ACCENT_PURP, lw=0.8)
    txt(slide, "Reads ASG + APG",
        Inches(10.88), PHASE_TOP + Inches(0.81), Inches(2.214), Inches(0.22),
        size=7.0, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)

    # Output block
    box(slide, Inches(10.84), PHASE_TOP + Inches(1.06), Inches(2.254), Inches(3.82),
        fill=RGBColor(0x08, 0x0E, 0x1C), line_color=ACCENT_PURP, lw=0.8)
    box(slide, Inches(10.84), PHASE_TOP + Inches(1.06), Inches(0.05), Inches(3.82), fill=ACCENT_PURP)
    txt(slide, "Output",
        Inches(10.92), PHASE_TOP + Inches(1.10), Inches(2.214), Inches(0.24),
        size=8.0, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)
    output_lines = [
        "Executive summary · 4 validated chains",
        "RCE + IDOR + SQLi + exposed DB backup",
        "11 vuln entries · full attack surface map",
        "Evidence at every ChainStep",
    ]
    for bi, line in enumerate(output_lines):
        txt(slide, line,
            Inches(10.92), PHASE_TOP + Inches(1.36) + bi * Inches(0.22),
            Inches(2.214), Inches(0.22),
            size=8.0, color=GREY_MID, align=PP_ALIGN.LEFT)

    # Footer note
    box(slide, P4_L, PHASE_TOP + PHASE_H - Inches(0.44), P4_W, Inches(0.44),
        fill=RGBColor(0x06, 0x0C, 0x18), line_color=ACCENT_PURP, lw=0.8)
    txt(slide, "ZERO manual commands",
        Inches(10.86), PHASE_TOP + PHASE_H - Inches(0.34), Inches(2.254), Inches(0.24),
        size=8.5, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)

    # ═══════════════════════════════════════════════════════
    # BOTTOM STATS BAR
    # ═══════════════════════════════════════════════════════
    STATS_TOP = Inches(6.78)
    box(slide, Inches(0.18), STATS_TOP, Inches(12.973), Inches(0.54),
        fill=RGBColor(0x08, 0x10, 0x22), line_color=ACCENT_CYAN, lw=1.2)

    stats = [
        ("14",   "subdomains",       ACCENT_LIME, Inches(0.22)),
        ("11",   "live hosts",       ACCENT_LIME, Inches(2.039)),
        ("28",   "open ports",       ACCENT_CYAN, Inches(3.858)),
        ("19",   "endpoints",        ACCENT_CYAN, Inches(5.677)),
        ("11",   "vulnerabilities",  ACCENT_GOLD, Inches(7.496)),
        ("4",    "validated chains", ACCENT_RED,  Inches(9.315)),
        ("0",    "manual commands",  ACCENT_PURP, Inches(11.134)),
    ]
    for val, label, color, stat_l in stats:
        txt(slide, val,
            stat_l, STATS_TOP + Inches(0.03), Inches(1.82), Inches(0.40),
            size=18, bold=True, color=color, align=PP_ALIGN.LEFT)
        txt(slide, label,
            stat_l, STATS_TOP + Inches(0.40), Inches(1.82), Inches(0.23),
            size=7.5, color=GREY_MID, align=PP_ALIGN.LEFT)

    slide_number(slide, "15", ACCENT_GOLD)
