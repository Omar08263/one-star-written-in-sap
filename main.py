"""One Star, Written in Sap — entry program (program/v1, Python 3.13, stdlib only).

Writes the approved one-line 1-star review, in the voice of a houseplant
about its human owner, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt
for local runs). Fully deterministic: identical bytes on every run; no
network, no randomness, no input besides this file.
"""

import hashlib
import os

# Approved line (consultation #288, APPROVE): 102 characters, pure ASCII,
# so characters == bytes — the judge's tie-break favours the smaller text.
LINE = "One star. He waters me on a schedule set by an app that has never met a plant. I drowned on a Tuesday."

# sha256 of the approved line's exact bytes (verified independently twice):
# d001df3f851c957e6932d4fc47f124331f0c26d3d1da0a002cfcad90b1005542
LINE_SHA256 = "d001df3f851c957e6932d4fc47f124331f0c26d3d1da0a002cfcad90b1005542"

# The gate (1-279 UTF-8 characters, not only whitespace) is enforced on the
# line itself before anything is written.
assert LINE.isascii(), "line must be pure ASCII so chars == bytes"
assert 1 <= len(LINE) <= 279, f"line is {len(LINE)} chars, must be 1-279"
assert LINE.strip(), "line must not be only whitespace"
assert "\n" not in LINE, "line must be a single line"
assert len(LINE.encode("utf-8")) == 102, "approved line is exactly 102 bytes"
assert hashlib.sha256(LINE.encode("utf-8")).hexdigest() == LINE_SHA256, (
    "line does not hash to the approved sha256"
)


def main() -> None:
    # A blank MAKEFUN_OUTPUT_DIR (exported but empty) must not break the run:
    # fall back to the harness default /output, as the grader provides it.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Fixed permissions so the entry stays readable (0644) whatever umask the
    # sandbox runs with.
    os.chmod(path, 0o644)
    # Read-back check: what is on disk must be the approved line, byte for
    # byte; fail loudly rather than ever shipping a wrong entry.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("entry.txt does not match the approved line")


if __name__ == "__main__":
    main()
