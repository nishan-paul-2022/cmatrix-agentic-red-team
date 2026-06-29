"""
Slide 9 — Offensive Tool Catalogue
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_RED)

    slide_header(slide, "OFFENSIVE TOOL CATALOGUE",
                 "11 Industry-Standard Security Tools \u2014 AI Agent Operated",
                 ACCENT_RED, title_size=28)
    slide_number(slide, "09", ACCENT_RED)

    # ── Column headers ─────────────────────────────────────────────────────────
    COL1_L, COL1_W = Inches(0.3), Inches(4.3)
    COL2_L, COL2_W = Inches(4.72), Inches(4.46)
    COL3_L, COL3_W = Inches(9.3), Inches(1.95)
    COL4_L, COL4_W = Inches(11.32), Inches(1.87)
    HDR_T = Inches(1.05)

    def col_hdr(label, l, w, color):
        box(slide, l, HDR_T, w, Inches(0.32), fill=color)
        txt(slide, label, l + Inches(0.1), HDR_T + Inches(0.04), w - Inches(0.2), Inches(0.24),
            size=10, bold=True, color=BG_DARK if color not in [ACCENT_RED, ACCENT_PURP] else WHITE,
            align=PP_ALIGN.CENTER)

    col_hdr("PHASE 1  \u00b7  RECONNAISSANCE", COL1_L, COL1_W, ACCENT_LIME)
    col_hdr("PHASE 2  \u00b7  ANALYSIS", COL2_L, COL2_W, ACCENT_CYAN)
    col_hdr("PHASE 3  \u00b7  VALIDATION", COL3_L, COL3_W, ACCENT_RED)
    col_hdr("PHASE 3  \u00b7  EVIDENCE", COL4_L, COL4_W, ACCENT_PURP)

    # ── Tool cards ─────────────────────────────────────────────────────────────
    CARD_T = HDR_T + Inches(0.38)

    def tool_card(slide, num, name, subtitle, body, l, top, w, h, num_color, name_color):
        box(slide, l, top, w, h, fill=RGBColor(0x08, 0x10, 0x20), line_color=RGBColor(0x20, 0x28, 0x38), lw=0.7)
        # Number badge
        box(slide, l, top, Inches(0.42), h, fill=num_color)
        txt(slide, num, l, top + h/2 - Inches(0.18), Inches(0.42), Inches(0.36),
            size=18, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
        # Content
        cx = l + Inches(0.5)
        cw = w - Inches(0.58)
        txt(slide, name, cx, top + Inches(0.08), cw, Inches(0.28),
            size=13, bold=True, color=name_color, align=PP_ALIGN.CENTER)
        txt(slide, subtitle, cx, top + Inches(0.36), cw, Inches(0.22),
            size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)
        txt(slide, body, cx, top + Inches(0.58), cw, h - Inches(0.68),
            size=9, color=WHITE, align=PP_ALIGN.CENTER, wrap=True)

    # Phase 1 — Recon (3 tools, full height each)
    ph1_tools = [
        ("1", "Amass", "Subdomain Enumeration \u00b7 Recon Agent",
         "DNS brute-force \u00b7 certificate transparency logs \u00b7 passive OSINT. Discovers all external subdomains and maps attack surface entry points."),
        ("2", "httpx", "Live Host Probing \u00b7 Recon Agent",
         "Validates which discovered hosts respond over HTTP/HTTPS. Identifies web servers, status codes, redirects, TLS details."),
        ("3", "Nmap", "Port + Service Scan \u00b7 Recon Agent",
         "Port scanning, service fingerprinting, OS detection. Optional NSE script execution for vuln detection on open services."),
    ]
    TH1 = (SLIDE_H - CARD_T - Inches(0.7)) / 3 - Inches(0.06)
    for i, (num, name, sub, body) in enumerate(ph1_tools):
        tool_card(slide, num, name, sub, body,
                  COL1_L, CARD_T + i * (TH1 + Inches(0.06)),
                  COL1_W, TH1, ACCENT_LIME, ACCENT_LIME)

    # Phase 2 — Analysis (5 tools)
    ph2_tools = [
        ("4", "WhatWeb", "Technology Fingerprinting \u00b7 Analysis Agent",
         "Identifies CMS, frameworks, server software, JS libraries, and versions from HTTP responses. Seeds Technology nodes for the ASG."),
        ("5", "Gobuster", "Directory Brute-Force \u00b7 Analysis Agent",
         "Discovers hidden paths, admin panels, backup files, and exposed resources via wordlist-based HTTP path enumeration."),
        ("6", "ffuf", "API + Parameter Fuzzing \u00b7 Analysis Agent",
         "Fast web fuzzer for API route discovery, parameter fuzzing, virtual host enumeration, and undocumented endpoint identification."),
        ("7", "Nuclei", "Template-Based Vuln Scan \u00b7 Analysis Agent",
         "Matches discovered services and technologies against a library of CVE and misconfiguration templates for automated vulnerability detection."),
        ("8", "OWASP ZAP", "Active Web App Scan \u00b7 Analysis Agent",
         "Crawls and actively tests for OWASP Top 10: XSS, CSRF, injection flaws, authentication weaknesses, and insecure direct object references."),
    ]
    TH2 = (SLIDE_H - CARD_T - Inches(0.7)) / 5 - Inches(0.05)
    for i, (num, name, sub, body) in enumerate(ph2_tools):
        tool_card(slide, num, name, sub, body,
                  COL2_L, CARD_T + i * (TH2 + Inches(0.05)),
                  COL2_W, TH2, ACCENT_CYAN, ACCENT_CYAN)

    # Phase 3 — Validation (2 tools)
    ph3_tools = [
        ("9", "SQLMap", "SQL Injection Validation \u00b7 Validation Agent",
         "Automated SQLi detection and exploitation. Confirms injection points, extracts database data, tests for OS-level access escalation."),
        ("10", "Metasploit", "Exploit + RCE Demo \u00b7 Validation Agent",
         "Executes known exploits against identified vulnerabilities. Validates APG ChainSteps, demonstrates impact, achieves proof of exploitation."),
    ]
    TH3 = (SLIDE_H - CARD_T - Inches(0.7)) / 2 - Inches(0.06)
    for i, (num, name, sub, body) in enumerate(ph3_tools):
        tool_card(slide, num, name, sub, body,
                  COL3_L, CARD_T + i * (TH3 + Inches(0.06)),
                  COL3_W, TH3, ACCENT_RED, ACCENT_RED)

    # Phase 3 — Evidence (1 tool)
    tool_card(slide, "11", "EyeWitness", "Screenshot Evidence \u00b7 Evidence Agent",
              "Headless screenshot capture of web pages, exposed panels, and API responses. Produces visual proof artifacts linked to ASG Evidence nodes.",
              COL4_L, CARD_T, COL4_W, TH3 * 2 + Inches(0.06), ACCENT_PURP, ACCENT_PURP)

    # Bottom disclaimer
    foot_t = SLIDE_H - Inches(0.68)
    box(slide, Inches(0.3), foot_t, SLIDE_W - Inches(0.6), Inches(0.44),
        fill=RGBColor(0x08, 0x08, 0x20), line_color=ACCENT_PURP, lw=0.8)
    txt(slide, "\U0001f512  Every tool is wrapped in a Tool Adapter \u2014 agents reason about targets, not command syntax.  "
        "No irreversible offensive operation executes without Commander-level scope validation.",
        Inches(0.45), foot_t + Inches(0.06), SLIDE_W - Inches(0.9), Inches(0.32),
        size=9.5, color=WHITE, align=PP_ALIGN.LEFT, wrap=True)
