"""
Slide 03 — Foundations & Inspirations
=======================================
Two-column layout: Academic Papers (left, 5 entries) + Open-Source Repos (right, 3 entries).
Each entry shows: name/venue, key mechanism borrowed, and the identified gap.
Matches presentation-final.pptx Slide 3.
"""
from palette import *


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, BG_DARK)
    chrome(slide, ACCENT_PURP)
    slide_header(slide, "FOUNDATIONS & INSPIRATIONS",
                 "Academic Papers + Open-Source Repositories That Shaped CMatrix",
                 ACCENT_PURP, title_size=26, divider_w=11)

    # ── Column layout ─────────────────────────────────────────────────────────
    COL_T  = Inches(1.08)
    LEFT_L, LEFT_W  = Inches(0.22), Inches(6.5)
    RIGHT_L, RIGHT_W = Inches(6.88), Inches(6.22)

    # Column headers
    box(slide, LEFT_L, COL_T, LEFT_W, Inches(0.3), fill=ACCENT_PURP)
    txt(slide, "📄  ACADEMIC PAPERS",
        LEFT_L + Inches(0.12), COL_T + Inches(0.05), LEFT_W - Inches(0.2), Inches(0.22),
        size=10, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    box(slide, RIGHT_L, COL_T, RIGHT_W, Inches(0.3), fill=RGBColor(0x30, 0x10, 0x60))
    txt(slide, "💻  OPEN-SOURCE REPOSITORIES",
        RIGHT_L + Inches(0.12), COL_T + Inches(0.05), RIGHT_W - Inches(0.2), Inches(0.22),
        size=10, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # ── Academic Papers (5 entries) ───────────────────────────────────────────
    papers = [
        (
            "1", "PentestGPT", "USENIX Security '24",
            ACCENT_CYAN,
            "Tripartite Reasoning / Generation / Parsing pipeline.\n"
            "Pentesting Task Tree as long-session context memory.",
            "Gap: Task Tree records tasks performed — not discovered facts. "
            "No structured target model; no representation of what can be done to it.",
        ),
        (
            "2", "AutoAttacker", "arXiv '24 — Xu et al.",
            ACCENT_LIME,
            "Modular planner / summarizer / code-generator for post-breach automation.\n"
            "Experience manager reuses attack subtasks within one mission.",
            "Gap: Experience reuse bounded to a single mission. "
            "Every new mission resets to zero knowledge — no cross-mission accumulation.",
        ),
        (
            "3", "Teams of LLM Agents (HPTSA)", "arXiv '24 — Zhu et al.",
            ACCENT_GOLD,
            "Hierarchical planner delegates to task-specific sub-agents.\n"
            "Task-specific document injection improves zero-day exploitation by 2.1x.",
            "Gap: No structured attack graph. No formal representation of which "
            "vulnerabilities chain together or how far a chain has been validated.",
        ),
        (
            "4", "PentestAgent", "AsiaCCS '25 — Shen et al.",
            ACCENT_TEAL,
            "Planning agent with RAG-backed shared memory.\n"
            "Execution agent self-diagnoses failed exploits before abandoning.",
            "Gap: RAG memory conflates discovery facts with reasoning hypotheses. "
            "Termination on empty task queue — attack surface may be unexplored.",
        ),
        (
            "5", "VulnBot", "arXiv '25 — Kong et al.",
            ACCENT_RED,
            "Five-module pipeline around a Penetration Task Graph.\n"
            "Summarizer condenses phase output to prevent history leakage.",
            "Gap: No formal attack graph. Context compaction is ad-hoc. "
            "No lifecycle for attack chains: no risk scoring or formal chain resolution.",
        ),
    ]

    CARD_T = COL_T + Inches(0.34)
    CARD_H = (SLIDE_H - CARD_T - Inches(0.22)) / len(papers)

    for i, (num, name, venue, clr, mechanism, gap) in enumerate(papers):
        ct = CARD_T + i * CARD_H
        ch = CARD_H - Inches(0.04)
        bg = RGBColor(0x0C, 0x08, 0x1A) if i % 2 == 0 else RGBColor(0x08, 0x06, 0x14)

        box(slide, LEFT_L, ct, LEFT_W, ch, fill=bg, line_color=clr, lw=0.8)
        box(slide, LEFT_L, ct, Inches(0.06), ch, fill=clr)

        # Number badge
        box(slide, LEFT_L + Inches(0.1), ct + Inches(0.06), Inches(0.26), Inches(0.26),
            fill=clr)
        txt(slide, num, LEFT_L + Inches(0.11), ct + Inches(0.07), Inches(0.24), Inches(0.22),
            size=8, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

        # Name + venue
        txt(slide, name, LEFT_L + Inches(0.42), ct + Inches(0.06),
            Inches(3.5), Inches(0.22),
            size=10, bold=True, color=clr, align=PP_ALIGN.LEFT)
        txt(slide, venue, LEFT_L + Inches(0.42), ct + Inches(0.26),
            Inches(3.5), Inches(0.18),
            size=8, color=GREY_MID, align=PP_ALIGN.LEFT)

        # Mechanism + gap (combined in remaining height)
        body = mechanism + "\n" + gap
        txt(slide, body, LEFT_L + Inches(0.1), ct + Inches(0.46),
            LEFT_W - Inches(0.18), ch - Inches(0.5),
            size=7.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    # ── Open-Source Repos (3 entries) ─────────────────────────────────────────
    repos = [
        (
            "6", "PentAGI", "vxcontrol/pentagi",
            ACCENT_PURP,
            "Production multi-agent pentesting platform.\n"
            "Adviser detects agent fixation; Reflector nudges stuck agents.",
            "Gap: Fixation detection is reactive — fires after repeated tool calls. "
            "No proactive graph-driven surface-exhaustion check.",
        ),
        (
            "7", "Claude Code", "Anthropic — yasasbanukaofficial/claude-code",
            ACCENT_CYAN,
            "Two-stage fast-filter + chain-of-thought tool-call permission classifier.\n"
            "27-event named hook architecture for operator intervention.",
            "Gap: Permission classification is general-purpose — not domain-aware. "
            "No offensive risk tier, scope enforcement, or security-intent routing.",
        ),
        (
            "8", "Hermes Agent", "NousResearch/hermes-agent",
            ACCENT_GOLD,
            "Closed learning loop: skill crystallization from completed tasks.\n"
            "Structured trajectory export for SFT/RL training via DSPy + Atropos.",
            "Gap: Skill crystallization and trajectory export are general-purpose. "
            "No security-domain indexing, APG integration, or dual-graph event format.",
        ),
    ]

    REPO_H = (SLIDE_H - CARD_T - Inches(0.22)) / len(repos)

    for i, (num, name, venue, clr, mechanism, gap) in enumerate(repos):
        ct = CARD_T + i * REPO_H
        ch = REPO_H - Inches(0.04)
        bg = RGBColor(0x10, 0x06, 0x1C) if i % 2 == 0 else RGBColor(0x0A, 0x04, 0x14)

        box(slide, RIGHT_L, ct, RIGHT_W, ch, fill=bg, line_color=clr, lw=0.8)
        box(slide, RIGHT_L, ct, Inches(0.06), ch, fill=clr)

        # Number badge
        box(slide, RIGHT_L + Inches(0.1), ct + Inches(0.06), Inches(0.26), Inches(0.26),
            fill=clr)
        txt(slide, num, RIGHT_L + Inches(0.11), ct + Inches(0.07), Inches(0.24), Inches(0.22),
            size=8, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

        # Name + venue
        txt(slide, name, RIGHT_L + Inches(0.42), ct + Inches(0.06),
            Inches(4.0), Inches(0.22),
            size=10, bold=True, color=clr, align=PP_ALIGN.LEFT)
        txt(slide, venue, RIGHT_L + Inches(0.42), ct + Inches(0.26),
            Inches(5.5), Inches(0.18),
            size=8, color=GREY_MID, align=PP_ALIGN.LEFT)

        # Body
        body = mechanism + "\n" + gap
        txt(slide, body, RIGHT_L + Inches(0.1), ct + Inches(0.46),
            RIGHT_W - Inches(0.18), ch - Inches(0.5),
            size=7.5, color=GREY_MID, align=PP_ALIGN.LEFT, wrap=True)

    slide_number(slide, "03", ACCENT_PURP)
