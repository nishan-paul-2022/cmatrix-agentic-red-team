"""
Slide 6 — Dual-Graph World Model
"""
from palette import *
from pptx.util import Pt


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_GOLD)

    txt(slide, "DUAL-GRAPH WORLD MODEL", Inches(0.3), Inches(0.07), Inches(8), Inches(0.26),
        size=10, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
    txt(slide, "Two Strictly Separated Knowledge Layers",
        Inches(0.3), Inches(0.32), Inches(12.5), Inches(0.52),
        size=32, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    slide_number(slide, "06", ACCENT_GOLD)

    # ── LEFT: ASG Panel ───────────────────────────────────────────────────────
    L = Inches(0.3)
    LW = Inches(6.5)
    PT = Inches(0.9)
    PH = Inches(6.42)

    box(slide, L, PT, LW, PH, fill=RGBColor(0x05, 0x12, 0x05), line_color=ACCENT_LIME, lw=1.2)
    txt(slide, "ASG \u2014 Attack Surface Graph", L + Inches(0.12), PT + Inches(0.08),
        LW - Inches(0.2), Inches(0.26), size=14, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
    txt(slide, "Discovered Reality  \u00b7  Every node = confirmed by tool  \u00b7  Every edge = confirmed relationship",
        L + Inches(0.12), PT + Inches(0.34), LW - Inches(0.2), Inches(0.22),
        size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # ASG graph nodes (simplified visual representation)
    NW = Inches(1.1)
    NH = Inches(0.4)

    def asg_node(slide, label, x, y, color=ACCENT_LIME):
        box(slide, x, y, NW, NH, fill=color, line_color=RGBColor(0x00, 0xAA, 0x00), lw=0.7)
        txt(slide, label, x, y + Inches(0.06), NW, NH - Inches(0.1),
            size=8, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    def asg_node_vuln(slide, label, x, y):
        box(slide, x, y, NW + Inches(0.3), NH, fill=ACCENT_RED, line_color=ACCENT_RED, lw=0.7)
        txt(slide, label, x, y + Inches(0.04), NW + Inches(0.3), NH - Inches(0.06),
            size=7.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    def asg_node_ev(slide, label, x, y):
        box(slide, x, y, NW + Inches(0.2), NH, fill=ACCENT_PURP, line_color=ACCENT_PURP, lw=0.7)
        txt(slide, label, x, y + Inches(0.04), NW + Inches(0.2), NH - Inches(0.06),
            size=7, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    def edge_lbl(slide, label, x, y):
        txt(slide, label, x, y, Inches(1.0), Inches(0.18), size=7, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # Row 1
    base_t = PT + Inches(0.62)
    asg_node(slide, "Domain\nshopvault.io", L + Inches(0.1), base_t)
    edge_lbl(slide, "has_host", L + Inches(1.28), base_t + Inches(0.12))
    asg_node(slide, "Host\n10.0.0.1\nUbuntu 22", L + Inches(2.0), base_t - Inches(0.1), color=ACCENT_LIME)
    asg_node(slide, "Host\n10.0.0.2\nDebian 11", L + Inches(2.0), base_t + Inches(0.65))
    asg_node(slide, "Host\napi.shopvault", L + Inches(2.0), base_t + Inches(1.38))

    # Ports
    asg_node(slide, "Port :443\ntcp open", L + Inches(3.28), base_t - Inches(0.1))
    asg_node(slide, "Port :22\ntcp open", L + Inches(3.28), base_t + Inches(0.42))
    asg_node(slide, "Port :8080\nunenc", L + Inches(3.28), base_t + Inches(0.94))
    asg_node(slide, "Port :80\ntcp open", L + Inches(3.28), base_t + Inches(1.46))

    # Services
    asg_node(slide, "Service\nNginx 1.18", L + Inches(4.5), base_t - Inches(0.1))
    asg_node(slide, "Service\nOpenSSH 8.9", L + Inches(4.5), base_t + Inches(0.42))
    asg_node(slide, "Service\nHTTP plain", L + Inches(4.5), base_t + Inches(0.94))

    # Tech nodes
    asg_node(slide, "Tech\nWordPress 5.9", L + Inches(0.55), base_t + Inches(2.2))
    asg_node(slide, "Tech\nWooCommerce", L + Inches(1.75), base_t + Inches(2.2))
    asg_node(slide, "Tech\nDjango 4.1", L + Inches(3.0), base_t + Inches(2.2))

    # Endpoints
    YELLOW_EP = RGBColor(0xB8, 0x86, 0x00)
    box(slide, L + Inches(4.4), base_t + Inches(1.78), NW, Inches(0.5), fill=YELLOW_EP)
    txt(slide, "Endpoint\n/wp-admin\nHIGH", L + Inches(4.4), base_t + Inches(1.8), NW, Inches(0.45),
        size=7.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    RED_EP = RGBColor(0x8B, 0x00, 0x00)
    box(slide, L + Inches(4.4), base_t + Inches(2.38), NW + Inches(0.2), Inches(0.55), fill=RED_EP)
    txt(slide, "/backup/\ndb_export\nCRITICAL", L + Inches(4.4), base_t + Inches(2.42), NW + Inches(0.2), Inches(0.5),
        size=7.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    asg_node(slide, "Endpoint\n/api/orders", L + Inches(0.55), base_t + Inches(2.85))
    asg_node(slide, "Endpoint\n/api/users\nundocumented", L + Inches(1.75), base_t + Inches(2.85))

    # Param + vuln + evidence
    asg_node(slide, "Param\nuser_id=?\ninjectable", L + Inches(0.55), base_t + Inches(3.55))
    asg_node_vuln(slide, "CVE-2022-21661\nSQLi CVSS 8.8", L + Inches(1.9), base_t + Inches(3.55))
    asg_node_vuln(slide, "IDOR /orders\nSeverity:HIGH", L + Inches(3.35), base_t + Inches(3.55))
    asg_node_ev(slide, "Evidence\nsqli-extract.txt", L + Inches(3.5), base_t + Inches(4.25))
    asg_node_ev(slide, "Evidence\nadmin-panel.png", L + Inches(4.75), base_t + Inches(3.55))
    asg_node_ev(slide, "Evidence\nwebshell-rce.png", L + Inches(4.75), base_t + Inches(4.25))

    # Edge labels
    edge_lbl(slide, "runs", L + Inches(3.2), base_t + Inches(0.12))
    edge_lbl(slide, "uses", L + Inches(4.46), base_t + Inches(2.56))
    edge_lbl(slide, "has_ep", L + Inches(4.25), base_t + Inches(2.02))
    edge_lbl(slide, "affected_by", L + Inches(2.1), base_t + Inches(3.28))
    edge_lbl(slide, "has_param", L + Inches(0.8), base_t + Inches(3.28))
    edge_lbl(slide, "affected_by", L + Inches(3.4), base_t + Inches(3.28))
    edge_lbl(slide, "validated_by", L + Inches(3.6), base_t + Inches(4.0))

    # Legend
    legend_t = PT + PH - Inches(0.32)
    leg_items = [("Infrastructure", GREY_DARK), ("Application", ACCENT_LIME),
                 ("Vulnerability", ACCENT_RED), ("Evidence", ACCENT_PURP)]
    for k, (name, color) in enumerate(leg_items):
        lx = L + Inches(0.12) + k * Inches(1.55)
        box(slide, lx, legend_t, Inches(0.18), Inches(0.18), fill=color)
        txt(slide, name, lx + Inches(0.22), legend_t - Inches(0.02), Inches(1.3), Inches(0.22),
            size=8, color=GREY_MID, align=PP_ALIGN.LEFT)

    # ── Strict Separation ─────────────────────────────────────────────────────
    sep_x = Inches(6.85)
    box(slide, sep_x, Inches(2.2), Inches(0.22), Inches(4.8), fill=GREY_MID)
    txt(slide, "STRICT\nSEPARATION", sep_x - Inches(0.1), Inches(4.3), Inches(0.55), Inches(0.55),
        size=7, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # ── RIGHT: APG Panel ──────────────────────────────────────────────────────
    R = Inches(7.12)
    RW = SLIDE_W - R - Inches(0.12)

    box(slide, R, PT, RW, PH, fill=RGBColor(0x12, 0x0A, 0x00), line_color=ACCENT_GOLD, lw=1.2)
    txt(slide, "APG \u2014 Attack Path Graph", R + Inches(0.12), PT + Inches(0.08),
        RW - Inches(0.2), Inches(0.26), size=14, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
    txt(slide, "Inferred Opportunity  \u00b7  Commander reasons from ASG vulnerabilities \u2014 no raw scan data",
        R + Inches(0.12), PT + Inches(0.34), RW - Inches(0.2), Inches(0.22),
        size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    CHAIN_BG = RGBColor(0x0C, 0x0A, 0x00)
    STEP_BG = RGBColor(0x0A, 0x18, 0x0A)
    STEP_BG2 = RGBColor(0x14, 0x0A, 0x00)

    def chain_block(slide, label, top, color, steps, impact):
        cw = RW - Inches(0.22)
        box(slide, R + Inches(0.1), top, cw, Inches(0.26), fill=color)
        txt(slide, label, R + Inches(0.15), top + Inches(0.03), cw - Inches(0.1), Inches(0.22),
            size=9.5, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
        ch = Inches(0.6)
        sw = (cw - Inches(0.15) - (len(steps) - 1) * Inches(0.06)) / len(steps)
        for k, (tool, action, note) in enumerate(steps):
            sl = R + Inches(0.1) + k * (sw + Inches(0.06))
            box(slide, sl, top + Inches(0.26), sw, ch, fill=STEP_BG, line_color=GREY_DARK, lw=0.5)
            txt(slide, f"{tool}\n{action}\n{note}", sl + Inches(0.05), top + Inches(0.28),
                sw - Inches(0.08), ch - Inches(0.06), size=7.5, color=WHITE, align=PP_ALIGN.CENTER, wrap=True)
            if k < len(steps) - 1:
                arr(slide, sl + sw, top + Inches(0.56), sl + sw + Inches(0.06), top + Inches(0.56),
                    color=GREY_MID, lw=1.0)
        box(slide, R + Inches(0.1), top + Inches(0.86), cw, Inches(0.28), fill=RGBColor(0x20, 0x08, 0x08))
        txt(slide, impact, R + Inches(0.15), top + Inches(0.9), cw - Inches(0.1), Inches(0.22),
            size=8, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    ct1 = PT + Inches(0.62)
    chain_block(slide, "Chain-01: SQLi \u2192 RCE  risk: 9.1\u2191  \u2713 VALIDATED", ct1,
                RGBColor(0x1A, 0x12, 0x00),
                [("SQLMap", "WP_Query", "SQLi confirmed"),
                 ("SQLMap", "dump users", "hash cracked"),
                 ("Metasploit", "webshell", "Full RCE")],
                "IMPACT  CRITICAL  \u00b7  Full RCE \u00b7 Customer PII exposed")

    ct2 = ct1 + Inches(1.22)
    chain_block(slide, "Chain-02: IDOR \u2192 Orders  risk: 7.5  \u2713 VALIDATED", ct2,
                RGBColor(0x0A, 0x18, 0x1A),
                [("SQLMap", "IDOR param", "confirmed"),
                 ("HTTP GET", "all orders", "PII exposed")],
                "IMPACT  HIGH  \u00b7  All orders + PII exposed")

    ct3 = ct2 + Inches(1.22)
    chain_block(slide, "Chain-03: Blind SQLi \u2192 Creds  risk: 8.1  \u2713 VALIDATED", ct3,
                RGBColor(0x16, 0x10, 0x00),
                [("SQLMap", "blind SQLi", "staging login"),
                 ("Extract", "DB creds", "reuse risk")],
                "IMPACT  HIGH  \u00b7  DB credentials extracted \u00b7 reuse risk")

    # APG Priority Queue
    pq_t = ct3 + Inches(1.28)
    box(slide, R + Inches(0.1), pq_t, RW - Inches(0.22), Inches(0.28), fill=ACCENT_GOLD)
    txt(slide, "APG Priority Queue:  #1 Chain-01 \u00b7 9.1  \u00b7  #2 Chain-03 \u00b7 8.1  \u00b7  #3 Chain-02 \u00b7 7.5  \u00b7  #4 Chain-04 \u00b7 7.0",
        R + Inches(0.15), pq_t + Inches(0.04), RW - Inches(0.3), Inches(0.20),
        size=8, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    txt(slide, "\u00b7 Commander re-ranks on every status change",
        R + Inches(0.15), pq_t + Inches(0.24), RW - Inches(0.3), Inches(0.18),
        size=7.5, color=BG_DARK, align=PP_ALIGN.CENTER)

    # Separation principle footnote
    fn_t = PT + PH - Inches(0.28)
    txt(slide, "Separation Principle: Discovery agents write only to the ASG \u2014 they never reason about chains.  "
        "The Commander writes only to the APG \u2014 it never runs tools.  No agent conflates discovered facts with hypothesised attack reasoning.",
        Inches(0.3), fn_t + Inches(0.02), SLIDE_W - Inches(0.6), Inches(0.24),
        size=8, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)
