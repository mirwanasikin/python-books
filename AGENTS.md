# AGENTS.md — Python DevOps Book

> Purpose: track progress, conventions, workflow for agents + human. Single source of truth.

## Project Overview

- **Title:** Python for DevOps & Automation — 30 Days to Deep Understanding
- **Audience:** Knows basic syntax/keywords, wants DevOps scripting, OOP gateway, no-AI independence
- **Stack:** Python 3.11+, Linux, Markdown, pytest
- **Duration:** 30 days, ~4-6 hrs/day
- **Goal:** Write/read Python unaided, deep how-it-works, use stdlib + third-party, build Linux automation

## Directory Structure

```
book_md/
├── AGENTS.md                 # this file
├── README.md                 # entry point, how to use book
├── prompt.md                 # original brief
├── book/
│   ├── 00-preface.md
│   ├── 01-week1-fundamentals/
│   │   ├── day01-how-python-works.md
│   │   ├── day02-objects-variables.md
│   │   ├── day03-numbers-strings-operators.md
│   │   ├── day04-control-flow.md
│   │   ├── day05-lists-tuples.md
│   │   ├── day06-dicts-sets.md
│   │   └── day07-week1-project.md
│   ├── 02-week2-functions-system/
│   │   ├── day08-functions.md
│   │   ├── day09-scope-closures-decorators.md
│   │   ├── day10-errors-context-managers.md
│   │   ├── day11-modules-packages.md
│   │   ├── day12-strings-regex.md
│   │   ├── day13-files-pathlib.md
│   │   └── day14-week2-project.md
│   ├── 03-week3-devops-core/
│   │   ├── day15-os-sys-subprocess.md
│   │   ├── day16-automation-toolkit.md
│   │   ├── day17-network-http.md
│   │   ├── day18-data-apis.md
│   │   ├── day19-testing-typing.md
│   │   └── day20-week3-project.md
│   ├── 04-week4-oop-advanced/
│   │   ├── day21-oop-basics.md
│   │   ├── day22-oop-inheritance.md
│   │   ├── day23-magic-methods.md
│   │   ├── day24-iterators-generators.md
│   │   ├── day25-concurrency.md
│   │   ├── day26-stdlib-tour.md
│   │   ├── day27-thirdparty-devops.md
│   │   ├── day28-packaging-deploy.md
│   │   ├── day29-capstone.md
│   │   └── day30-final-exam.md
│   └── appendix/
│       ├── A-keywords-reference.md
│       ├── B-stdlib-cheatsheet.md
│       └── C-devops-recipes.md
├── progress/
│   └── progress.json         # machine-readable progress
├── tests/
│   ├── day01/
│   ├── ...day30/
│   └── conftest.py
└── scripts/
    └── check_progress.py
```

## Conventions

- **Markdown:** GitHub-flavored, code blocks with `python` tag, runnable examples
- **Code style:** black, ruff, type hints where relevant, `python3.11+`
- **Examples:** Every keyword → explanation + runnable snippet + DevOps context where possible
- **Methods:** Every keyword's related methods (e.g., `str` methods for string keywords) → signature + example
- **Tests:** pytest, one file per day in `tests/dayNN/test_dayNN.py`, `pytest tests/dayNN -v` must pass when day done
- **Todo:** Each day file ends with `- [ ]` checklist; copy to `progress/progress.json` when done

## Workflow for Agents

1. **Read** `progress/progress.json` before editing
2. **Work** one day at a time, keep examples runnable on Linux
3. **Validate:** `pytest tests/dayNN -v` + `ruff check` if available
4. **Update** `progress/progress.json` and day checklist
5. **Never** commit secrets, never skip test creation

## Progress Tracking

- `progress/progress.json` schema:
```json
{
  "current_day": 0,
  "completed_days": [],
  "scores": { "day01": 0 },
  "started_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

- Daily checklist template (in each day file):
```md
## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/dayNN -v`
- [ ] Build mini-script for Linux (where applicable)

## Test
Run: `pytest tests/dayNN -v` — see `tests/dayNN/test_dayNN.py`
```

## 30-Day Map + Keyword Coverage

| Week | Days | Focus | Keywords Introduced |
|------|------|-------|---------------------|
| 0 | 0 | Preface + setup | — |
| 1 | 1-7 | Fundamentals, execution model | `None, True, False, and, or, not, is, in, if, elif, else, match, case, for, while, break, continue, pass, import, as` |
| 2 | 8-14 | Functions, errors, modules, data | `def, return, lambda, yield, global, nonlocal, try, except, finally, raise, assert, with, from, del` |
| 3 | 15-20 | DevOps core, stdlib, testing | `async, await` (preview), re-use all prior |
| 4 | 21-30 | OOP, advanced, concurrency, deploy | `class, async, await, type` (soft) + all 35 hard keywords |

Full 35 hard keywords + soft `match/case/type/_` covered in `appendix/A-keywords-reference.md`.

## Commands

```bash
# setup
python3 -m venv .venv && source .venv/bin/activate
pip install pytest requests pyyaml ruff black

# run day test
pytest tests/day01 -v
pytest -v                          # all days

# check progress
python scripts/check_progress.py

# lint
ruff check book/ tests/ 2>/dev/null || echo "ruff not installed"
```

## Definition of Done (per day)

- All examples run without error on Linux
- Todos checked in markdown
- `pytest` green for that day
- `progress.json` updated
- No AI used to solve exercises (human attests)

## Notes for Human

- 4-6 hrs/day, unemployed schedule → deep work blocks
- Goal not speed, retention. Re-type, don't copy.
- Every week ends with Linux automation project, not toy exercise.
