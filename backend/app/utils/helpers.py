"""Helper utilities for the application."""

import re


def clean_response(content: str) -> str:
    """Clean up the response by removing tool call syntax and extra whitespace."""
    if not content:
        return ""

    # Remove TOOL_CALL lines
    lines = content.split("\n")
    cleaned_lines = []
    skip_next = False

    for line in lines:
        # Skip TOOL_CALL lines
        if re.match(r"^\s*TOOL_CALL:", line, re.IGNORECASE):
            continue
        # Skip TOOL_RESULTS section header
        if re.match(r"^\s*TOOL_RESULTS:", line, re.IGNORECASE):
            skip_next = True
            continue
        # Skip the instruction line after TOOL_RESULTS
        if skip_next and "provide your final answer" in line.lower():
            skip_next = False
            continue

        cleaned_lines.append(line)

    # Join and clean up extra whitespace
    result = "\n".join(cleaned_lines)
    result = re.sub(r"\n{3,}", "\n\n", result)  # Max 2 consecutive newlines
    result = result.strip()

    return result


import string


def normalize_text(text: str) -> str:
    """
    Normalize text by removing whitespace, punctuation and converting to lowercase.

    Args:
        text: Input text

    Returns:
        Normalized text
    """
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remove all whitespace
    text = "".join(text.split())
    return text
