"""
Slide 03 — Related Work Gap Analysis
=====================================
Three-column table: System | What it lacks | How CMatrix addresses it
Positioned between Problem and Scope to ground the architecture in named prior work.
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_PURP)
    slide_header(slide, "RELATED WORK", "Where Prior Systems Fall Short — and How CMatrix Responds",
                 ACCENT_PURP, title_size=28, divider_w=10)

    # ── Column headers ────────────────────────────────────────────────────────
    COL_TOPS = Inches(1.05)
    COLS = [
        (Inches(0.22), Inches(3.8),  "PRIOR SYSTEM",         ACCENT_PURP),
        (Inches(4.18), Inches(4.8),  "WHAT IT LACKS",        ACCENT_RED),
        (Inches(9.14), Inches(4.0),  "CMatrix ADDRESSES BY", ACCENT_LIME),
    ]
    for cl, cw, label, clr in COLS:
        box(slide, cl, COL_TOPS, cw, Inches(0.32), fill=clr)
        txt(slide, label, cl + Inches(0.08), COL_TOPS + Inches(0.05), cw - Inches(0.12), Inches(0.24),
            size=9.5, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    # ── Rows ──────────────────────────────────────────────────────────────────
    rows = [
        (
            "PentestGPT\n(USENIX Sec '24)", ACCENT_CYAN,
            "Flat conversation history — no structured world model of the target. "
            "Task Tree records tasks, not discovered facts.",
            "ASG: a typed property graph of the target. Every discovered node is a "
            "first-class fact, not a sentence in history.",
        ),
        (
            "AutoAttacker\n(arXiv '24)", ACCENT_LIME,
            "Experience reuse within one session only. Resets to zero knowledge on "
            "every new mission. No cross-session learning.",
            "Cross-Mission Experience Store (C10) + Attack Strategy Library (C11): "
            "validated chains accumulate across all missions.",
        ),
        (
            "HPTSA / Teams of LLM Agents\n(arXiv '24)", ACCENT_GOLD,
            "No structured attack graph. Hierarchical delegation but no formal "
            "representation of which vulnerabilities chain together.",
            "APG AttackChain lifecycle (C3): attack paths are first-class entities "
            "with risk scores, priorities, and evidence links.",
        ),
        (
            "PentestAgent\n(AsiaCCS '25)", ACCENT_TEAL,
            "RAG shared memory conflates discovery facts with reasoning. "
            "Termination is task-queue empty — attack surface may still have unexplored nodes.",
            "Dual-graph separation (C1) + Dual termination (C8): both ASG exhaustion "
            "AND APG resolution required for mission close.",
        ),
        (
            "VulnBot\n(arXiv '25)", ACCENT_RED,
            "Five-module pipeline with no formal attack graph. Context compaction "
            "is ad-hoc. No lifecycle for attack chains.",
            "Lossless Context Compaction (C6): three-layer ASG-backed scheme preserves "
            "all discovered findings regardless of mission length.",
        ),
    ]

    ROW_START = COL_TOPS + Inches(0.36)
    ROW_H = (SLIDE_H - ROW_START - Inches(0.28)) / len(rows)

    for i, (system, sys_clr, lacks, addresses) in enumerate(rows):
        rt = ROW_START + i * ROW_H
        rh = ROW_H - Inches(0.06)
        bg = RGBColor(0x0E, 0x0C, 0x1A) if i % 2 == 0 else RGBColor(0x08, 0x0A, 0x14)

        # System column
        cl0, cw0 = Inches(0.22), Inches(3.8)
        box(slide, cl0, rt, cw0, rh, fill=bg, line_color=sys_clr, lw=0.8)
        box(slide, cl0, rt, Inches(0.06), rh, fill=sys_clr)
        txt(slide, system, cl0 + Inches(0.14), rt + Inches(0.06),
            cw0 - Inches(0.2), rh - Inches(0.1),
            size=10, bold=True, color=sys_clr, align=PP_ALIGN.LEFT, wrap=True)

        # Lacks column
        cl1, cw1 = Inches(4.18), Inches(4.8)
        box(slide, cl1, rt, cw1, rh, fill=bg, line_color=RGBColor(0x40, 0x10, 0x10), lw=0.5)
        txt(slide, lacks, cl1 + Inches(0.1), rt + Inches(0.06),
            cw1 - Inches(0.16), rh - Inches(0.1),
            size=9, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

        # CMatrix column
        cl2, cw2 = Inches(9.14), Inches(4.0)
        box(slide, cl2, rt, cw2, rh, fill=bg, line_color=RGBColor(0x10, 0x30, 0x10), lw=0.5)
        txt(slide, addresses, cl2 + Inches(0.1), rt + Inches(0.06),
            cw2 - Inches(0.16), rh - Inches(0.1),
            size=9, color=ACCENT_LIME, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "03", ACCENT_PURP)
