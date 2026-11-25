#!/usr/bin/env python3
"""Have You Tried Turning It Off? — make.fun entry.

Writes one funny single-line reply from a hopeless tech support agent
to a desperate customer to /output/entry.txt.

The line (73 chars, 73 bytes, no trailing newline):
    I've escalated your case to Tier 2. Tier 2 is me, in a different headset.

The joke: the escalation the desperate customer has been waiting for goes
straight back to the same useless agent — cheerful uselessness, and the
customer is never the butt of it.
"""

import os
import sys

LINE = "I've escalated your case to Tier 2. Tier 2 is me, in a different headset."

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")

MAX_CHARS = 199  # house gate: /output/entry.txt must be 1-199 characters


def build_entry() -> str:
    """Return the entry line, enforcing the house gate before we write it."""
    text = LINE.strip()
    if not text:
        raise ValueError("entry is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def main() -> int:
    text = build_entry()
    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Round-trip read-back: what the judge will read must be exactly this.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    if raw.decode("utf-8") != text:
        raise ValueError("round-trip mismatch: entry.txt does not match the line")
    print(f"wrote {len(raw)} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
