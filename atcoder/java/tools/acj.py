#!/usr/bin/env python3
import argparse
import os
import re
import sys
import shutil
import subprocess
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


BASE_URL = "https://atcoder.jp"

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def fatal(msg: str, code: int = 1):
    eprint(f"{RED}{BOLD}Error:{RESET} {msg}")
    sys.exit(code)


def http_get(url: str) -> str:
    req = Request(url, headers={
        "User-Agent": "AtCoderJava-ContestTools/1.0 (+https://github.com/)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    try:
        with urlopen(req) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except HTTPError as e:
        fatal(f"HTTP error {e.code} when fetching {url}")
    except URLError as e:
        fatal(f"Failed to reach {url}: {e.reason}")


class TaskListParser(HTMLParser):
    """Parses the contest tasks page to extract mapping of problem label -> task slug and title.

    Accepts typical AtCoder tasks table structure. We simply collect any links that look like
    /contests/<contest>/tasks/<task_slug> and derive the problem letter from slug suffix or title column.
    """

    def __init__(self):
        super().__init__()
        self.tasks = []  # list of (href, title)
        self._in_link = False
        self._current_href = None
        self._current_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href and "/tasks/" in href:
                # candidate task link; we'll capture text
                self._in_link = True
                self._current_href = href
                self._current_text = []

    def handle_data(self, data):
        if self._in_link and data.strip():
            self._current_text.append(data.strip())

    def handle_endtag(self, tag):
        if tag == "a" and self._in_link:
            title = " ".join(self._current_text).strip()
            self.tasks.append((self._current_href, title))
            self._in_link = False
            self._current_href = None
            self._current_text = []


class SampleParser(HTMLParser):
    """Parses task page to extract only Sample Input/Output blocks.

    Strategy: Track headings and only capture <pre> blocks when the most recent
    heading contains one of the explicit sample labels:
      - Japanese: 入力例 / 出力例
      - English:  Sample Input / Sample Output
    This avoids picking up the generic format blocks under 入力/出力 sections.
    """

    def __init__(self, lang: str = "ja"):
        super().__init__()
        if lang not in ("ja", "en", "any"):
            raise ValueError("lang must be one of: ja, en, any")
        self.lang = lang
        self.samples = []  # list[(label, text)] where label in {'in','out'} or None
        self._capture_pre = False
        self._current_pre: list[str] = []
        self._in_heading = False
        self._current_heading: list[str] = []
        self._sample_mode: str | None = None  # 'in' / 'out' when the next <pre> should be captured
        # AtCoder includes both Japanese and English statements in the same HTML,
        # wrapped in elements like <span class="lang-ja"> and <span class="lang-en">.
        # Track the current language scope so we don't duplicate samples.
        self._lang_stack: list[tuple[str, str]] = []  # (tag, lang)

    @staticmethod
    def _classify_heading(text: str) -> str | None:
        h = text.strip().lower()
        # Japanese explicit sample labels
        if "入力例" in h or "sample input" in h:
            return "in"
        if "出力例" in h or "sample output" in h:
            return "out"
        return None

    def _lang_allowed(self) -> bool:
        if self.lang == "any":
            return True
        current = self._lang_stack[-1][1] if self._lang_stack else None
        return current is None or current == self.lang

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "")
        if cls:
            tokens = set(re.split(r"\s+", cls.strip()))
            if "lang-ja" in tokens:
                self._lang_stack.append((tag, "ja"))
            elif "lang-en" in tokens:
                self._lang_stack.append((tag, "en"))

        if tag in ("h2", "h3", "h4", "h5"):
            if self._lang_allowed():
                self._in_heading = True
                self._current_heading = []
        elif tag == "pre":
            # start capturing candidates; will be appended only if _sample_mode set
            if self._lang_allowed():
                self._capture_pre = True
                self._current_pre = []

    def handle_endtag(self, tag):
        if tag in ("h2", "h3", "h4", "h5"):
            if self._in_heading:
                heading_text = "".join(self._current_heading)
                self._sample_mode = self._classify_heading(heading_text)
                self._in_heading = False
                self._current_heading = []
        elif tag == "pre":
            if self._capture_pre:
                text = "".join(self._current_pre)
                if self._sample_mode in ("in", "out"):
                    self.samples.append((self._sample_mode, text))
                # reset capture; keep _sample_mode None to require a new matching heading
                self._capture_pre = False
                self._current_pre = []
                self._sample_mode = None

        if self._lang_stack and self._lang_stack[-1][0] == tag:
            self._lang_stack.pop()

    def handle_data(self, data):
        if self._in_heading and self._lang_allowed():
            self._current_heading.append(data)
        if self._capture_pre and self._lang_allowed():
            self._current_pre.append(data)


def derive_letter_from_slug(slug: str) -> str | None:
    # examples: abc414_a, abc414_b, arc175_a, agc071_a, abc293_h
    m = re.search(r"_([a-z])$", slug)
    if m:
        return m.group(1).upper()
    # Sometimes old contests use different slugs; fallback: last path segment letter
    m2 = re.search(r"([A-Za-z])(?:$|\W)", os.path.basename(slug))
    if m2:
        return m2.group(1).upper()
    return None


def find_java_template(root: str) -> str:
    # Prefer shared template at repo_root/template/Main.java
    script_dir = os.path.dirname(os.path.abspath(__file__))  # .../atcoder/java/tools
    shared = os.path.normpath(os.path.join(script_dir, "..", "..", "..", "template", "Main.java"))
    if os.path.isfile(shared):
        return shared

    candidates = [
        os.path.join(root, "Main.java"),
    ]
    # Also look one level under existing contest dirs for a Main.java
    for entry in os.listdir(root):
        p = os.path.join(root, entry)
        if os.path.isdir(p):
            cand = os.path.join(p, "Main.java")
            if os.path.isfile(cand):
                candidates.append(cand)
    for c in candidates:
        if os.path.isfile(c):
            return c
    fatal("Could not find a Java template Main.java in repo root or contest dirs.")


def ensure_problem_scaffold(root: str, contest: str, letter: str, template_path: str) -> str:
    contest_dir = os.path.join(root, contest)
    prob_dir = os.path.join(contest_dir, letter)
    tests_dir = os.path.join(prob_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    java_path = os.path.join(prob_dir, "Main.java")
    if not os.path.exists(java_path):
        shutil.copyfile(template_path, java_path)
    return prob_dir


def write_samples(tests_dir: str, inouts: list[tuple[str | None, str]]):
    # Pair inputs and outputs by order; try to use labels if present
    inputs = []
    outputs = []
    for label, text in inouts:
        text = text.replace("\r\n", "\n").rstrip("\n") + "\n"
        if label == "in":
            inputs.append(text)
        elif label == "out":
            outputs.append(text)
        else:
            # Heuristic: alternate
            if len(inputs) == len(outputs):
                inputs.append(text)
            else:
                outputs.append(text)

    count = min(len(inputs), len(outputs))
    for i in range(count):
        with open(os.path.join(tests_dir, f"sample{i+1}.in"), "w", encoding="utf-8") as f:
            f.write(inputs[i])
        with open(os.path.join(tests_dir, f"sample{i+1}.out"), "w", encoding="utf-8") as f:
            f.write(outputs[i])

    # Clean up old duplicated samples (e.g., when both lang-ja and lang-en were parsed).
    for fname in os.listdir(tests_dir):
        m = re.match(r"sample(\d+)\.(in|out)$", fname)
        if not m:
            continue
        idx = int(m.group(1))
        if idx > count:
            try:
                os.remove(os.path.join(tests_dir, fname))
            except OSError:
                pass
    return count


def parse_contest(contest: str, only_letters: set[str] | None, root: str, lang: str):
    tasks_url = f"{BASE_URL}/contests/{contest}/tasks"
    print(f"{BLUE}{BOLD}Fetching tasks:{RESET} {tasks_url}")
    html = http_get(tasks_url)
    p = TaskListParser()
    p.feed(html)

    # Build mapping letter -> (slug, title)
    mapping = {}
    for href, title in p.tasks:
        if not href.startswith("/contests/"):
            continue
        parts = href.strip("/").split("/")
        if len(parts) >= 4 and parts[2] == "tasks":
            slug = parts[3]
            letter = derive_letter_from_slug(slug)
            if letter and letter not in mapping:
                mapping[letter] = (slug, title)

    if not mapping:
        fatal("Could not parse tasks list for contest. The page structure may have changed or the contest id is wrong.")

    letters = sorted(mapping.keys(), key=lambda x: (len(x), x))
    if only_letters:
        letters = [L for L in letters if L in only_letters]
        if not letters:
            fatal("None of the requested problems were found in the contest.")

    template = find_java_template(root)
    print(f"Using template: {template}")

    created = []
    for L in letters:
        slug, title = mapping[L]
        task_url = f"{BASE_URL}/contests/{contest}/tasks/{slug}"
        print(f"{CYAN}→ {BOLD}{contest}/{L}{RESET} {DIM}({slug}){RESET}")
        prob_dir = ensure_problem_scaffold(root, contest, L, template)
        tests_dir = os.path.join(prob_dir, "tests")

        # Fetch and parse samples
        thtml = http_get(task_url)
        sp = SampleParser(lang=lang)
        sp.feed(thtml)
        n = write_samples(tests_dir, sp.samples)
        print(f"   Samples: {GREEN}{n}{RESET} saved in {tests_dir}")
        created.append((L, prob_dir, n))

    print(f"\n{GREEN}{BOLD}Done.{RESET} Created/updated {len(created)} problems.")


def compile_java(java_dir: str) -> tuple[bool, str]:
    src = os.path.join(java_dir, "Main.java")
    if not os.path.isfile(src):
        return False, "Main.java not found"
    try:
        proc = subprocess.run(["javac", "-encoding", "UTF-8", "Main.java"], cwd=java_dir,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        ok = proc.returncode == 0
        return ok, proc.stdout
    except FileNotFoundError:
        return False, "javac not found in PATH"


def run_case(java_dir: str, infile: str, timeout_sec: float = 4.0) -> tuple[int, str, str]:
    try:
        with open(infile, "r", encoding="utf-8") as f:
            proc = subprocess.run(["java", "Main"], cwd=java_dir, input=f.read(),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True, timeout=timeout_sec)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except FileNotFoundError:
        return -1, "", "java not found in PATH"


def normalize(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.replace("\r\n", "\n").split("\n")).strip() + "\n"


def test_contest(contest: str, only_letters: set[str] | None, root: str, verbose: bool, fail_fast: bool, all_problems: bool):
    contest_dir = os.path.join(root, contest)
    if not os.path.isdir(contest_dir):
        fatal(f"Contest directory not found: {contest_dir}. Run parse first.")

    if all_problems:
        letters = [d for d in sorted(os.listdir(contest_dir)) if os.path.isdir(os.path.join(contest_dir, d))]
        if only_letters:
            letters = [L for L in letters if L in only_letters]
    else:
        letters = sorted(list(only_letters)) if only_letters else []
        if not letters:
            # default: detect A..H present
            letters = [d for d in sorted(os.listdir(contest_dir)) if os.path.isdir(os.path.join(contest_dir, d))]

    total_cases = 0
    passed = 0
    failed = 0
    skipped = 0

    for L in letters:
        prob_dir = os.path.join(contest_dir, L)
        tests_dir = os.path.join(prob_dir, "tests")
        print(f"\n{BLUE}{BOLD}Problem {contest}/{L}{RESET}")

        ok, out = compile_java(prob_dir)
        if not ok:
            # If no Main.java, treat as skip; if other compile error, count as failed
            if "Main.java not found" in out:
                print(f"  {YELLOW}No Main.java; skipping{RESET}")
                skipped += 1
                continue
            print(f"  {RED}Compile failed{RESET}\n{out}")
            failed += 1
            if fail_fast:
                break
            continue
        elif verbose:
            if out.strip():
                print(f"  {DIM}javac:{RESET}\n{DIM}{out}{RESET}")
        # gather tests
        if not os.path.isdir(tests_dir):
            print(f"  {YELLOW}No tests directory: {tests_dir}{RESET}")
            skipped += 1
            continue
        inputs = [f for f in os.listdir(tests_dir) if f.endswith('.in')]
        inputs.sort(key=lambda x: int(re.search(r"(\d+)", x).group(1)) if re.search(r"(\d+)", x) else x)
        if not inputs:
            print(f"  {YELLOW}No sample inputs found in {tests_dir}{RESET}")
            skipped += 1
            continue

        for inf in inputs:
            idxm = re.search(r"(\d+)", inf)
            idx = idxm.group(1) if idxm else "?"
            out_file = inf.replace('.in', '.out')
            in_path = os.path.join(tests_dir, inf)
            out_path = os.path.join(tests_dir, out_file)
            exp = open(out_path, 'r', encoding='utf-8').read() if os.path.exists(out_path) else None
            rc, stdout, stderr = run_case(prob_dir, in_path)
            total_cases += 1
            if rc != 0:
                print(f"  [{L}-{idx}] {RED}RE/Timeout{RESET} rc={rc}")
                if verbose and stderr:
                    print(f"    {DIM}{stderr}{RESET}")
                failed += 1
                if fail_fast:
                    break
                continue
            if exp is None:
                print(f"  [{L}-{idx}] {YELLOW}No expected output; printed:{RESET}\n{stdout}")
                continue
            if normalize(stdout) == normalize(exp):
                print(f"  [{L}-{idx}] {GREEN}OK{RESET}")
                passed += 1
            else:
                print(f"  [{L}-{idx}] {RED}WA{RESET}")
                if verbose:
                    print(f"    {YELLOW}expected:{RESET}\n{exp}")
                    print(f"    {YELLOW}actual:{RESET}\n{stdout}")
                failed += 1
                if fail_fast:
                    break
        if fail_fast and failed:
            break

    print(f"\n{BOLD}Summary:{RESET} cases={total_cases} {GREEN}passed={passed}{RESET} {RED}failed={failed}{RESET} {YELLOW}skipped={skipped}{RESET}")
    return 0 if failed == 0 else 1


def parse_args(argv):
    ap = argparse.ArgumentParser(prog="acj", description="AtCoder Java Contest Tools: parse contests and run sample tests.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_parse = sub.add_parser("parse", help="Parse a contest and scaffold problems + samples")
    ap_parse.add_argument("contest", help="Contest id, e.g., abc414")
    ap_parse.add_argument("--problems", "-p", help="Comma-separated problem letters, e.g., A,B,D", default=None)
    ap_parse.add_argument("--lang", choices=["ja", "en", "any"], default="ja",
                          help="Which statement language to parse samples from (default: ja)")

    ap_test = sub.add_parser("test", help="Compile and run sample tests")
    ap_test.add_argument("contest", help="Contest id, e.g., abc414")
    ap_test.add_argument("--problems", "-p", help="Comma-separated problem letters to test", default=None)
    ap_test.add_argument("--all", action="store_true", help="Run tests for all problems present in the contest folder")
    ap_test.add_argument("--verbose", "-v", action="store_true", help="Verbose output (show diffs, compiler output)")
    ap_test.add_argument("--fail-fast", action="store_true", help="Stop on first failure")

    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    root = os.getcwd()

    if args.cmd == "parse":
        letters = None
        if args.problems:
            letters = set(x.strip().upper() for x in re.split(r"[\s,]+", args.problems) if x.strip())
        parse_contest(args.contest, letters, root, lang=args.lang)
        return 0
    elif args.cmd == "test":
        letters = None
        if args.problems:
            letters = set(x.strip().upper() for x in re.split(r"[\s,]+", args.problems) if x.strip())
        code = test_contest(args.contest, letters, root, verbose=args.verbose, fail_fast=args.fail_fast, all_problems=args.all)
        return code
    else:
        fatal("Unknown command")


if __name__ == "__main__":
    sys.exit(main())
