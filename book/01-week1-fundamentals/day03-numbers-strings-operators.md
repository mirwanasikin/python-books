# Day 03 — Numbers, Strings, and Operators

Keywords: `and, or, not, in`

## Keywords + Methods

### Numbers (`int`, `float`, `complex`)
- **Type:** Numeric types
- **Methods:** `int.bit_length()`, `float.is_integer()`
- **Example:**
  ```python
  # DevOps: Port numbers and resource limits
  port = 8080
  print(port.bit_length()) # Bits needed to represent port
  
  load_avg = 1.75
  print(load_avg.is_integer()) # False
  ```

### Strings (`str`)
- **Type:** Immutable text sequences
- **Methods:** `str.split()`, `str.join()`, `str.strip()`, `str.replace()`, `str.upper()`, `str.lower()`, `str.startswith()`
- **Example:**
  ```python
  # DevOps: Parsing df -h output line
  line = " /dev/sda1      50G   20G    30G   40% /"
  parts = line.split()
  mount_point = parts[-1]
  usage_pct = parts[-2].replace('%', '')
  
  print(f"Mount: {mount_point}, Usage: {usage_pct}%")
  ```

### Operators (Arithmetic, Comparison, Logical, Bitwise, Identity, Membership)
- **Type:** Operator symbols
- **Methods:** `__add__`, `__eq__`, `__and__`, etc.
- **Example:**
  ```python
  # Arithmetic
  max_connections = 1024 * 2
  
  # Comparison & Logical
  cpu_pct = 85.5
  memory_pct = 90.0
  is_critical = (cpu_pct > 80.0) and (memory_pct > 85.0)
  
  # Bitwise (Permissions chmod simulation)
  READ = 4
  WRITE = 2
  EXEC = 1
  file_perm = READ | WRITE # 6
  has_write = bool(file_perm & WRITE)
  ```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day03 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day03 -v` — see `tests/day03/test_day03.py`
