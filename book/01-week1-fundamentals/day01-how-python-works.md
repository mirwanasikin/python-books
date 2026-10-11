# Day 01 — How Python Works

Keywords: `None, True, False, and, or, not, is, in, if, elif, else, match, case, for, while, break, continue, pass, import, as`

## Keywords + Methods

### `None`
- **Type:** Singleton NoneType
- **Method:** `None.__repr__()` → string `'None'`
- **Example:**
  ```python
  result = None
  if result is None:
      print('No result')
  ```

### `True`, `False`
- **Type:** bool (subclass of int)
- **Methods:** `True.__and__(other)`, `True.__or__(other)`, `True.__invert__()`, `False.__bool__()`
- **Example:**
  ```python
  user_active = True
  if user_active:
      print('User is active')
  
  # Boolean logic
  authenticated = False and password_check
  ```

### `and`, `or`, `not`
- **Type:** Binary/Boolean operators
- **Methods:** None (operators)
- **Example:**
  ```python
  # Chaining conditions for Linux checks
  if has_sudo_rights and is_root:
      run_system_command('systemctl restart nginx')
  
  # Fallback logic
  if not cached and fetch_from_api():
      cache_result()
  
  # Range check using or
  if port in [80, 443, 8080] or (1024 <= port <= 49151):
      open_port(port)
  ```

### `is`, `in`
- **Type:** Identity/Membership operators
- **Methods:** `x in y` uses `y.__contains__(x)`, `x is y` compares identity
- **Example:**
  ```python
  # Using is for None checks (recommended)
  if config is None:
      config = load_default_config()
  
  # Membership for service names
  service = 'nginx'
  if service in ['nginx', 'apache', 'httpd']:
      reload_webserver(service)
  ```

### `if`, `elif`, `else`
- **Type:** Conditional statements
- **Methods:** None (control flow)
- **Example:**
  ```python
  def get_service_status(service_name):
      if service_name == 'nginx':
          return check_nginx_status()
      elif service_name == 'apache':
          return check_apache_status()
      else:
          return check_generic_service(service_name)
  ```

### `match`, `case` (structural pattern matching)
- **Type:** Pattern matching statements
- **Methods:** None (control flow)
- **Example:**
  ```python
  def get_log_level(level):
      match level:
          case 0 | 1 | 2:
              return 'ERROR'
          case 3 | 4 | 5:
              return 'WARN'
          case 6 | 7 | 8:
              return 'INFO'
          case _:
              return 'UNKNOWN'
  ```

### `for`, `while`
- **Type:** Iteration loops
- **Methods:** `for x in iterable:` uses `iterable.__iter__()`, `while condition:` loops until False
- **Example:**
  ```python
  # Process list of services
  services = ['nginx', 'apache', 'docker', 'ssh']
  for service in services:
      if service in active_services():
          restart_service(service)
      else:
          start_service(service)
  
  # Wait for process with timeout
  timeout = 30
  elapsed = 0
  while elapsed < timeout and not process_complete:
      time.sleep(1)
      elapsed += 1
  ```

### `break`, `continue`
- **Type:** Loop control
- **Methods:** None (control flow)
- **Example:**
  ```python
  # Find first critical service
  critical_services = ['ssh', 'docker', 'cron']
  for service in critical_services:
      if is_service_critical(service):
          print(f'Critical: {service}')
          break
  
  # Skip non-critical services
  for service in all_services:
      if not is_service_critical(service):
          continue
      restart_service(service)
  ```

### `pass`
- **Type:** No-op, placeholder
- **Method:** None
- **Example:**
  ```python
  # Placeholder for future implementation
  def temp_script():
      pass  # TODO: implement log rotation
  
  # Match case with no operation
  match value:
      case 'temp':
          pass  # will be handled elsewhere
  ```

### `import`, `as`
- **Type:** Module/namespace management
- **Methods:** `import module`, `from module import name`, `import module as alias`
- **Example:**
  ```python
  # Import standard library
  import os
  import sys
  import subprocess
  
  # Import with alias for convenience
  import psutil as sys_monitor
  import pandas as pd
  import yaml as yaml_parser
  
  # Import specific functions
  from datetime import datetime, timedelta
  from pathlib import Path
  
  # DevOps context
  import json
  import shlex
  from typing import List, Dict, Optional
  ```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day01 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day01 -v` — see `tests/day01/test_day01.py`