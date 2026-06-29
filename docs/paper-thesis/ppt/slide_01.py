"""
Slide 1 — Cover Slide
"""
from palette import *


def build_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    set_bg(slide, BG_DARK)

    # ── Chrome: left bar = cyan, top = lime, bottom = cyan ────────────────────
    box(slide, Inches(0), Inches(0), Inches(0.06), SLIDE_H, fill=ACCENT_CYAN)
    box(slide, Inches(0.06), Inches(0), SLIDE_W - Inches(0.06), Inches(0.04), fill=ACCENT_LIME)
    box(slide, Inches(0.06), SLIDE_H - Inches(0.04), SLIDE_W - Inches(0.06), Inches(0.04), fill=ACCENT_CYAN)

    # ── Tag + Title ───────────────────────────────────────────────────────────
    txt(slide, "RESEARCH PRESENTATION",
        Inches(0.5), Inches(0.85), Inches(8), Inches(0.45),
        size=13, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

    tb = slide.shapes.add_textbox(Inches(0.5), Inches(1.35), Inches(8.8), Inches(1.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    run = p.add_run(); run.text = "CMatrix"
    run.font.name = "Calibri"; run.font.size = Pt(72); run.font.bold = True
    run.font.color.rgb = WHITE

    # ── Sub-title (multi-line, matching final PPTX) ───────────────────────────
    tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(2.85), Inches(8.83), Inches(1.21))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    lines = [
        "Dual-Graph-Guided LLM-Orchestrated",
        "Multi-Agent Framework for Autonomous",
        "Vulnerability Assessment and Penetration Testing (VAPT)",
    ]
    for j, line in enumerate(lines):
        p2 = tf2.paragraphs[0] if j == 0 else tf2.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        r2 = p2.add_run(); r2.text = line
        r2.font.size = Pt(21); r2.font.italic = True
        r2.font.color.rgb = ACCENT_CYAN

    # ── Divider ───────────────────────────────────────────────────────────────
    box(slide, Inches(0.5), Inches(4.28), Inches(6.5), Inches(0.03), fill=GREY_MID)

    # ── Keyword badges ────────────────────────────────────────────────────────
    badges = [
        ("Autonomous Pentesting",  Inches(0.5)),
        ("AI Agent Orchestration", Inches(3.55)),
        ("Attack Graph Reasoning", Inches(6.6)),
    ]
    for label, lx in badges:
        box(slide, lx, Inches(4.45), Inches(2.75), Inches(0.42),
            fill=CARD_BG, line_color=ACCENT_CYAN, lw=1.0)
        txt(slide, label,
            lx + Inches(0.1), Inches(4.48), Inches(2.6), Inches(0.36),
            size=12, bold=True, color=ACCENT_LIME, align=PP_ALIGN.CENTER)

    # ── Date + Scope info ─────────────────────────────────────────────────────
    txt(slide, "Supervisor Meeting  ·  June 2026",
        Inches(0.5), Inches(5.2), Inches(8), Inches(0.38),
        size=14, color=GREY_MID, align=PP_ALIGN.LEFT)
    txt(slide, "Black-Box · Grey-Box  ·  Network  ·  Web  ·  REST API",
        Inches(0.5), Inches(5.62), Inches(10), Inches(0.38),
        size=13, color=GREY_MID, align=PP_ALIGN.LEFT)

    # ── Right panel: Thesis Supervisor ───────────────────────────────────────
    SUP_L = Inches(9.65)
    SUP_W = Inches(3.53)

    box(slide, SUP_L, Inches(0.85), SUP_W, Inches(2.33),
        fill=RGBColor(0x06, 0x10, 0x22), line_color=ACCENT_CYAN, lw=1.2)
    txt(slide, "THESIS SUPERVISOR",
        SUP_L + Inches(0.14), Inches(0.92), SUP_W - Inches(0.24), Inches(0.22),
        size=8.5, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
    sup_lines = [
        ("Dr. Md. Abdur Razzaque", 11, True, WHITE),
        ("Professor & Chairman", 9.5, False, GREY_MID),
        ("Dept. of Computer Science & Engineering", 9, False, GREY_MID),
        ("University of Dhaka", 9, False, GREY_MID),
    ]
    for k, (line, sz, bold, clr) in enumerate(sup_lines):
        txt(slide, line,
            SUP_L + Inches(0.14), Inches(1.18) + k * Inches(0.28),
            SUP_W - Inches(0.24), Inches(0.26),
            size=sz, bold=bold, color=clr, align=PP_ALIGN.LEFT)

    # ── Right panel: Presented By ─────────────────────────────────────────────
    box(slide, SUP_L, Inches(3.33), SUP_W, Inches(3.0),
        fill=RGBColor(0x04, 0x18, 0x0C), line_color=ACCENT_LIME, lw=1.2)
    txt(slide, "PRESENTED BY",
        SUP_L + Inches(0.14), Inches(3.40), SUP_W - Inches(0.24), Inches(0.22),
        size=8.5, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
    pres_lines = [
        ("Nishan Paul", 11, True, WHITE),
        ("Reg. 55", 9.5, False, GREY_MID),
        ("Md Rakibur Rahman", 11, True, WHITE),
        ("Reg. 49", 9.5, False, GREY_MID),
        ("July 2025 · Batch 05", 9, False, GREY_MID),
        ("Professional Masters in Information and Cyber Security", 8.5, False, GREY_MID),
    ]
    for k, (line, sz, bold, clr) in enumerate(pres_lines):
        txt(slide, line,
            SUP_L + Inches(0.14), Inches(3.68) + k * Inches(0.38),
            SUP_W - Inches(0.24), Inches(0.34),
            size=sz, bold=bold, color=clr, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "01", ACCENT_CYAN)
