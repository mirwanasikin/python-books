# Preface — Python for DevOps & Automation

This book is a 30-day journey from the core mechanics of Python to complex infrastructure automation. It is designed for those who understand some syntax but want to transition into being capable, independent Python developers who don't rely on AI to write code.

## Why Python for DevOps?

Bash is great for quick pipes, but Python provides:
- **Testability:** Robust unit and integration tests.
- **Maintainability:** Clearer structure for large automation logic.
- **Library Support:** Deep integration with cloud providers (AWS, Azure, GCP), databases, and network protocols.
- **Abstraction:** Move from thinking in commands to thinking in systems and state.

## 30-Day Philosophy

- **No AI:** You must type every line. AI assistance during this learning phase stunts your ability to internalize syntax and debug.
- **Linux Native:** Every example runs on Linux. You'll learn to handle processes, files, and networks like a pro.
- **DevOps Context:** Every keyword and method is grounded in real-world infrastructure tasks.

## Setup Your Environment

```bash
# Recommended setup for this book
python3 -m venv .venv
source .venv/bin/activate
pip install pytest requests pyyaml ruff black psutil
```

Now, turn to Day 01 and begin.
