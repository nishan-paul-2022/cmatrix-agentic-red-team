"""
Slide 4 — Scope
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_LIME)

    slide_header(slide, "SCOPE", "What CMatrix Assesses — and What It Does Not",
                 ACCENT_LIME, title_size=34)
    slide_number(slide, "04", ACCENT_LIME)

    # ── Left column: IN SCOPE ─────────────────────────────────────────────────
    L_L = Inches(0.3)
    L_W = Inches(6.3)
    col_t = Inches(1.15)
    col_h = Inches(6.1)

    box(slide, L_L, col_t, L_W, Inches(0.36), fill=ACCENT_LIME)
    txt(slide, "\u2713  IN SCOPE", L_L + Inches(0.12), col_t + Inches(0.04),
        L_W - Inches(0.2), Inches(0.28), size=12, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    in_scope = [
        ("Web Applications", "HTTP/HTTPS services, CMS, REST APIs, GraphQL endpoints."),
        ("Network Services", "Exposed ports, services, TLS/SSL, open protocols."),
        ("API Attack Surface", "REST endpoints, parameter injection, IDOR, auth bypass."),
        ("Black-Box Mode", "Zero prior knowledge. Operator provides: root domain + scope declaration only."),
        ("Grey-Box Mode", "Partial knowledge. Operator additionally provides: known IP ranges, credentials, network topology fragments. ASG Host nodes are pre-seeded."),
        ("Authorised Assessments", "CMatrix operates only within declared scope. Scope check fires before every tool execution at the Risk Gate."),
    ]

    CARD_IN = RGBColor(0x08, 0x20, 0x0A)
    item_h = Inches(0.76)
    item_gap = Inches(0.07)
    item_t = col_t + Inches(0.42)

    for i, (title, body) in enumerate(in_scope):
        top = item_t + i * (item_h + item_gap)
        box(slide, L_L, top, L_W, item_h, fill=CARD_IN, line_color=ACCENT_LIME, lw=0.8)
        txt(slide, title, L_L + Inches(0.14), top + Inches(0.06),
            L_W - Inches(0.25), Inches(0.28), size=11.5, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
        txt(slide, body, L_L + Inches(0.14), top + Inches(0.34),
            L_W - Inches(0.25), Inches(0.38), size=10, color=WHITE, align=PP_ALIGN.LEFT, wrap=True)

    # ── Right column: OUT OF SCOPE ────────────────────────────────────────────
    R_L = Inches(6.83)
    R_W = Inches(6.3)

    box(slide, R_L, col_t, R_W, Inches(0.36), fill=ACCENT_RED)
    txt(slide, "\u2715  OUT OF SCOPE", R_L + Inches(0.12), col_t + Inches(0.04),
        R_W - Inches(0.2), Inches(0.28), size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    out_scope = [
        "\u2715  White-Box  (source code review, SAST)",
        "\u2715  Mobile Applications  (iOS, Android)",
        "\u2715  Cloud / IoT Infrastructure  (AWS, Azure, embedded devices)",
        "\u2715  Wireless Networks  (Wi-Fi, Bluetooth, RF)",
        "\u2715  Active Directory / Domain Services",
        "\u2715  Physical / Social Engineering Attacks",
    ]

    CARD_OUT = RGBColor(0x2A, 0x08, 0x08)
    out_item_h = Inches(0.42)
    out_item_gap = Inches(0.06)
    out_t = col_t + Inches(0.42)

    for i, label in enumerate(out_scope):
        top = out_t + i * (out_item_h + out_item_gap)
        box(slide, R_L, top, R_W, out_item_h, fill=CARD_OUT, line_color=ACCENT_RED, lw=0.7)
        txt(slide, label, R_L + Inches(0.12), top + Inches(0.06),
            R_W - Inches(0.2), Inches(0.30), size=11, color=WHITE, align=PP_ALIGN.LEFT)

    # ── Operator Configuration box ────────────────────────────────────────────
    op_t = col_t + Inches(0.42) + 6 * (out_item_h + out_item_gap) + Inches(0.1)
    op_h = Inches(1.65)
    box(slide, R_L, op_t, R_W, Inches(0.32), fill=ACCENT_CYAN)
    txt(slide, "OPERATOR CONFIGURATION  (one-time, before mission start)",
        R_L + Inches(0.12), op_t + Inches(0.04), R_W - Inches(0.2), Inches(0.25),
        size=10, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    op_lines = [
        "\u2192  Root domain (e.g. shopvault.io)",
        "\u2192  Scope declaration  (all subdomains \u00b7 web apps \u00b7 APIs)",
        "\u2192  Assessment mode  (Black-Box or Grey-Box)",
        "\u2192  Grey-Box extras if applicable  (IP ranges, credentials)",
    ]
    CARD_OP = RGBColor(0x04, 0x14, 0x28)
    box(slide, R_L, op_t + Inches(0.32), R_W, op_h - Inches(0.32), fill=CARD_OP, line_color=ACCENT_CYAN, lw=0.8)
    for i, line in enumerate(op_lines):
        txt(slide, line, R_L + Inches(0.16), op_t + Inches(0.38) + i * Inches(0.29),
            R_W - Inches(0.3), Inches(0.27), size=10.5, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    # Italic footnote
    txt(slide, "All subsequent tool calls, reasoning, and reporting are fully autonomous — zero manual commands during the assessment.",
        R_L, op_t + op_h + Inches(0.06), R_W, Inches(0.38),
        size=9.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)
