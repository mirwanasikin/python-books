# Day 08 — Functions

Keywords: `def, return, lambda`

## Keywords + Methods

### `def`
- **Type:** Function definition
- **Methods:** `def function_name(parameters):` creates a function object
- **Example:**
  ```python
  def check_disk(path='/', threshold=80):
      """Check disk usage and warn if above threshold"""
      import shutil
      try:
          usage = shutil.disk_usage(path)
          percent_used = (usage.used / usage.total) * 100
          if percent_used > threshold:
              print(f"WARNING: Disk usage at {path} is {percent_used:.1f}%")
              return False
          return True
      except Exception as e:
          print(f"ERROR checking disk {path}: {e}")
          return False
  
  # Usage in DevOps script
  if not check_disk('/'):
      send_alert('Root disk is filling up!')
  ```

### `return`
- **Type:** Return value from function
- **Methods:** `function_name()` returns specified value, can return multiple values as tuple
- **Example:**
  ```python
  def analyze_disk_space(mount_points=['/', '/home', '/var']):
      """Analyze disk space across multiple mount points"""
      results = []
      for point in mount_points:
          import shutil
          usage = shutil.disk_usage(point)
          percent = (usage.used / usage.total) * 100
          results.append((point, percent, usage.free))
      return results
  
  # Process disk analysis
  disk_report = analyze_disk_space()
  for mount, usage, free in disk_report:
      if usage > 90:
          print(f"CRITICAL: {mount} at {usage:.1f}% used")
  ```

### `lambda`
- **Type:** Anonymous function
- **Methods:** `lambda parameters: expression` - single expression function
- **Example:**
  ```python
  # Lambda for sorting services by usage
  services = {'web': 85, 'db': 92, 'cache': 78}
  sorted_services = sorted(services.items(), key=lambda x: x[1], reverse=True)
  
  # Lambda for disk health check
  is_healthy = lambda usage: usage < 85
  disk_usages = [75, 82, 91, 68]
  healthy_disks = list(filter(is_healthy, disk_usages))
  
  # Lambda for log level classification
  classify_log = lambda level: 'CRITICAL' if level >= 90 else 'WARN' if level >= 70 else 'INFO'
  log_levels = [95, 45, 80, 30]
  levels = list(map(classify_log, log_levels))
  ```

## DevOps Context
Functions are the building blocks of DevOps automation. They enable:

- **Reusable operations**: `check_disk()` checks multiple mounts consistently
- **Data processing**: `analyze_disk_space()` returns structured data for reporting
- **Error handling**: Functions can isolate failures and provide meaningful messages
- **Configuration management**: Functions can read config files and validate settings

### Reusable Check Function Example
```python
def validate_service_config(service_name, config_file='/etc/services.conf'):
    """Validate service configuration file"""
    try:
        with open(config_file) as f:
            config = json.load(f)
        if service_name in config:
            print(f"✓ {service_name} config is valid")
            return config[service_name]
        else:
            print(f"✗ {service_name} not found in config")
            return None
    except FileNotFoundError:
        print(f"✗ Config file {config_file} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in {config_file}: {e}")
        return None

# Use in deployment script
nginx_config = validate_service_config('nginx')
if nginx_config:
    deploy_service('nginx', nginx_config)
```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day08 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day08 -v` — see `tests/day08/test_day08.py`