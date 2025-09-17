#!/usr/bin/env python3
"""
Update README.md with links to existing docs and hardware assets.
Idempotent: only rewrites the block between markers.

Markers in README.md:
  <!-- AUTOLINKS:BEGIN -->
  ... generated content ...
  <!-- AUTOLINKS:END -->

Usage:
  python scripts/update_readme_links.py            # writes README.md
  python scripts/update_readme_links.py --check    # exits 1 if changes needed
"""
import sys
import os
from pathlib import Path
from urllib.parse import quote

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

def md_link(path: Path, label: str | None = None) -> str:
    rel = path.as_posix()
    href = quote(rel, safe="/._-")
    return f"[{label or path.name}]({href})"

def gather_docs():
    items = []
    if DOCS.exists():
        for p in sorted(DOCS.glob("*.md")):
            label = FRIENDLY.get(p.name) or p.stem.replace("_", " ").replace("-", " ").title()
            items.append(f"- **{label}:** {md_link(p)}")
    for name in ("LICENSE", "CHANGELOG.md", "CODEOWNERS"):
        p = ROOT / name
        if p.exists():
            items.append(f"- **{FRIENDLY.get(name, name)}:** {md_link(p)}")
    return items

def gather_hw():
    items = []
    fritz = HW / "fritzing"
    encl = HW / "enclosure"
    bom = HW / "BOM.csv"
    if fritz.exists():
        for p in sorted(fritz.glob("*.fzz")):
            items.append(f"- **Fritzing design (.fzz):** {md_link(p)}")
    if encl.exists():
        items.append(f"- **Enclosure (3D models):** {md_link(encl)}")
    if bom.exists():
        items.append(f"- **{FRIENDLY['BOM.csv']}:** {md_link(bom)}")
    return items

def build_block() -> str:
    doc_lines = gather_docs()
    hw_lines = gather_hw()

    out = []
    out.append("## Reference & Docs")
    seen = set()
    for line in doc_lines:
        if line not in seen:
            out.append(line)
            seen.add(line)
    if hw_lines:
        out.append("")
        out.append("### Hardware")
        for line in hw_lines:
            if line not in seen:
                out.append(line)
                seen.add(line)
    return "\n".join(out) + "\n"

def main():
    block = build_block()
    if not README.exists():
        print("README.md not found", file=sys.stderr)
        sys.exit(2)
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
        print("README.md links up to date.")
        return

    if new_txt != txt:
        README.write_text(new_txt, encoding="utf-8")
        print("README.md updated.")
    else:
        print("README.md already up to date.")

if __name__ == "__main__":
    main()
