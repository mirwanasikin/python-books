# Day 05 — Lists and Tuples

Keywords: `for, in, break, continue, pass`

## Keywords + Methods

### Lists (`list`)
- **Type:** Mutable sequences
- **Methods:** `append()`, `extend()`, `pop()`, `sort()`, `reverse()`, `insert()`, `remove()`, `clear()`, `copy()`
- **Example:**
  ```python
  # DevOps: Managing a list of server names
  servers = ['web01', 'web02', 'db01', 'cache01']
  
  # Add servers
  servers.append('monitor01')
  
  # Add multiple servers at once
  new_servers = ['log01', 'log02']
  servers.extend(new_servers)
  
  # Restart all web servers
  for server in servers:
      if server.startswith('web'):
          restart_server(server)
      else:
          continue
  
  # Install monitoring on web01
  if servers:
      servers[0] = 'monitor01'
  ```

### Tuples (`tuple`)
- **Type:** Immutable sequences
- **Methods:** `index()`, `count()`
- **Example:**
  ```python
  # DevOps: Port and service pairs (immutable)
  port_services = [(80, 'nginx'), (443, 'apache'), (3306, 'mysql')]
  
  # Tuple unpacking
  for port, service in port_services:
      print(f"Port {port} -> {service}")
  
  # Find index of port 3306
  mysql_index = port_services.index((3306, 'mysql'))
  ```

### Slicing and Mutation
- **Type:** Sequence operations
- **Methods:** `slice`, `__getitem__`, `__setitem__`
- **Example:**
  ```python
  # DevOps: Get list of web servers using slice
  servers = ['web01', 'web02', 'db01', 'cache01', 'web03']
  web_servers = servers[0::2]  # Every other server starting from index 0
  
  # Modify list
  servers[1] = 'web04'  # Replace web02 with web04
  servers[2:4] = ['db02', 'cache02']  # Replace slice
  ```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day05 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day05 -v` — see `tests/day05/test_day05.py`
