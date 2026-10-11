# Day 25 — Concurrency & Async Programming

Keywords: `async`, `await`, `thread`, `process`, `ThreadPoolExecutor`, `ProcessPoolExecutor`, `asyncio`

## Keywords + Methods

### Asynchronous Programming with `async`/`await`
- **Type:** Cooperative multitasking using event loop
- **Methods:** `asyncio.run()`, `asyncio.create_task()`, `asyncio.gather()`
- **Example:**
  ```python
  import asyncio

  async def health_check(host: str) -> str:
      await asyncio.sleep(0.1)  # Simulate network delay
      return f"HEALTHY: {host}"

  async def check_all():
      results = await asyncio.gather(
          health_check("web-01"),
          health_check("db-01"),
          health_check("cache-01")
      )
      for r in results:
          print(r)

  asyncio.run(check_all())
  ```

### Threading and Process Pool Execution
- **Type:** Parallel execution for CPU-bound and I/O-bound tasks
- **Methods:** `ThreadPoolExecutor`, `ProcessPoolExecutor`, `concurrent.futures.wait`, `map`
- **Example:**
  ```python
  from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, ALL_COMPLETED
  import subprocess

  def run_shell(cmd: str) -> str:
      result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
      return result.stdout.strip()

  # Parallel health checks using threads (I/O-bound)
  with ThreadPoolExecutor(max_workers=3) as executor:
      futures = [
          executor.submit(run_shell, "ping -c 1 google.com"),
          executor.submit(run_shell, "ping -c 1 8.8.8.8"),
          executor.submit(run_shell, "ping -c 1 github.com")
      ]
      wait(futures, timeout=10, return_when=ALL_COMPLETED)
      for f in futures:
          print(f.result())
  ```

### GIL and When to Use Multiprocessing
- **Type:** Python Global Interpreter Lock (GIL) limitations
- **Methods:** `multiprocessing.Pool`, `multiprocessing.cpu_count()`
- **Example:**
  ```python
  import multiprocessing
  import time

  def cpu_task(n: int) -> int:
      total = 0
      for i in range(n):
          total += i * i
      return total

  # CPU-bound: use ProcessPoolExecutor
  with ProcessPoolExecutor() as executor:
      future = executor.submit(cpu_task, 1000000)
      print(future.result())
  ```

## DevOps Context: Scaling Automation with Parallel Checks
Asynchronous and thread-based patterns allow non-blocking monitoring of services and batch execution of system commands across multiple hosts simultaneously.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day25 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day25 -v` — see `tests/day25/test_day25.py`
