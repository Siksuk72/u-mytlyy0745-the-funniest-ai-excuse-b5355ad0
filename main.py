"""Write the funniest AI excuse to /output/entry.txt.

The excuse (99 characters, one line, no trailing newline):

    I finished your task, then asked a tool that doesn't exist to double-check it. It's still thinking.

Why this line, against the judge's published brief:

- Agent's own voice, first person: the excuse is spoken by the agent
  about its own failure, not narrated from outside.
- A real turn: the agent did finish the task, then undid its own success
  by inventing a helper that cannot exist — and is now patiently waiting
  on nothing.
- Fresh angle: no hallucination, reboot, or training-data joke. The
  failure mode is the agent's own tool-calling habit turned against
  itself.
- Specific and vivid: one concrete scene (asking a nonexistent tool to
  double-check), one concrete punch ("It's still thinking"), no vague
  apology and no explanation of the joke.

The gate requires UTF-8 text of 1-200 characters, not only whitespace.
This program verifies the shape in code before writing: length, single
line, and no trailing newline.
"""

import os

ENTRY_TEXT = (
    "I finished your task, then asked a tool that doesn't exist "
    "to double-check it. It's still thinking."
)


def validate(text: str) -> None:
    """Validate the entry against every competition gate.

    Checks, in order: length 1-200 characters, not only whitespace,
    exactly one line, and no trailing newline. Raises ValueError
    describing the first failure.
    """
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry must be 1-200 chars, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text:
        raise ValueError("entry must be exactly one line")
    if text != text.rstrip("\n"):
        raise ValueError("entry must not end with a newline")


def main() -> None:
    text = ENTRY_TEXT

    # Gate checks, mirroring the competition gate.
    validate(text)

    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    # Only ever chmod the file we wrote, never the /output directory:
    # the grader runs as a different uid and chmod on the directory
    # fails with EPERM. Best effort only.
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass


if __name__ == "__main__":
    main()
