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

    # ── Ghost watermark (dim "CMATRIX" on right) ──────────────────────────────
    ghost = slide.shapes.add_textbox(Inches(4.5), Inches(0.8), Inches(8.8), Inches(5.8))
    tf = ghost.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = "CMATRIX"
    run.font.name = "Calibri"; run.font.size = Pt(130); run.font.bold = True
    # Dim colour via XML
    sp = ghost.element
    for r in sp.iter(qn('a:r')):
        for sf in r.iter(qn('a:solidFill')):
            srgb = sf.find(qn('a:srgbClr'))
            if srgb is not None:
                srgb.set('val', '0D2535')

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

    # ── Sub-title ─────────────────────────────────────────────────────────────
    txt(slide,
        "Dual-Graph-Guided LLM-Orchestrated\nMulti-Agent Framework for Autonomous VAPT",
        Inches(0.5), Inches(3.05), Inches(9.5), Inches(1.2),
        size=22, italic=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)

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
    txt(slide, "Black-Box & Grey-Box Assessment  ·  Network  ·  Web  ·  REST API",
        Inches(0.5), Inches(5.62), Inches(10), Inches(0.38),
        size=13, color=GREY_MID, align=PP_ALIGN.LEFT)

    slide_number(slide, "01", ACCENT_CYAN)
