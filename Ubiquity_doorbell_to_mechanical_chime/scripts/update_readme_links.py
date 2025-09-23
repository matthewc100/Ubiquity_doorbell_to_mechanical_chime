#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
readme = ROOT / "README.md"

docs = [
    ("Firewall (UFW) hardening", ROOT/"docs/FIREWALL.md"),
    ("Operations (service, logs, updates)", ROOT/"docs/OPERATIONS.md"),
    ("UniFi Protect setup", ROOT/"docs/UNIFI-PROTECT.md"),
    ("Project log", ROOT/"docs/PROJECT_LOG.md"),
    ("License", ROOT/"LICENSE"),
    ("Changelog", ROOT/"CHANGELOG.md"),
    ("Codeowners", ROOT/"CODEOWNERS"),
]

hardware = [
    ("Fritzing design (.fzz)", ROOT/"hardware/fritzing/Front Door chime.fzz"),
    ("Enclosure (3D models)", ROOT/"hardware/enclosure"),
    ("Bill of Materials", ROOT/"hardware/BOM.csv"),
]

BEGIN = "<!-- AUTOLINKS:BEGIN -->"
END = "<!-- AUTOLINKS:END -->"

def make_rel(p: Path) -> str:
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()

def build_block() -> str:
    lines = ["## Reference & Docs"]
    for label, path in docs:
        lines.append(f"- **{label}:** [{path.name}]({make_rel(path)})")
    lines.append("")
    lines.append("### Hardware")
    for label, path in hardware:
        display = path.name if path.is_file() else path.name
        lines.append(f"- **{label}:** [{display}]({make_rel(path)})")
    return "\n".join(lines)

def main():
    text = readme.read_text(encoding="utf-8")
    block = build_block()
    if BEGIN in text and END in text:
        before, rest = text.split(BEGIN, 1)
        _, after = rest.split(END, 1)
        new = before + BEGIN + "\n" + block + "\n" + END + after
    else:
        new = text.rstrip() + "\n\n" + BEGIN + "\n" + block + "\n" + END + "\n"
    readme.write_text(new, encoding="utf-8")
    print("README.md updated.")

if __name__ == "__main__":
    sys.exit(main())
