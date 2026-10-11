# Personal Python DevOps Learning Guide

This repository hosts my 30‑day self‑guided Python curriculum, crafted to transition from basic syntax to production‑ready DevOps automation without relying on AI assistance.

## Why this guide?

- **Tailored pace:** 4‑6 hours per day, re‑typing every example to cement knowledge.
- **DevOps focus:** Every concept is illustrated with real‑world Linux automation scenarios (service checks, log processing, CLI tooling).
- **Progress tracking:** `progress/progress.json` records completed days; daily markdown checklists ensure disciplined learning.
- **Test‑driven learning:** Each day ships a pytest suite (`tests/dayXX/`). Run `pytest -q tests/dayXX` to confirm mastery before moving on.

## Quick start

```bash
# clone repo
git clone <YOUR_URL>
cd book_md
# create isolated environment
python3 -m venv .venv && source .venv/bin/activate
# install core deps (pytest, requests, pyyaml, ruff, black)
pip install -r <(printf "pytest\nrequests\npyyaml\nruff\nblack")
```

Now open `book/00-preface.md` and begin Day 1.

## Repository layout

```
book_md/
├─ book/                 # 30 markdown lessons, one per day
├─ tests/                # pytest suites mirroring each lesson
├─ progress/              # JSON progress tracker
├─ scripts/               # utility scripts (e.g., progress checker)
├─ README.md              # you are here
└─ AGENTS.md              # internal agent conventions
```

## Contributing (optional)

If you improve an example or add a new DevOps snippet, open a PR. Keep the “no‑AI‑code‑generation” rule: all code must be hand‑written.

## License

MIT – feel free to fork, adapt, and share your own 30‑day journey.

Welcome to your 30-day intensive course in Python. This book is engineered specifically for system administrators, DevOps engineers, and infrastructure builders who want to master Python from the ground up, write code unaided by AI, and build robust Linux automation.

## How to Use This Book

1. **Unemployed Schedule:** Spend 4-6 hours daily. Re-type code manually—never copy-paste. Muscle memory and deep cognitive absorption are required.
2. **Execution Model:** Every day covers syntax, internals, methods, and a DevOps use-case.
3. **Verification:** Each day has a matching pytest suite in `tests/dayNN/`. Run `pytest tests/dayNN -v` to verify completion.
4. **Tracking:** Progress is logged in `progress/progress.json` and daily markdown checklists.

## Course Outline

- **Week 1:** Fundamentals, memory model, flow control, collections.
- **Week 2:** Functions, scope, error handling, modules, files.
- **Week 3:** DevOps core, OS integration, subprocess, networking, data, testing.
- **Week 4:** OOP deep dive, iterators, generators, concurrency, packaging, capstone.

> [!IMPORTANT]
> This book was created by AI, yeah i know it's hypocrite but yeah I'm good (˵• ̀⩊•́˵)
