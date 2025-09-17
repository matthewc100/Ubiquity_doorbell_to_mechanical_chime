#!/usr/bin/env python3
"""
update_readme_links.py (v4)

- Forces **relative** links using os.path.relpath() from repo root
- Works on Windows/OneDrive paths
- Idempotent block between markers is owned by this script

Markers in README.md:
  <!-- AUTOLINKS:BEGIN -->
  ... generated content ...
  <!-- AUTOLINKS:END -->

Usage:
  python scripts/update_readme_links.py            # writes README.md
  python scripts/update_readme_links.py --check    # exits 1 if changes needed
  python scripts/update_readme_links.py --verbose  # prints discovered files
  python scripts/update_readme_links.py --version  # prints script version
"""
import sys, os
from pathlib import Path
from urllib.parse import quote

VERSION = "v4"
ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
DOCS = ROOT / "docs"
HW = ROOT / "hardware"
BEGIN = "<!-- AUTOLINKS:BEGIN -->"
END = "<!-- AUTOLINKS:END -->"

FRIENDLY = {
    "UNIFI-PROTECT.md": "UniFi Protect setup",
    "FIREWALL.md": "Firewall (UFW) hardening",
    "OPERATIONS.md": "Operations (service, logs, updates)",
    "PROJECT_LOG.md": "Project log",
    "CHANGELOG.md": "Changelog",
    "LICENSE": "License",
    "CODEOWNERS": "Codeowners",
    "BOM.csv": "Bill of Materials",
}

def to_relative_href(path: Path) -> str:
    """
    Return a POSIX-style relative path from ROOT to `path`, URL-encoded.
    Fallback to filename if paths are on different drives (Windows edge case).
    """
    try:
        rel = os.path.relpath(str(path), start=str(ROOT))
    except Exception:
        rel = path.name  # last-resort fallback
    # Normalize to POSIX-style separators
    rel_posix = rel.replace("\\", "/")
    # If something weird still leaked an absolute path with a colon, keep only the filename
    if ":" in rel_posix:
        rel_posix = path.name
    return quote(rel_posix, safe="/._-")

def md_link(path: Path, label: str | None = None) -> str:
    return f"[{label or path.name}]({to_relative_href(path)})"

def label_for(p: Path) -> str:
    return FRIENDLY.get(p.name) or p.stem.replace("_", " ").replace("-", " ").title()

def gather_docs(verbose=False):
    items, found = [], []
    if DOCS.exists():
        for p in sorted(DOCS.rglob("*.md")):
            found.append(p); items.append(f"- **{label_for(p)}:** {md_link(p)}")
    for name in ("LICENSE", "CHANGELOG.md", "CODEOWNERS"):
        p = ROOT / name
        if p.exists():
            found.append(p); items.append(f"- **{label_for(p)}:** {md_link(p)}")
    if verbose:
        print("Docs discovered:"); [print("  -", x.as_posix()) for x in found]
    return items

def gather_hw(verbose=False):
    items, found = [], []
    fritz = HW / "fritzing"
    encl = HW / "enclosure"
    bom = HW / "BOM.csv"
    if fritz.exists():
        for p in sorted(fritz.glob("*.fzz")):
            found.append(p); items.append(f"- **Fritzing design (.fzz):** {md_link(p)}")
    if encl.exists():
        found.append(encl); items.append(f"- **Enclosure (3D models):** {md_link(encl)}")
    if bom.exists():
        found.append(bom); items.append(f"- **{FRIENDLY['BOM.csv']}:** {md_link(bom)}")
    if verbose:
        print("Hardware discovered:"); [print("  -", x.as_posix()) for x in found]
    return items

def build_block(verbose=False) -> str:
    doc_lines = gather_docs(verbose=verbose)
    hw_lines = gather_hw(verbose=verbose)
    out, seen = [], set()
    out.append("## Reference & Docs")
    for line in doc_lines:
        if line not in seen:
            out.append(line); seen.add(line)
    if hw_lines:
        out.append(""); out.append("### Hardware")
        for line in hw_lines:
            if line not in seen:
                out.append(line); seen.add(line)
    return "\n".join(out) + "\n"

def main():
    if "--version" in sys.argv:
        print(VERSION); return
    verbose = "--verbose" in sys.argv
    block = build_block(verbose=verbose)
    if not README.exists():
        print("README.md not found", file=sys.stderr); sys.exit(2)
    txt = README.read_text(encoding="utf-8")

    if BEGIN in txt and END in txt:
        pre, rest = txt.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        new_txt = pre + BEGIN + "\n" + block + END + post
    else:
        new_txt = txt.rstrip() + "\n\n" + BEGIN + "\n" + block + END + "\n"

    if "--check" in sys.argv:
        if new_txt != txt:
            print("README.md is out of date; run: python scripts/update_readme_links.py")
            sys.exit(1)
        print("README.md links up to date."); return

    if new_txt != txt:
        README.write_text(new_txt, encoding="utf-8")
        print("README.md updated.")
    else:
        print("README.md already up to date.")

if __name__ == "__main__":
    main()
