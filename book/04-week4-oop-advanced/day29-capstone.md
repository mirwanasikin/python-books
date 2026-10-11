# Day 29 — Capstone Project: Infrastructure Monitor

Today is for synthesis. You will build a production-ready infrastructure monitor (`infra_monitor.py`) that combines everything you've learned.

## Project Spec: `InfraMonitor`

Build a tool that:
1. **Config:** Reads a YAML list of hosts and services to check.
2. **Execution:** Performs checks in parallel (async or threading).
3. **Checks:**
   - ICMP Ping (via subprocess).
   - HTTP Health Check (via requests).
   - Custom Service check (e.g., check if a port is open).
4. **Logging:** Records all events to `infra.log`.
5. **Report:** Generates a JSON report and a pretty table in the terminal (use `rich` if available, or simple formatting).
6. **CLI:** Uses `argparse` to accept config path, timeout, and report destination.

## Architecture

- **`Check` Abstract Base Class:** Define a common interface for `PingCheck`, `HttpCheck`, `PortCheck`.
- **`Server` Class:** Holds server state and a list of `Check` objects.
- **`Monitor` Class:** Orchestrates the execution and report generation.

## Starter Code

```python
import asyncio
import yaml
import logging
from abc import ABC, abstractmethod

class Check(ABC):
    @abstractmethod
    async def run(self):
        pass

class PingCheck(Check):
    def __init__(self, host):
        self.host = host
    async def run(self):
        # Implement ping check using subprocess
        pass

# ... build other checks and the orchestrator
```

## Success Criteria

- [ ] Runs without error.
- [ ] Handles timeouts and network failures gracefully.
- [ ] Generates valid JSON report.
- [ ] Passing all tests in `tests/day29/test_day29.py`.

## Todo
- [ ] Design your class hierarchy.
- [ ] Implement async execution.
- [ ] Build the CLI entry point.
- [ ] Pass `pytest tests/day29 -v`.

## Test
Run: `pytest tests/day29 -v`
