# Competitive Programming Workspace

Unified workspace for solutions and tooling across platforms.

## Structure

- `codeforces/` — Codeforces contest folders + `cfprep.py`
- `atcoder/` — AtCoder solutions (Java)
- `project-euler/` — Project Euler solutions (Java/Python)

## Common workflows

**Codeforces**

- Download contest templates + samples:
  - `cd codeforces && python3 cfprep.py get <contest_id> --letters A-F --langs py,java --samples`
- Run samples:
  - `cd codeforces/<contest-folder> && python3 cf_runner.py test A --lang java`

**AtCoder**

- Java workspace lives under `atcoder/java/`.

**Project Euler**

- Java solutions: `project-euler/java/`
- Python solutions: `project-euler/python/` (files like `PE60.py`)
