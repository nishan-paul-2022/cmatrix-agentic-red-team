# CMatrix Presentation Build System
# ==================================
# Usage:
#   make ppt           — build presentation (default output)
#   make ppt OUT=my.pptx — build to custom path
#   make clean         — remove generated PPTX
#   make list          — list all slide modules in build order
#   make check         — verify all slide_*.py have build_slide()

PYTHON      ?= python3
BUILD_SCRIPT = main/build.py
OUTPUT      ?= presentation.pptx
PPT_DIR     := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: ppt clean list check help

## Build the presentation
ppt:
	@cd "$(PPT_DIR)" && $(PYTHON) $(BUILD_SCRIPT) $(OUTPUT)

## Remove the generated PPTX
clean:
	@rm -f "$(PPT_DIR)$(OUTPUT)"
	@echo "  🗑  Removed $(OUTPUT)"

## List all slide modules in build order
list:
	@echo "Slide modules (build order):"
	@ls "$(PPT_DIR)"main/slide_*.py 2>/dev/null | sort -V | nl -ba | \
	  awk '{printf "  %s  %s\n", $$1, $$2}'

## Verify all slide_*.py files have a build_slide() function
check:
	@echo "Checking slide modules..."
	@ok=0; fail=0; \
	for f in $$(ls -v "$(PPT_DIR)"main/slide_*.py 2>/dev/null); do \
	  if grep -q "def build_slide" "$$f"; then \
	    echo "  ✓  $$(basename $$f)"; ok=$$((ok+1)); \
	  else \
	    echo "  ✗  $$(basename $$f)  — missing build_slide()"; fail=$$((fail+1)); \
	  fi; \
	done; \
	echo ""; \
	echo "  OK: $$ok   FAIL: $$fail"

## Print help
help:
	@echo ""
	@echo "  CMatrix PPT Build System"
	@echo "  ─────────────────────────────────────────"
	@echo "  make ppt              Build the presentation"
	@echo "  make ppt OUT=x.pptx  Build to custom filename"
	@echo "  make clean            Remove generated PPTX"
	@echo "  make list             List slide modules in order"
	@echo "  make check            Verify all slides have build_slide()"
	@echo ""
	@echo "  Workflow:"
	@echo "    • Edit any main/slide_N.py to change a slide"
	@echo "    • Add main/slide_N.py with build_slide(prs) to add a slide"
	@echo "    • Delete or rename a main/slide_*.py to remove it"
	@echo "    • Run  make ppt  to regenerate"
	@echo ""
