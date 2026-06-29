"""
Slide 14 — Cross-Mission Learning: Experience Store + Attack Strategy Library
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_TEAL)

    # ── Header ────────────────────────────────────────────────────────────────
    txt(slide, "CROSS-MISSION LEARNING",
        Inches(0.3), Inches(0.08), Inches(8.0), Inches(0.29),
        size=11, bold=True, color=ACCENT_TEAL, align=PP_ALIGN.LEFT)
    txt(slide, "Experience Store + Attack Strategy Library — CMatrix Gets Smarter Each Mission",
        Inches(0.3), Inches(0.38), Inches(12.5), Inches(0.54),
        size=26, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # ═══════════════════════════════════════════════════════
    # FLOW DIAGRAM — top strip
    # ═══════════════════════════════════════════════════════
    FLOW_TOP = Inches(1.10)
    FLOW_H = Inches(1.00)

    # Mission N box
    box(slide, Inches(0.30), FLOW_TOP, Inches(2.50), FLOW_H,
        fill=RGBColor(0x06, 0x14, 0x20), line_color=ACCENT_CYAN, lw=1.5)
    txt(slide, "Mission N\n(completed)",
        Inches(0.45), FLOW_TOP + Inches(0.15), Inches(2.20), Inches(0.54),
        size=13, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.CENTER)

    # Arrow + label
    arr(slide, Inches(2.80), FLOW_TOP + Inches(0.50), Inches(4.10), FLOW_TOP + Inches(0.50),
        color=ACCENT_CYAN, lw=1.5)
    txt(slide, "Report Agent writes\nvalidated chains",
        Inches(2.82), FLOW_TOP + Inches(0.12), Inches(1.12), Inches(0.53),
        size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # Experience Store box
    box(slide, Inches(4.10), FLOW_TOP, Inches(2.50), FLOW_H,
        fill=RGBColor(0x04, 0x20, 0x1E), line_color=ACCENT_TEAL, lw=2.0)
    txt(slide, "Cross-Mission\nExperience Store",
        Inches(4.155), FLOW_TOP + Inches(0.04), Inches(2.35), Inches(0.51),
        size=12, bold=True, color=ACCENT_TEAL, align=PP_ALIGN.CENTER)
    txt(slide, "RAG-backed · persistent\nacross all missions",
        Inches(4.155), FLOW_TOP + Inches(0.56), Inches(2.35), Inches(0.40),
        size=9.0, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)

    # Arrow + label
    arr(slide, Inches(6.70), FLOW_TOP + Inches(0.50), Inches(8.00), FLOW_TOP + Inches(0.50),
        color=ACCENT_GOLD, lw=1.5)
    txt(slide, "Crystallize\n(>=2 missions)",
        Inches(6.72), FLOW_TOP + Inches(0.10), Inches(1.12), Inches(0.39),
        size=8.5, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)

    # Attack Strategy Library box
    box(slide, Inches(8.00), FLOW_TOP + Inches(0.075), Inches(2.35), Inches(0.94),
        fill=RGBColor(0x20, 0x18, 0x04), line_color=ACCENT_GOLD, lw=2.0)
    txt(slide, "Attack Strategy\nLibrary",
        Inches(8.12), FLOW_TOP + Inches(0.10), Inches(2.134), Inches(0.51),
        size=12, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.CENTER)
    txt(slide, "Named strategies · confidence scores\ntechnology-fingerprint indexed",
        Inches(8.10), FLOW_TOP + Inches(0.54), Inches(2.35), Inches(0.40),
        size=9.0, italic=True, color=GREY_MID, align=PP_ALIGN.CENTER)

    # Arrow + label
    arr(slide, Inches(10.60), FLOW_TOP + Inches(0.50), Inches(11.80), FLOW_TOP + Inches(0.50),
        color=ACCENT_LIME, lw=1.5)
    txt(slide, "Pre-ranked seeds\nat mission start",
        Inches(10.565), FLOW_TOP + Inches(0.10), Inches(1.12), Inches(0.39),
        size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # Mission N+1 box
    box(slide, Inches(11.80), FLOW_TOP + Inches(0.01), Inches(1.25), FLOW_H,
        fill=RGBColor(0x06, 0x20, 0x10), line_color=ACCENT_LIME, lw=1.5)
    txt(slide, "Mission\nN+1",
        Inches(11.845), FLOW_TOP + Inches(0.10), Inches(1.15), Inches(0.51),
        size=12, bold=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)

    # Subtitle below flow
    txt(slide, "Candidate chain hypotheses injected into Commander context",
        Inches(7.128), FLOW_TOP + Inches(1.04), Inches(4.0), Inches(0.24),
        size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)

    # ═══════════════════════════════════════════════════════
    # LEFT PANEL — Cross-Mission Experience Store
    # ═══════════════════════════════════════════════════════
    P_TOP = Inches(2.42)
    P_H = Inches(4.55)
    LP_W = Inches(6.20)

    box(slide, Inches(0.30), P_TOP, LP_W, P_H,
        fill=RGBColor(0x04, 0x18, 0x18), line_color=ACCENT_TEAL, lw=1.5)
    box(slide, Inches(0.30), P_TOP, LP_W, Inches(0.40), fill=ACCENT_TEAL)
    txt(slide, "Cross-Mission Experience Store",
        Inches(0.42), P_TOP + Inches(0.06), Inches(6.0), Inches(0.30),
        size=12, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    # Sub-sections
    csections = [
        ("What it stores",
         "Per-mission · per-chain raw records of validated exploitation outcomes. Target technology fingerprint · CVE · successful tool invocation · ChainStep sequence · mission outcome."),
        ("When it's written",
         "Report Agent writes one entry for every chain with terminal status VALIDATED at mission close."),
        ("When it's read",
         "Commander queries immediately after Recon Agent writes first Technology nodes to ASG — before Analysis begins. Retrieved records become candidate chain hypotheses."),
        ("Research origin",
         "Generalizes AutoAttacker's within-mission experience-reuse mechanism to cross-mission scope. AutoAttacker reuses subtasks within one session; CMatrix accumulates across every mission ever run."),
    ]

    row_y = P_TOP + Inches(0.50)
    for title, body in csections:
        box(slide, Inches(0.42), row_y, Inches(5.96), Inches(0.94),
            fill=RGBColor(0x06, 0x22, 0x22), line_color=ACCENT_TEAL, lw=0.8)
        txt(slide, title,
            Inches(0.52), row_y + Inches(0.06), Inches(5.82), Inches(0.29),
            size=11, bold=True, color=ACCENT_TEAL, align=PP_ALIGN.LEFT)
        txt(slide, body,
            Inches(0.52), row_y + Inches(0.32), Inches(5.82), Inches(0.55),
            size=9.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)
        row_y += Inches(0.98)

    # ═══════════════════════════════════════════════════════
    # RIGHT PANEL — Attack Strategy Library
    # ═══════════════════════════════════════════════════════
    RP_L = Inches(6.75)
    RP_W = Inches(6.38)

    box(slide, RP_L, P_TOP, RP_W, P_H,
        fill=RGBColor(0x1C, 0x14, 0x04), line_color=ACCENT_GOLD, lw=1.5)
    box(slide, RP_L, P_TOP, RP_W, Inches(0.40), fill=ACCENT_GOLD)
    txt(slide, "Attack Strategy Library",
        RP_L + Inches(0.12), P_TOP + Inches(0.06), Inches(6.18), Inches(0.30),
        size=12, bold=True, color=BG_DARK, align=PP_ALIGN.LEFT)

    rsections = [
        ("What it stores",
         "Generalized attack procedures distilled from multiple validated outcomes against the same target technology class. Named strategies (e.g. STRAT-WP-SQLI-001) with confidence scores."),
        ("Crystallization threshold",
         "Same technology fingerprint (e.g. WordPress 5.x + WooCommerce + Nginx) produces validated AttackChain in 2 or more independent missions → Commander triggers crystallization."),
        ("When it's used",
         "Retrieved at mission start. Strategies are injected as pre-ranked APG AttackChain seeds — prioritized above zero-prior chains because they carry validated track record."),
        ("Why it matters",
         "No existing autonomous VAPT system accumulates and generalizes validated exploitation procedures across sessions. Every prior system resets to zero knowledge on each mission. CMatrix's library makes it measurably more efficient on repeat target-type engagements."),
    ]

    row_y = P_TOP + Inches(0.50)
    for title, body in rsections:
        box(slide, RP_L + Inches(0.12), row_y, Inches(6.14), Inches(0.94),
            fill=RGBColor(0x22, 0x18, 0x06), line_color=ACCENT_GOLD, lw=0.8)
        txt(slide, title,
            RP_L + Inches(0.22), row_y + Inches(0.06), Inches(6.0), Inches(0.29),
            size=11, bold=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT)
        txt(slide, body,
            RP_L + Inches(0.22), row_y + Inches(0.32), Inches(6.0), Inches(0.55),
            size=9.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)
        row_y += Inches(0.98)

    slide_number(slide, "14", ACCENT_TEAL)
