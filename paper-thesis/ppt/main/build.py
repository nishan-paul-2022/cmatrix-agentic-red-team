#!/usr/bin/env python3
"""
build.py — CMatrix Presentation Builder
============================================
Usage:
    python3 build.py              # builds to default output path
    python3 build.py out.pptx     # builds to custom path

How it works
------------
1. Discovers every  slide_*.py  file in this directory, sorted by filename.
2. Imports each module and calls  module.build_slide(prs).
3. Saves the final Presentation to OUTPUT_PATH.

Adding a slide:   create slide_N.py with a build_slide(prs) function.
Removing a slide: delete (or rename) the corresponding slide_*.py file.
Reordering:       rename files so the numeric prefix reflects the desired order.
"""
import sys
import os
import glob
import re
import importlib.util

# ── Configuration ─────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCRIPT_DIR, "presentation.pptx")

# ── Imports ───────────────────────────────────────────────────────────────────
from pptx import Presentation
from pptx.util import Inches

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def discover_slides(directory: str) -> list[str]:
    """Return numerically sorted list of slide_*.py file paths."""
    pattern = os.path.join(directory, "slide_*.py")
    paths = glob.glob(pattern)
    if not paths:
        raise FileNotFoundError(f"No slide_*.py files found in: {directory}")
        
    def sort_key(path):
        basename = os.path.basename(path)
        match = re.search(r'\d+', basename)
        return int(match.group()) if match else 0
        
    return sorted(paths, key=sort_key)


def load_module(filepath: str):
    """Dynamically import a Python file as a module."""
    name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    # Make the slide directory importable (for `from palette import *`)
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    spec.loader.exec_module(module)
    return module


def build(output_path: str):
    slides = discover_slides(SCRIPT_DIR)

    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║  CMatrix Presentation Builder                    ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  Found {len(slides):2d} slide module(s)                      ║")
    print(f"╚══════════════════════════════════════════════════╝")
    print()

    # Create presentation with correct dimensions
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H

    for i, filepath in enumerate(slides, start=1):
        name = os.path.basename(filepath)
        print(f"  [{i:02d}/{len(slides):02d}]  Building  {name} ...", end="", flush=True)
        try:
            module = load_module(filepath)
            if not hasattr(module, "build_slide"):
                print(f"  ⚠  SKIP — no build_slide() function found")
                continue
            module.build_slide(prs)
            print(f"  ✓")
        except Exception as exc:
            print(f"\n         ✗  ERROR: {exc}")
            raise

    prs.save(output_path)
    print()
    print(f"  ✅  Saved → {output_path}")
    print(f"      Slides: {len(prs.slides)}")


if __name__ == "__main__":
    build(OUTPUT_PATH)
