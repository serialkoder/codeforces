#!/usr/bin/env python3
# cfprep.py — Codeforces contest prep helper (creates templates + color runner)
# Usage:
#   python3 cfprep.py get 1976 --letters A-F --langs py,java --samples
#   cd 1976-<contest-name> && python3 cf_runner.py test A --color auto
#   # or wrapper:
#   python3 cfprep.py test A --color auto

import argparse, json, os, re, sys, html, urllib.request
from pathlib import Path
from typing import List, Tuple
from string import Template

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"

PY_TPL = """#!/usr/bin/env python3
# Contest: $contest_id  Problem: $letter - $name
# URL: https://codeforces.com/contest/$contest_id/problem/$letter

import sys
data = sys.stdin.buffer.read().decode("utf-8", errors="ignore").split()
it = iter(data)

def y():
    print("YES")

def n():
    print("NO")

def yn(ok: bool):
    print("YES" if ok else "NO")

def solve():
    # t = int(next(it))  # uncomment if multiple test cases
    # for _ in range(t):
    #     n = int(next(it))
    #     # arr = [int(next(it)) for __ in range(n)]
    #     # TODO: solve
    #     # print(answer)
    pass

if __name__ == "__main__":
    solve()
"""

JAVA_TPL = """// Contest: $contest_id  Problem: $letter - $name
// URL: https://codeforces.com/contest/$contest_id/problem/$letter
import java.io.*;
import java.util.*;

public final class Main {
    private static final PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));

    private static void y() { out.println("YES"); }
    private static void n() { out.println("NO"); }
    private static void yn(boolean ok) { out.println(ok ? "YES" : "NO"); }

    private static void pc(char[] a) { out.print(a); }
    private static void pcl(char[] a) { out.print(a); out.println(); }
    private static void pc(char[] a, int off, int len) { out.write(a, off, len); }
    private static void pcl(char[] a, int off, int len) { out.write(a, off, len); out.println(); }

    private static final class FS {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        FS(InputStream is) { in = is; }
        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        String next() throws IOException {
            StringBuilder sb = new StringBuilder();
            int c;
            while ((c = read()) <= 32 && c != -1) {}
            while (c > 32) { sb.append((char)c); c = read(); }
            return sb.toString();
        }
        int nextInt() throws IOException { return Integer.parseInt(next()); }
        long nextLong() throws IOException { return Long.parseLong(next()); }

        int[] readInts(int n) throws IOException {
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = nextInt();
            return a;
        }

        long[] readLongs(int n) throws IOException {
            long[] a = new long[n];
            for (int i = 0; i < n; i++) a[i] = nextLong();
            return a;
        }

        private byte[] readAllBytes() throws IOException {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            if (ptr < len) {
                baos.write(buffer, ptr, len - ptr);
                ptr = len;
            }
            byte[] tmp = new byte[1 << 16];
            int r;
            while ((r = in.read(tmp)) != -1) baos.write(tmp, 0, r);
            return baos.toByteArray();
        }

        int[] readAllInts() throws IOException {
            byte[] b = readAllBytes();
            int[] a = new int[Math.max(8, b.length / 2)];
            int sz = 0;
            int i = 0;
            while (i < b.length) {
                while (i < b.length && b[i] <= 32) i++;
                if (i >= b.length) break;
                int sign = 1;
                if (b[i] == '-') { sign = -1; i++; }
                int v = 0;
                while (i < b.length && b[i] > 32) {
                    v = v * 10 + (b[i] - '0');
                    i++;
                }
                if (sz == a.length) a = Arrays.copyOf(a, a.length * 2);
                a[sz++] = v * sign;
            }
            return Arrays.copyOf(a, sz);
        }

        long[] readAllLongs() throws IOException {
            byte[] b = readAllBytes();
            long[] a = new long[Math.max(8, b.length / 2)];
            int sz = 0;
            int i = 0;
            while (i < b.length) {
                while (i < b.length && b[i] <= 32) i++;
                if (i >= b.length) break;
                long sign = 1;
                if (b[i] == '-') { sign = -1; i++; }
                long v = 0;
                while (i < b.length && b[i] > 32) {
                    v = v * 10 + (b[i] - '0');
                    i++;
                }
                if (sz == a.length) a = Arrays.copyOf(a, a.length * 2);
                a[sz++] = v * sign;
            }
            return Arrays.copyOf(a, sz);
        }
    }

    public static void main(String[] args) throws Exception {
        FS in = new FS(System.in);
        // int t = in.nextInt(); // uncomment for multi-case
        // while (t-- > 0) {
        //     int n = in.nextInt();
        //     // long[] a = new long[n];
        //     // for (int i = 0; i < n; i++) a[i] = in.nextLong();
        //     // TODO: solve
        //     // out.println(ans);
        // }
        out.flush();
    }
}
"""

# -------- colorized runner to write into <contest_root>/cf_runner.py --------
CF_RUNNER = r"""#!/usr/bin/env python3
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
"""


# ---------------------- helpers ----------------------
def http_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        import json as _json

        return _json.loads(r.read().decode("utf-8"))


def http_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="ignore")


def extract_contest_id(token: str) -> int:
    m = re.search(r"(?:contest|gym)/(\d+)", token)
    if m:
        return int(m.group(1))
    return int(token)


def slugify(s: str, maxlen: int = 40) -> str:
    s = s.strip()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("_")
    if not s:
        s = "Problem"
    return s[:maxlen]


def ensure_file(
    path: Path, content: str, overwrite: bool = False, make_exe: bool = False
):
    if path.exists() and not overwrite:
        return False
    path.write_text(content, encoding="utf-8")
    if make_exe:
        try:
            path.chmod(path.stat().st_mode | 0o111)
        except Exception:
            pass
    return True


# crude sample extraction that works on most CF pages without external deps
def parse_samples_from_html(html_text: str) -> List[Tuple[str, str]]:
    def pre_html_to_text(pre_html: str) -> str:
        s = pre_html
        s = re.sub(r"(?is)<br\s*/?>", "\n", s)
        s = re.sub(r"(?is)</div\s*>", "\n", s)
        s = re.sub(r"(?is)</p\s*>", "\n", s)
        s = re.sub(r"(?is)</li\s*>", "\n", s)
        s = re.sub(r"(?is)<div[^>]*>", "", s)
        s = re.sub(r"(?is)<span[^>]*>", "", s)
        s = re.sub(r"(?is)</span\s*>", "", s)
        s = re.sub(r"(?is)<.*?>", "", s)
        s = html.unescape(s)
        s = s.replace("\u00a0", " ")
        return s.strip("\n\r")

    block = re.search(
        r'<div class="sample-tests">(.+?)</div>\s*</div>', html_text, flags=re.S | re.I
    )
    if not block:
        block = re.search(
            r'<div class="sample-test">(.+?)</div>\s*</div>',
            html_text,
            flags=re.S | re.I,
        )
    if not block:
        return []
    segment = block.group(1)
    ins = re.findall(r'(?is)<div class="input">.*?<pre>(.+?)</pre>', segment)
    outs = re.findall(r'(?is)<div class="output">.*?<pre>(.+?)</pre>', segment)
    pairs = []
    for i in range(min(len(ins), len(outs))):
        a = pre_html_to_text(ins[i])
        b = pre_html_to_text(outs[i])
        pairs.append((a, b))
    return pairs


def fetch_contest(contest_id: int):
    url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&from=1&count=1"
    data = http_json(url)
    if data.get("status") != "OK":
        raise RuntimeError(f"CF API error: {data}")
    cinfo = data["result"]["contest"]
    problems = data["result"]["problems"]
    return cinfo, problems


def fetch_samples(contest_id: int, letter: str) -> List[Tuple[str, str]]:
    urls = [
        f"https://codeforces.com/contest/{contest_id}/problem/{letter}",
        f"https://codeforces.com/problemset/problem/{contest_id}/{letter}",
    ]
    for u in urls:
        try:
            page = http_text(u)
            pairs = parse_samples_from_html(page)
            if pairs:
                return pairs
        except Exception:
            pass
    return []


def write_problem_dir(
    root: Path,
    contest_id: int,
    letter: str,
    name: str,
    langs: List[str],
    write_samples: bool,
    overwrite: bool,
    only_samples: bool = False,
):
    pdir = root / f"{letter}.{slugify(name)}"
    pdir.mkdir(parents=True, exist_ok=True)

    if not only_samples:
        if "py" in langs:
            py_path = pdir / f"{letter}.py"
            ensure_file(
                py_path,
                Template(PY_TPL).substitute(
                    contest_id=contest_id, letter=letter, name=name
                ),
                overwrite,
                make_exe=True,
            )
        if "java" in langs:
            ensure_file(
                pdir / "Main.java",
                Template(JAVA_TPL).substitute(
                    contest_id=contest_id, letter=letter, name=name
                ),
                overwrite,
            )

    if write_samples:
        pairs = fetch_samples(contest_id, letter)
        if pairs:
            sdir = pdir / "samples"
            sdir.mkdir(exist_ok=True)
            for i, (iin, out) in enumerate(pairs, 1):
                (sdir / f"{i}.in").write_text(iin + "\n", encoding="utf-8")
                (sdir / f"{i}.out").write_text(out + "\n", encoding="utf-8")


def write_readme(root: Path, contest_id: int, contest_name: str, problems, overwrite: bool):
    lines = [f"# CF {contest_id}: {contest_name}", ""]
    for p in problems:
        idx = p.get("index")
        name = p.get("name", "")
        link = f"https://codeforces.com/contest/{contest_id}/problem/{idx}"
        lines.append(f"- [ ] {idx} — {name}  ({link})")
    ensure_file(root / "README.md", "\n".join(lines) + "\n", overwrite)


def write_runner(root: Path, overwrite: bool):
    ensure_file(root / "cf_runner.py", CF_RUNNER, overwrite, make_exe=True)


def do_get(args):
    contest_id = extract_contest_id(args.contest)
    cinfo, problems = fetch_contest(contest_id)
    cname = cinfo.get("name", f"Contest_{contest_id}")
    contest_slug = slugify(cname, 60)
    root = Path(args.root).expanduser().resolve() / f"{contest_id}-{contest_slug}"
    root.mkdir(parents=True, exist_ok=True)

    if args.only_samples:
        args.samples = True

    letters = None
    if args.letters:
        letters = [
            s.strip().upper() for s in re.split(r"[,\s]+", args.letters) if s.strip()
        ]
    langs = [s.strip().lower() for s in args.langs.split(",") if s.strip()]

    if not args.only_samples:
        write_readme(root, contest_id, cname, problems, args.overwrite)
        write_runner(root, args.overwrite)

    created = 0
    for p in problems:
        idx = p.get("index")
        if letters and idx not in letters:
            continue
        name = p.get("name", "")
        write_problem_dir(
            root,
            contest_id,
            idx,
            name,
            langs,
            args.samples,
            args.overwrite,
            only_samples=args.only_samples,
        )
        created += 1

    print(f"Contest at: {root}")
    print(f"Problems created: {created}")
    if args.samples:
        print("Sample tests downloaded where available.")
    if not args.only_samples:
        print(
            "Runner written: cf_runner.py (use: python3 cf_runner.py test A --color auto)"
        )


def do_test(args):
    root = Path.cwd()
    runner = root / "cf_runner.py"
    if not runner.exists():
        print("cf_runner.py not found in current directory. Run from a contest root.")
        sys.exit(2)
    cmd = [sys.executable, str(runner), "test"]
    if args.which:
        cmd.append(args.which)
    if args.all:
        cmd.append("--all")
    if args.lang:
        cmd += ["--lang", args.lang]
    if args.timeout is not None:
        cmd += ["--timeout", str(args.timeout)]
    if args.mode:
        cmd += ["--mode", args.mode]
    if args.show_diff is not None:
        cmd += ["--show-diff", str(args.show_diff)]
    if args.color:
        cmd += ["--color", args.color]
    os.execv(sys.executable, cmd)


def main():
    ap = argparse.ArgumentParser(
        description="Prepare Codeforces contests (templates + color runner)"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("get", help="create contest folder with templates")
    g.add_argument("contest", help="contest ID or URL")
    g.add_argument("--letters", help="letters to include, e.g. 'A-D' or 'A,C,E'")
    g.add_argument(
        "--langs", default="py,java", help="comma list: py,java (default: py,java)"
    )
    g.add_argument(
        "--root", default=".", help="where to create the contest dir (default: .)"
    )
    g.add_argument("--samples", action="store_true", help="download sample tests")
    g.add_argument(
        "--only-samples",
        action="store_true",
        help="only (re)download samples; do not create/overwrite code, README, or runner",
    )
    g.add_argument("--overwrite", action="store_true", help="overwrite existing files")
    g.set_defaults(func=do_get)

    t = sub.add_parser("test", help="run samples (wrapper for cf_runner.py)")
    t.add_argument("which", nargs="?", help="problem letter or dir; omit with --all")
    t.add_argument("--all", action="store_true", help="run all problems with samples/")
    t.add_argument("--lang", choices=["py", "java"])
    t.add_argument("--timeout", type=float, default=2.0)
    t.add_argument("--mode", choices=["exact", "ws", "tokens"], default="ws")
    t.add_argument("--show-diff", type=int, default=3)
    t.add_argument("--color", choices=["auto", "always", "never"], default="auto")
    t.set_defaults(func=do_test)

    args = ap.parse_args()
    if args.cmd == "get" and args.letters and "-" in args.letters:
        m = re.fullmatch(r"\s*([A-Za-z])\s*-\s*([A-Za-z])\s*", args.letters)
        if m:
            a, b = m.group(1).upper(), m.group(2).upper()
            rng = [chr(c) for c in range(ord(a), ord(b) + 1)]
            args.letters = ",".join(rng)
    args.func(args)


if __name__ == "__main__":
    main()
