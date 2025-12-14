#!/usr/bin/env python3
# cf_runner.py — sample tester for Codeforces contest folders (with color)
import argparse, os, sys, subprocess, time, difflib, shutil, re
from pathlib import Path

DEF_TIMEOUT = 2.0

# -------------------- color helpers --------------------
class _Colors:
    def __init__(self, enabled: bool):
        self.enabled = enabled
        self.reset = "\x1b[0m" if enabled else ""
        def sty(code): return (lambda s: f"\x1b[{code}m{s}{self.reset}" if enabled else s)
        def col(code): return (lambda s: f"\x1b[{code}m{s}{self.reset}" if enabled else s)
        # styles
        self.bold = sty("1")
        self.dim  = sty("2")
        # colors
        self.red     = col("31")
        self.green   = col("32")
        self.yellow  = col("33")
        self.blue    = col("34")
        self.magenta = col("35")
        self.cyan    = col("36")
        self.gray    = col("90")

    def status(self, tag: str):
        if tag == "AC":  return self.green(self.bold("✓ AC"))
        if tag == "WA":  return self.red(self.bold("✗ WA"))
        if tag == "RE":  return self.red(self.bold("💥 RE"))
        if tag == "TLE": return self.yellow(self.bold("⏱ TLE"))
        return tag

def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()

# -------------------- file helpers --------------------
def find_problem_dir(root: Path, key: str) -> Path | None:
    for p in sorted(root.iterdir()):
        if p.is_dir():
            if p.name == key or p.name.startswith(f"{key}."):
                return p
    return None

def list_sample_pairs(samples_dir: Path):
    pairs = []
    if not samples_dir.exists():
        return pairs
    def key_of(p):
        m = re.search(r"(\d+)$", p.stem)
        return int(m.group(1)) if m else 0
    ins = sorted(samples_dir.glob("*.in"), key=key_of)
    for i in ins:
        m = re.search(r"(\d+)$", i.stem)
        num = m.group(1) if m else "1"
        out = samples_dir / f"{num}.out"
        if out.exists():
            pairs.append((i, out))
    return pairs

def normalize_lines(s: str, mode: str):
    if mode == "exact":
        return s.splitlines(keepends=False)
    if mode == "ws":
        lines = [line.rstrip() for line in s.splitlines()]
        while lines and lines[-1] == "":
            lines.pop()
        return lines
    if mode == "tokens":
        return s.split()
    raise ValueError("bad compare mode")

def run_proc(cmd, input_bytes: bytes, cwd: Path, timeout: float):
    try:
        start = time.monotonic()
        p = subprocess.run(
            cmd, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=str(cwd), timeout=timeout, check=False
        )
        dur = time.monotonic() - start
        return ("OK", p.returncode, p.stdout, p.stderr, dur)
    except subprocess.TimeoutExpired as e:
        return ("TLE", None, e.stdout or b"", e.stderr or b"", timeout)
    except Exception as e:
        return ("RE", None, b"", str(e).encode(), 0.0)

def build_cmd(problem_dir: Path, lang: str):
    if lang == "py":
        preferred = problem_dir / (problem_dir.name.split(".")[0] + ".py")
        src = preferred if preferred.exists() else (problem_dir / "A.py")
        if not src.exists():
            raise FileNotFoundError("Python file not found (expected *.py)")
        return (["python3", str(src)], None)
    elif lang == "java":
        src = problem_dir / "Main.java"
        if not src.exists():
            raise FileNotFoundError("Main.java not found")
        class_file = problem_dir / "Main.class"
        if (not class_file.exists()) or (class_file.stat().st_mtime < src.stat().st_mtime):
            javac = shutil.which("javac") or "javac"
            cp = subprocess.run([javac, "--release", "21", "-encoding", "UTF-8", str(src)],
                                cwd=str(problem_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if cp.returncode != 0:
                sys.stderr.write(cp.stderr.decode(errors="ignore"))
                raise RuntimeError("javac failed")
        java = shutil.which("java") or "java"
        return ([java, "-Xms64m", "-Xmx1024m", "Main"], None)
    else:
        raise ValueError("lang must be py or java")

def judge_problem(problem_dir: Path, lang: str, timeout: float, mode: str, show_diff: int, colors: _Colors):
    samples = list_sample_pairs(problem_dir / "samples")
    if not samples:
        print(colors.yellow(f"[{problem_dir.name}] no samples/ found"))
        return 0, 0

    header = f"[{problem_dir.name}] {lang.upper()}  cases={len(samples)}  timeout={timeout}s  mode={mode}"
    print(colors.cyan(colors.bold(header)))

    cmd, _ = build_cmd(problem_dir, lang)
    passed = 0
    for i, (fin, fout) in enumerate(samples, 1):
        input_bytes = fin.read_bytes()
        expected = fout.read_text(encoding="utf-8", errors="ignore")
        status, code, out, err, dur = run_proc(cmd, input_bytes, problem_dir, timeout)
        actual = out.decode("utf-8", errors="ignore")

        tag = status if status != "OK" else ("OK" if code == 0 else "RE")
        if tag == "OK":
            expN = normalize_lines(expected, mode)
            actN = normalize_lines(actual, mode)
            ok = (expN == actN)
            if ok:
                print(f"  #{i}: {colors.status('AC')}  {colors.gray(f'({dur:.3f}s)')}")
                passed += 1
            else:
                print(f"  #{i}: {colors.status('WA')}  {colors.gray(f'({dur:.3f}s)')}")
                if mode == "tokens":
                    diff = list(difflib.unified_diff(expN, actN, lineterm=""))
                else:
                    diff = list(difflib.unified_diff(expN, actN, fromfile='exp', tofile='act', lineterm=""))
                shown = 0
                for line in diff:
                    if shown >= show_diff: break
                    if line.startswith('---') or line.startswith('+++'):
                        print("       ", colors.dim(line))
                    elif line.startswith('@@'):
                        print("       ", colors.cyan(line))
                    elif line.startswith('-'):
                        print("       ", colors.red(line))
                    elif line.startswith('+'):
                        print("       ", colors.green(line))
                    else:
                        print("       ", line[:200])
                    shown += 1
        elif tag == "TLE":
            print(f"  #{i}: {colors.status('TLE')} {colors.gray(f'({dur:.3f}s)')}")
        else:  # RE
            msg = (err or b"").decode(errors="ignore").strip()
            short = msg.splitlines()[0] if msg else ""
            print(f"  #{i}: {colors.status('RE')}  {colors.gray(f'({dur:.3f}s)')}  {colors.dim(short[:160])}")

    total = len(samples)
    summary = f"==> Passed {passed}/{total}"
    if passed == total and total > 0:
        print(colors.green(colors.bold(summary)))
    else:
        print(colors.red(colors.bold(summary)))
    return passed, total

def autodetect_lang(problem_dir: Path, prefer: str | None):
    if prefer in ("py","java"):
        return prefer
    has_py = any(problem_dir.glob("*.py"))
    has_java = (problem_dir / "Main.java").exists()
    if has_py: return "py"
    if has_java: return "java"
    return "py"

def main():
    ap = argparse.ArgumentParser(description="Run Codeforces samples (colorized)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("test", help="run samples")
    t.add_argument("which", nargs="?", help="problem letter (A,B,...) or directory; omit with --all")
    t.add_argument("--all", action="store_true", help="run all problems with samples/")
    t.add_argument("--lang", choices=["py","java"], help="force language")
    t.add_argument("--timeout", type=float, default=DEF_TIMEOUT)
    t.add_argument("--mode", choices=["exact","ws","tokens"], default="ws")
    t.add_argument("--show-diff", type=int, default=3)
    t.add_argument("--color", choices=["auto","always","never"], default="auto",
                   help="color output (default: auto)")

    args = ap.parse_args()

    if args.color == "always":
        colors = _Colors(True)
    elif args.color == "never":
        colors = _Colors(False)
    else:
        colors = _Colors(_supports_color())

    root = Path(__file__).resolve().parent
    if args.cmd == "test":
        targets = []
        if args.all:
            for d in sorted(p for p in root.iterdir() if p.is_dir() and re.match(r"^[A-Z]\.", p.name)):
                targets.append(d)
        else:
            if not args.which:
                print(_Colors(True).red("specify a problem letter like 'A' or use --all"))
                sys.exit(2)
            d = find_problem_dir(root, args.which)
            if not d:
                print(_Colors(True).red(f"problem '{args.which}' not found"))
                sys.exit(2)
            targets = [d]

        overall_ok = True
        for d in targets:
            lang = autodetect_lang(d, args.lang)
            try:
                ok, total = judge_problem(d, lang, args.timeout, args.mode, args.show_diff, colors)
                overall_ok &= (ok == total and total > 0)
            except Exception as e:
                print(colors.red(f"[{d.name}] ERROR: {e}"))
                overall_ok = False
        sys.exit(0 if overall_ok else 1)

if __name__ == "__main__":
    main()
