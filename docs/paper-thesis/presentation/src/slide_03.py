"""
Slide 3 — Foundations & Inspirations
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_PURP)

    # Header
    txt(slide, "FOUNDATIONS & INSPIRATIONS", Inches(0.3), Inches(0.07), Inches(8), Inches(0.26),
        size=10, bold=True, color=ACCENT_PURP, align=PP_ALIGN.LEFT)
    txt(slide, "Academic Papers + Open-Source Repositories That Shaped CMatrix",
        Inches(0.3), Inches(0.32), Inches(12.5), Inches(0.52),
        size=26, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # Slide number badge (top-right, as in original)
    txt(slide, "03", SLIDE_W - Inches(0.55), Inches(0.05), Inches(0.52), Inches(0.45),
        size=20, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)

    # Column headers
    col_l_l = Inches(0.3)
    col_r_l = Inches(6.83)
    col_w = Inches(6.3)
    hdr_t = Inches(0.9)

    # Left header: Academic Papers
    box(slide, col_l_l, hdr_t, col_w, Inches(0.32), fill=GREY_DARK)
    txt(slide, "\u2399  ACADEMIC PAPERS", col_l_l + Inches(0.1), hdr_t + Inches(0.03),
        col_w - Inches(0.2), Inches(0.26), size=11, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # Right header: Open-Source Repositories
    box(slide, col_r_l, hdr_t, col_w, Inches(0.32), fill=GREY_DARK)
    txt(slide, "\U0001f4bb  OPEN-SOURCE REPOSITORIES", col_r_l + Inches(0.1), hdr_t + Inches(0.03),
        col_w - Inches(0.2), Inches(0.26), size=11, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # ── Left column: 5 academic papers ────────────────────────────────────────
    papers = [
        ("1", "PentestGPT", "USENIX Security '24",
         "Tripartite Reasoning / Generation / Parsing pipeline.\nPentesting Task Tree as long-session context memory.",
         "Gap: Task Tree records tasks performed — not discovered facts. No structured target model; no representation of what can be done to it."),
        ("2", "AutoAttacker", "arXiv '24 — Xu et al.",
         "Modular planner / summarizer / code-generator for post-breach automation.\nExperience manager reuses attack subtasks within one mission.",
         "Gap: Experience reuse bounded to a single mission. Every new mission resets to zero knowledge — no cross-mission accumulation."),
        ("3", "Teams of LLM Agents (HPTSA)", "arXiv '24 — Zhu et al.",
         "Hierarchical planner delegates to task-specific sub-agents.\nTask-specific document injection improves zero-day exploitation by 2.1x.",
         "Gap: No structured attack graph. No formal representation of which vulnerabilities chain together or how far a chain has been validated."),
        ("4", "PentestAgent", "AsiaCCS '25 — Shen et al.",
         "Planning agent with RAG-backed shared memory.\nExecution agent self-diagnoses failed exploits before abandoning.",
         "Gap: RAG memory conflates discovery facts with reasoning hypotheses. Termination on empty task queue — attack surface may be unexplored."),
        ("5", "VulnBot", "arXiv '25 — Kong et al.",
         "Five-module pipeline around a Penetration Task Graph.\nSummarizer condenses phase output to prevent history leakage.",
         "Gap: No formal attack graph. Context compaction is ad-hoc. No lifecycle for attack chains: no risk scoring or formal chain resolution."),
    ]

    card_t = Inches(1.28)
    card_h = Inches(1.19)
    card_gap = Inches(0.04)
    num_w = Inches(0.38)
    CARD_LEFT_BG = RGBColor(0x10, 0x16, 0x2B)
    GAP_COLOR = RGBColor(0x22, 0x28, 0x3A)

    for i, (num, title, venue, body, gap) in enumerate(papers):
        top = card_t + i * (card_h + card_gap)
        box(slide, col_l_l, top, col_w, card_h, fill=CARD_LEFT_BG, line_color=RGBColor(0x30, 0x38, 0x50), lw=0.8)
        # Number badge
        box(slide, col_l_l, top, num_w, card_h, fill=GAP_COLOR)
        txt(slide, num, col_l_l + Inches(0.01), top + Inches(0.38), num_w - Inches(0.02), Inches(0.36),
            size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        # Content
        cx = col_l_l + num_w + Inches(0.1)
        cw = col_w - num_w - Inches(0.15)
        txt(slide, title, cx, top + Inches(0.04), cw, Inches(0.24),
            size=11, bold=True, color=ACCENT_LIME, align=PP_ALIGN.LEFT)
        txt(slide, venue, cx, top + Inches(0.27), cw, Inches(0.18),
            size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)
        txt(slide, body, cx, top + Inches(0.44), cw, Inches(0.34),
            size=8.5, color=WHITE, align=PP_ALIGN.LEFT, wrap=True)
        txt(slide, gap, cx, top + Inches(0.75), cw, Inches(0.40),
            size=8, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT, wrap=True)

    # ── Right column: 3 open-source repos ─────────────────────────────────────
    repos = [
        ("6", "PentAGI", "vxcontrol/pentagi",
         "Production multi-agent pentesting platform.\nAdviser detects agent fixation; Reflector nudges stuck agents.",
         "Gap: Fixation detection is reactive — fires after repeated tool calls. No proactive graph-driven surface-exhaustion check."),
        ("7", "Claude Code", "Anthropic — yasasbanukaofficial/claude-code",
         "Two-stage fast-filter + chain-of-thought tool-call permission classifier.\n27-event named hook architecture for operator intervention.",
         "Gap: Permission classification is general-purpose — not domain-aware. No offensive risk tier, scope enforcement, or security-intent routing."),
        ("8", "Hermes Agent", "NousResearch/hermes-agent",
         "Closed learning loop: skill crystallization from completed tasks.\nStructured trajectory export for SFT/RL training via DSPy + Atropos.",
         "Gap: Skill crystallization and trajectory export are general-purpose. No security-domain indexing, APG integration, or dual-graph event format."),
    ]

    repo_card_h = Inches(1.99)
    CARD_RIGHT_BG = RGBColor(0x0C, 0x18, 0x28)

    for i, (num, title, venue, body, gap) in enumerate(repos):
        top = card_t + i * (repo_card_h + card_gap)
        box(slide, col_r_l, top, col_w, repo_card_h, fill=CARD_RIGHT_BG, line_color=ACCENT_CYAN, lw=0.8)
        # Number badge
        box(slide, col_r_l, top, num_w, repo_card_h, fill=RGBColor(0x04, 0x14, 0x28))
        txt(slide, num, col_r_l + Inches(0.01), top + Inches(0.82), num_w - Inches(0.02), Inches(0.36),
            size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        # Content
        cx = col_r_l + num_w + Inches(0.1)
        cw = col_w - num_w - Inches(0.15)
        txt(slide, title, cx, top + Inches(0.08), cw, Inches(0.28),
            size=13, bold=True, color=ACCENT_CYAN, align=PP_ALIGN.LEFT)
        txt(slide, venue, cx, top + Inches(0.36), cw, Inches(0.20),
            size=8.5, italic=True, color=GREY_MID, align=PP_ALIGN.LEFT)
        txt(slide, body, cx, top + Inches(0.56), cw, Inches(0.50),
            size=9, color=WHITE, align=PP_ALIGN.LEFT, wrap=True)
        txt(slide, gap, cx, top + Inches(1.1), cw, Inches(0.80),
            size=8.5, italic=True, color=ACCENT_GOLD, align=PP_ALIGN.LEFT, wrap=True)
