# Day 24 — Iterators & Generators

Keywords: `yield`, `iter`, `__iter__`, `__next__`, `generator expression`, `itertools`

## Keywords + Methods

### Generators and `yield`
- **Type:** Deferred execution, lazy evaluation
- **Methods:** `__iter__`, `__next__`
- **Example:**
  ```python
  def parse_log_lines(file_path: str):
      with open(file_path) as f:
          for line in f:
              if "ERROR" in line:
                  yield line.strip()

  # Process large file without memory blow-up
  error_logs = list(parse_log_lines("/var/log/nginx/access.log"))
  print(f"Found {len(error_logs)} errors")
  ```

### Generator Expressions
- **Type:** Concise inline lazy sequences
- **Methods:** `(__iter__, __next__)` inherited from generators
- **Example:**
  ```python
  ports = [80, 443, 8080, 8081, 3000, 5000]
  # Filter high-usage ports (> 100 connections) lazily
  high_ports = (p for p in ports if p > 1000)  # yields nothing
  high_ports = (p for p in ports if p < 1000)
  print(list(high_ports))
  ```

### `itertools` for Efficient Streams
- **Type:** Built-in tools for iteration optimization
- **Methods:** `count`, `cycle`, `repeat`, `islice`, `takewhile`, `chain`, `tee`, `zip_longest`
- **Example:**
  ```python
  from itertools import islice, cycle, zip_longest

  # Stream continuous service health checks
  ports = [22, 80, 443]
  checks = cycle(ports)
  first_five = list(islice(checks, 5))
  print(first_five)

  # Parallel check and log streaming
  services = ["web", "db", "cache"]
  metrics = [10, 20, 30]
  for s, m in zip_longest(services, metrics, fillvalue=0):
      print(f"{s}: {m} connections")
  ```

## DevOps Context: Stream Processing Large Datasets
Generators avoid loading huge log files or system metrics into memory, crucial for high-performance automation scripts on constrained resources.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day24 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day24 -v` — see `tests/day24/test_day24.py`
