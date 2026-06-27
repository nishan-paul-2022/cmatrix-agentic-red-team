"""
Slide 04 — Scope
=================
Clearly defines: In Scope, Out of Scope, Assessment Modes (Black-Box vs Grey-Box),
and the operator's role in the initial configuration.
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_CYAN)
    slide_header(slide, "SCOPE", "What CMatrix Assesses — and What It Does Not",
                 ACCENT_CYAN, title_size=34, divider_w=9)

    # ── Left: IN SCOPE ────────────────────────────────────────────────────────
    IN_L, IN_W = Inches(0.22), Inches(5.9)
    IN_T, IN_H = Inches(1.08), Inches(5.4)
    box(slide, IN_L, IN_T, IN_W, IN_H,
        fill=RGBColor(0x04, 0x18, 0x0C), line_color=ACCENT_LIME, lw=1.8)
    box(slide, IN_L, IN_T, IN_W, Inches(0.34), fill=ACCENT_LIME)
    txt(slide, "✓  IN SCOPE", IN_L + Inches(0.12), IN_T + Inches(0.05),
        IN_W - Inches(0.2), Inches(0.26), size=12, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    in_scope = [
        ("Web Applications", "HTTP/HTTPS services, CMS, REST APIs, GraphQL endpoints."),
        ("Network Services", "Exposed ports, services, TLS/SSL, open protocols."),
        ("API Attack Surface", "REST endpoints, parameter injection, IDOR, auth bypass."),
        ("Black-Box Mode", "Zero prior knowledge. Operator provides: root domain + scope declaration only."),
        ("Grey-Box Mode", "Partial knowledge. Operator additionally provides: known IP ranges, credentials, "
                         "network topology fragments. ASG Host nodes are pre-seeded."),
        ("Authorised Assessments", "CMatrix operates only within declared scope. Scope check fires before "
                                   "every tool execution at the Risk Gate."),
    ]
    for i, (heading, body) in enumerate(in_scope):
        it = IN_T + Inches(0.44) + i * Inches(0.83)
        box(slide, IN_L + Inches(0.12), it, IN_W - Inches(0.24), Inches(0.78),
            fill=RGBColor(0x06, 0x22, 0x10), line_color=ACCENT_LIME, lw=0.5)
        txt(slide, heading, IN_L + Inches(0.22), it + Inches(0.05),
            IN_W - Inches(0.36), Inches(0.26), size=11, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
        txt(slide, body, IN_L + Inches(0.22), it + Inches(0.3),
            IN_W - Inches(0.36), Inches(0.42), size=9.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # ── Right: OUT OF SCOPE ───────────────────────────────────────────────────
    OUT_L, OUT_W = Inches(6.32), Inches(4.9)
    OUT_T, OUT_H = Inches(1.08), Inches(3.4)
    box(slide, OUT_L, OUT_T, OUT_W, OUT_H,
        fill=RGBColor(0x1C, 0x08, 0x08), line_color=ACCENT_RED, lw=1.8)
    box(slide, OUT_L, OUT_T, OUT_W, Inches(0.34), fill=ACCENT_RED)
    txt(slide, "✕  OUT OF SCOPE", OUT_L + Inches(0.12), OUT_T + Inches(0.05),
        OUT_W - Inches(0.2), Inches(0.26), size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    out_scope = [
        "White-Box  (source code review, SAST)",
        "Mobile Applications  (iOS, Android)",
        "Cloud / IoT Infrastructure  (AWS, Azure, embedded devices)",
        "Wireless Networks  (Wi-Fi, Bluetooth, RF)",
        "Active Directory / Domain Services",
        "Physical / Social Engineering Attacks",
    ]
    for i, item in enumerate(out_scope):
        ot = OUT_T + Inches(0.44) + i * Inches(0.48)
        box(slide, OUT_L + Inches(0.12), ot, OUT_W - Inches(0.24), Inches(0.42),
            fill=RGBColor(0x28, 0x0C, 0x0C), line_color=ACCENT_RED, lw=0.4)
        txt(slide, f"✕  {item}", OUT_L + Inches(0.22), ot + Inches(0.06),
            OUT_W - Inches(0.36), Inches(0.32), size=10, color=GREY_MID, align=PP_ALIGN.LEFT)

    # ── Right bottom: Operator config note ───────────────────────────────────
    OP_T = OUT_T + OUT_H + Inches(0.12)
    OP_H = Inches(5.4) - (OP_T - IN_T)
    box(slide, OUT_L, OP_T, OUT_W, OP_H,
        fill=RGBColor(0x06, 0x10, 0x22), line_color=ACCENT_CYAN, lw=1.2)
    box(slide, OUT_L, OP_T, OUT_W, Inches(0.3), fill=ACCENT_CYAN)
    txt(slide, "OPERATOR CONFIGURATION  (one-time, before mission start)",
        OUT_L + Inches(0.1), OP_T + Inches(0.04), OUT_W - Inches(0.18), Inches(0.24),
        size=9, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    op_items = [
        "Root domain (e.g. shopvault.io)",
        "Scope declaration  (all subdomains · web apps · APIs)",
        "Assessment mode  (Black-Box or Grey-Box)",
        "Grey-Box extras if applicable  (IP ranges, credentials)",
    ]
    for i, item in enumerate(op_items):
        ot2 = OP_T + Inches(0.38) + i * Inches(0.34)
        txt(slide, f"→  {item}", OUT_L + Inches(0.18), ot2,
            OUT_W - Inches(0.3), Inches(0.3), size=9.5, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    txt(slide,
        "All subsequent tool calls, reasoning, and reporting are fully autonomous — "
        "zero manual commands during the assessment.",
        OUT_L + Inches(0.18), OP_T + Inches(1.78), OUT_W - Inches(0.3), Inches(0.52),
        size=9.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "04", ACCENT_CYAN)
