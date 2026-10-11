# Day 02 — Objects and Variables

Keywords: `None, True, False, is, in`

## Keywords + Methods

### `None` (Deep Dive)
- **Type:** `NoneType` (Singleton)
- **Methods:** `None.__bool__()` → `False`
- **Example:**
  ```python
  # Sentinel for missing environment variables
  import os
  db_host = os.getenv('DB_HOST') # Returns None if not set
  
  if db_host is None:
      print("Warning: DB_HOST not set, using localhost")
      db_host = '127.0.0.1'
  ```

### `True`, `False` (Boolean-Int relationship)
- **Type:** `bool` (subclass of `int`)
- **Methods:** `int.bit_length()` (since bools are ints)
- **Example:**
  ```python
  # Bools are 1 and 0
  print(True + True)   # 2
  print(False * 10)    # 0
  
  status_code = 0
  is_success = not status_code # 0 is False, so not 0 is True
  
  # bit_length of 1 (True) is 1, 0 (False) is 0
  print(True.bit_length()) 
  ```

### `is` vs `==`
- **Type:** Identity vs Equality
- **Methods:** `id()` to check memory address
- **Example:**
  ```python
  # Identity check (same object in memory)
  a = [1, 2, 3]
  b = a
  c = list(a)
  
  print(a is b) # True (points to same object)
  print(a is c) # False (different object in memory)
  print(a == c) # True (values are equal)
  
  # Always use 'is' for None
  if db_host is None:
      pass
  ```

### `in` (Membership)
- **Type:** Membership operator
- **Methods:** `__contains__`
- **Example:**
  ```python
  # Check if service in restricted list
  blocked_ips = ["192.168.1.50", "10.0.0.8"]
  current_ip = "10.0.0.8"
  
  if current_ip in blocked_ips:
      print(f"Access denied for {current_ip}")
  ```

## Object Model Concepts

### Variables as Names (References)
- Python variables are tags/labels, not boxes.
- Assignment `x = y` makes `x` refer to same object as `y`.

### Dynamic Typing
- Variable `x` can change type because it just points to objects.
  ```python
  x = "nginx"   # x is str
  x = 80        # x is now int
  ```

### Assignment & Unpacking
  ```python
  # Augmented assignment
  count = 0
  count += 1 # count = count + 1
  
  # Unpacking (Multiple assignment)
  cpu_load, mem_usage = (0.5, 85)
  print(f"CPU: {cpu_load}, Mem: {mem_usage}%")
  ```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day02 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day02 -v` — see `tests/day02/test_day02.py`
