# Day 04 — Control Flow

Keywords: `if, elif, else, match, case, for, while, break, continue, pass, and, or, not`

## Keywords + Methods

### `if/elif/else` and Truthiness
- **Type:** Conditional branching
- **Methods:** `bool()` to check truthiness
- **Example:**
  ```python
  # DevOps: Checking disk usage with truthiness
  def check_disk_usage(mount_point):
      if mount_point:  # Truthy check
          try:
              usage = os.path.getsize(mount_point)  # actual implementation
              if usage > 90 * 1024**3:  # 90GB
                  return "CRITICAL"
              elif usage > 80 * 1024**3:  # 80GB
                  return "WARNING"
              else:
                  return "OK"
          except OSError:
              return "ERROR"
      else:
          return "INVALID"
  ```

### `match/case` (Pattern Matching)
- **Type:** Structural pattern matching
- **Methods:** `__match_args__` for dataclasses
- **Example:**
  ```python
  # DevOps: Service status patterns
  def get_service_health(status):
      match status:
          case 0 | 1 | 2:
              return "UP"  # 0: running, 1: starting, 2: healthy
          case 3 | 4:
              return "DEGRADED"  # 3: degraded, 4: warning
          case 5 | 6 | 7 | 8 | 9:
              return "DOWN"  # All error states
          case _:
              return "UNKNOWN"
  ```

### `for` and `in`
- **Type:** Iteration and membership
- **Methods:** `__iter__()`, `__contains__()`
- **Example:**
  ```python
  # DevOps: Process multiple services
  services = ["nginx", "apache", "docker", "ssh"]
  for service in services:
      if service in active_services():
          print(f"Service {service} is running")
  ```

### `while` and `break/continue`
- **Type:** Loop control
- **Methods:** `break` exits, `continue` skips
- **Example:**
  ```python
  # DevOps: Retry loop with timeout
  def wait_for_service(service_name, timeout=30):
      retries = 0
      while retries < timeout:
          if check_service(service_name):
              print(f"Service {service_name} is up")
              break
          retries += 1
          time.sleep(1)
      else:
          print(f"Timeout waiting for {service_name}")
  ```

### `and`, `or`, `not` (Logical Operators)
- **Type:** Boolean logic
- **Methods:** `__and__`, `__or__`, `__not__`
- **Example:**
  ```python
  # DevOps: Complex condition checks
  def can_start_service(service_config):
      has_deps = all(dep in running_services for dep in service_config.get('dependencies', []))
      return (has_deps and not service_config.get('maintenance_mode', False))
  ```

### Comprehensions Intro
- **Type:** List/dict/set comprehensions
- **Methods:** `__iter__()`, `__contains__()`
- **Example:**
  ```python
  # DevOps: List comprehension for port status
  open_ports = [80, 443, 8080, 8081, 3306]
  standard_ports = [p for p in open_ports if p < 1024]
  
  # Dict comprehension for service status map
  status_map = {port: 'UP' for port in [80, 443] if check_port(port)}
  ```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day04 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day04 -v` — see `tests/day04/test_day04.py`
