from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C_DIR = ROOT / "results" / "c"
ASM_DIR = ROOT / "results" / "asm"
DOC = ROOT / "results" / "compiler_gap.md"

BENCHMARKS = ("absval", "isolate_rmb", "popcount")
FLAG_SETS = (("base", "-march=x86-64"), ("v3", "-march=x86-64-v3"))
BEGIN = "<!-- gap-table:begin -->"
END = "<!-- gap-table:end -->"

SUPEROPT = {
    "absval": "**3** (proven)",
    "isolate_rmb": "**2** (proven)",
    "popcount": "no result (frontier)",
}


def count_instructions(asm: str) -> int:
    count = 0
    for raw in asm.splitlines():
        line = raw.split("#", 1)[0].split(";", 1)[0].strip()
        if not line or line.startswith(".") or line.endswith(":"):
            continue
        mnemonic = line.split(None, 1)[0]
        if mnemonic in ("ret", "retq"):
            continue
        count += 1
    return count


def _gcc_version() -> str:
    out = subprocess.run(
        ["gcc", "--version"], capture_output=True, text=True, check=True
    )
    return out.stdout.splitlines()[0]


def _compile(bench: str, tag: str, march: str) -> Path:
    src = C_DIR / f"{bench}.c"
    dest = ASM_DIR / f"gcc-{bench}-{tag}.s"
    subprocess.run(
        ["gcc", "-O3", march, "-S", "-o", str(dest), str(src)], check=True
    )
    return dest


def _count_snapshot(path: Path) -> int | None:
    if not path.exists():
        return None
    n = count_instructions(path.read_text())
    if n == 0:
        raise SystemExit(f"parsed zero instructions from {path}")
    return n


def _cell(n: int | None) -> str:
    return str(n) if n is not None else "—"


def _table() -> str:
    ASM_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        "| benchmark | gcc -O3 base | gcc -O3 v3 | clang -O3 base "
        "| clang -O3 v3 | superopt (proven minimum) |",
        "|---|---|---|---|---|---|",
    ]
    for bench in BENCHMARKS:
        cells = [bench]
        for tag, march in FLAG_SETS:
            path = _compile(bench, tag, march)
            cells.append(_cell(_count_snapshot(path)))
        for tag, _march in FLAG_SETS:
            cells.append(_cell(_count_snapshot(ASM_DIR / f"clang-{bench}-{tag}.s")))
        cells.append(SUPEROPT[bench])
        rows.append("| " + " | ".join(cells) + " |")
    rows.append("")
    rows.append(f"Local gcc: `{_gcc_version()}`. Counting rule: every")
    rows.append("instruction in the function body except `ret`; applied by")
    rows.append("`scripts/compiler_gap.py`, tested in `tests/test_compiler_gap.py`.")
    return "\n".join(rows)


def main() -> None:
    table = _table()
    if DOC.exists():
        text = DOC.read_text(encoding="utf-8")
        if BEGIN not in text or END not in text:
            raise SystemExit(f"{DOC} exists but lacks {BEGIN}/{END} markers")
        head, rest = text.split(BEGIN, 1)
        _mid, tail = rest.split(END, 1)
        text = f"{head}{BEGIN}\n{table}\n{END}{tail}"
    else:
        text = f"# Compiler gap\n\n{BEGIN}\n{table}\n{END}\n"
    DOC.write_text(text, encoding="utf-8")
    print(f"wrote {DOC}")


if __name__ == "__main__":
    sys.exit(main())
