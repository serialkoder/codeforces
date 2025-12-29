# Competitive Programming Workspace

Unified workspace for solutions and tooling across platforms.

## Structure

- `codeforces/` — Codeforces contest folders + `cfprep.py`
- `atcoder/` — AtCoder solutions (Java)
- `project-euler/` — Project Euler solutions (Java/Python)

## Common workflows

**Codeforces**

- Download contest templates + samples:
  - From repo root (auto writes under `codeforces/`):
    - `python3 cfprep.py get <contest_id> --letters A-F --langs py,java --samples`
  - Or from inside `codeforces/`:
    - `cd codeforces && python3 cfprep.py get <contest_id> --letters A-F --langs py,java --samples`
- Run samples:
  - `cd codeforces/<contest-folder> && python3 cf_runner.py test A --lang java`

**AtCoder**

- Java workspace lives under `atcoder/java/`.
- Download problems + sample tests (scaffold):
  - `cd atcoder/java && ./bin/p abc414` (all problems)
  - `cd atcoder/java && ./bin/p abc414 A,B,D` (subset)
  - (equivalent) `cd atcoder/java && python3 tools/acj.py parse abc414 -p A,B,D`
- Run sample tests:
  - `cd atcoder/java && ./bin/r abc414 --all`
  - `cd atcoder/java && ./bin/r abc414 A,B -v` (verbose)
  - (equivalent) `cd atcoder/java && python3 tools/acj.py test abc414 -p A,B --verbose`

**Project Euler**

- Java solutions: `project-euler/java/`
- Python solutions: `project-euler/python/` (files like `PE60.py`)
