# Day 06 — Dicts and Sets

Keywords: `import, from, with, del, as`

## Keywords + Methods

### Dictionaries (`dict`)
- **Type:** Mutable mappings
- **Methods:** `get()`, `keys()`, `values()`, `items()`, `update()`, `setdefault()`, `pop()`, `clear()`, `copy()`
- **Example:**
  ```python
  # DevOps: Service configuration dictionary
  config = {
      'web_port': 8080,
      'log_level': 'INFO',
      'max_connections': 100,
      'ssl_enabled': True
  }
  
  # Get service port with default
  port = config.get('port', 8000)
  
  # Iterate over config
  for key, value in config.items():
      print(f"{key}: {value}")
  
  # Update config with runtime values
  runtime_config = {'log_level': 'DEBUG'}
  config.update(runtime_config)
  ```

### Sets (`set`)
- **Type:** Unordered collections (no duplicates)
- **Methods:** `add()`, `update()`, `remove()`, `discard()`, `pop()`, `clear()`, `copy()`
- **Example:**
  ```python
  # DevOps: Track active connections by IP
  active_connections = {'192.168.1.10', '10.0.0.5', '172.16.0.8'}
  
  # Add new connections
  new_connections = {'192.168.1.11', '10.0.0.6'}
  active_connections.update(new_connections)
  
  # Deduplicate server list
  servers = ['web01', 'web01', 'db01', 'web02', 'db01']
  unique_servers = list(set(servers))
  ```

### Set Operations
- **Type:** Set theory operations
- **Methods:** `union()`, `intersection()`, `difference()`, `symmetric_difference()`
- **Example:**
  ```python
  # DevOps: Compare running vs configured services
  running_services = {'nginx', 'apache', 'docker'}
  configured_services = {'nginx', 'apache', 'ssh'}
  
  # Services running but not configured
  extra_services = running_services - configured_services
  
  # Services in either list
  all_services = running_services | configured_services
  
  # Services in both lists
  common_services = running_services & configured_services
  ```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day06 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day06 -v` — see `tests/day06/test_day06.py`
