# Day 10 — Errors, Context Managers, and Assertions

Keywords: `try, except, finally, raise, assert, with`

## Keywords + Methods

### `try`, `except`, `finally`
- **Type:** Exception handling
- **Methods:** `try:` block code, `except ExceptionType:` handle errors, `finally:` cleanup code
- **Example:**
  ```python
  def read_service_config(service_name):
      """Read service configuration with proper error handling"""
      config_path = f"/etc/{service_name}.conf"
      
      try:
          with open(config_path) as f:
              config = json.load(f)
          print(f"✓ Loaded config from {config_path}")
          return config
      except FileNotFoundError:
          print(f"✗ Config file {config_path} not found")
          return None
      except json.JSONDecodeError as e:
          print(f"✗ Invalid JSON in {config_path}: {e}")
          return None
      except PermissionError:
          print(f"✗ No permission to read {config_path}")
          return None
      except Exception as e:
          print(f"✗ Unexpected error reading {config_path}: {e}")
          return None
      finally:
          print(f"Config read attempt for {service_name} completed")
  
  # Use in deployment script
  nginx_config = read_service_config('nginx')
  if nginx_config:
      apply_changes(nginx_config)
  ```

### `raise`
- **Type:** Exception raising
- **Methods:** `raise ExceptionType('message')` to raise or re-raise exceptions
- **Example:**
  ```python
  class ServiceError(Exception):
      """Base exception for service-related errors"""
      pass
  
  class InvalidConfigError(ServiceError):
      """Raised when configuration is invalid"""
      pass
  
  def validate_disk_config(config):
      """Validate disk configuration and raise errors for invalid values"""
      if not config.get('mount_point'):
          raise InvalidConfigError("mount_point is required")
      
      if not 0 < config.get('threshold', 0) <= 100:
          raise InvalidConfigError("threshold must be between 1 and 100")
      
      if config.get('alert_level') not in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
          raise InvalidConfigError("alert_level must be LOW, MEDIUM, HIGH, or CRITICAL")
      
      return True
  
  try:
      disk_config = {'mount_point': '/data', 'threshold': 90}
      validate_disk_config(disk_config)
      print(f"✓ Validated: {disk_config}")
  except InvalidConfigError as e:
      print(f"✗ Config error: {e}")
      # Could implement recovery logic here
  except ServiceError as e:
      print(f"✗ Service error: {e}")
      send_alert(f"Service configuration failed: {e}")
  
  # Re-raising with context
  def read_with_validation(path):
      try:
          data = read_file(path)
      except IOError as e:
          raise ServiceError(f"Failed to read {path}") from e
  ```

### `assert`
- **Type:** Assertion for debugging
- **Methods:** `assert condition, message` raises AssertionError if condition is False
- **Example:**
  ```python
  def check_disk_health(path='/'):
      """Check disk health with assertions for debugging"""
      import shutil
      
      usage = (shutil.disk_usage(path).used / shutil.disk_usage(path).total) * 100
      
      # Assertions for development/debugging
      assert isinstance(path, str), "path must be string"
      assert path.startswith('/'), "path must start with /"
      assert 0 <= usage <= 100, f"usage must be 0-100%, got {usage}%"
      
      if usage > 95:
          raise ServiceError(f"Critical: {path} at {usage:.1f}% used")
      
      if usage > 85:
          print(f"WARNING: {path} at {usage:.1f}% used")
      
      return usage
  
  # Use assertions in automated tests
  def run_disk_health_checks():
      test_paths = ['/root', '/home', '/var', '/tmp']
      
      for path in test_paths:
          try:
              usage = check_disk_health(path)
              log_health_check(path, usage)
          except (AssertionError, ServiceError) as e:
              print(f"✗ Check failed for {path}: {e}")
              send_alert(f"Health check failed for {path}: {e}")
  
  run_disk_health_checks()
  ```

### `with`
- **Type:** Context manager
- **Methods:** `with expression as variable:` ensures cleanup even if exceptions occur
- **Example:**
  ```python
  def process_log_file(log_path):
      """Process log file with automatic cleanup"""
      with open(log_path, 'r') as log_file:
          lines = log_file.readlines()
          print(f"Read {len(lines)} lines from {log_path}")
      
      # File automatically closed even if processing fails
      processed_count = 0
      for line in lines:
          try:
              processed_count += process_log_line(line)
          except Exception as e:
              print(f"Failed to process line: {e}")
              continue
      
      return processed_count
  
  def manage_resources():
      """Manage multiple resources with context managers"""
      # Multiple context managers for different operations
      with open('/var/log/system.log', 'r') as log_file, \
           open('/tmp/processed.log', 'w') as output_file:
          
          for line in log_file:
              # Process each line and write to output
              processed = analyze_log_line(line)
              output_file.write(processed)
      
      print("Log processing completed")
  
  # Custom context manager for API operations
  from contextlib import contextmanager
  
  @contextmanager
  def api_connection(url, timeout=30):
      """Context manager for API connections"""
      client = connect_to_api(url)
      try:
          yield client
      finally:
          client.close()
          print(f"API connection to {url} closed")
  
  # Use with API calls
  with api_connection('https://api.example.com/metrics') as client:
      metrics = client.get_metrics()
      print(f"Retrieved {len(metrics)} metrics")
  ```

## Context Managers
- **Type:** Automatic resource management
- **Methods:** Classes with `__enter__()` and `__exit__()` methods
- **Example:**
  ```python
  class LogRotator:
      """Context manager for log rotation"""
      def __init__(self, log_file, max_size=10*1024*1024):
          self.log_file = log_file
          self.max_size = max_size
          self.backup_file = f"{log_file}.backup"
      
      def __enter__(self):
          if os.path.exists(self.log_file):
              size = os.path.getsize(self.log_file)
              if size > self.max_size:
                  print(f"Rotating log {self.log_file} ({size} bytes)")
                  if os.path.exists(self.backup_file):
                      os.remove(self.backup_file)
                  os.rename(self.log_file, self.backup_file)
          return self
      
      def __exit__(self, exc_type, exc_val, exc_tb):
          print(f"Log rotator finished for {self.log_file}")
          # Cleanup can happen here if needed
  
  def write_log_with_rotation(message, log_file='/var/log/app.log'):
      """Write log message with automatic rotation"""
      with LogRotator(log_file):
          with open(log_file, 'a') as f:
              f.write(f"{datetime.now()}: {message}\n")
      
      # Original log file can be processed after rotation
      if os.path.exists(f"{log_file}.backup"):
          process_backup_log(f"{log_file}.backup")
  
  # Usage example
  write_log_with_rotation("Starting service deployment")
  write_log_with_rotation("Service deployed successfully")
  ```

## DevOps Context
Error handling and context managers are essential for reliable DevOps:

- **API error handling**: Graceful handling of network failures, authentication errors
- **File operations**: Safe reading/writing with automatic cleanup and rotation
- **Resource management**: Ensure connections, locks, and temporary files are always cleaned up
- **Configuration validation**: Validate settings with clear error messages and recovery options

### Error Handling in API Operations
```python
import requests
from contextlib import contextmanager

class APIError(Exception):
    """Base exception for API errors"""
    pass

@contextmanager
def api_session(base_url, timeout=30, retries=3):
    """Context manager for API sessions with retry logic"""
    session = requests.Session()
    session.timeout = timeout
    
    try:
        for attempt in range(retries):
            try:
                yield session
                break
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    raise APIError(f"API request failed after {retries} attempts: {e}")
                print(f"Retry {attempt + 1}/{retries}...")
                time.sleep(2 ** attempt)  # Exponential backoff
    finally:
        session.close()

def get_service_status(service_name):
    """Get service status from API with comprehensive error handling"""
    try:
        with api_session(f"https://api.example.com/services/{service_name}") as session:
            response = session.get('/')
            response.raise_for_status()  # Raise HTTPError for bad responses
            
            data = response.json()
            return {
                'status': data.get('status', 'unknown'),
                'last_check': data.get('last_check'),
                'health': data.get('health', False)
            }
    except APIError as e:
        print(f"✗ API error for {service_name}: {e}")
        send_alert(f"Service {service_name} API error: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        print(f"✗ Invalid JSON response for {service_name}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error checking {service_name}: {e}")
        return None

# Use in monitoring script
for service in ['nginx', 'apache', 'redis', 'postgres']:
    status = get_service_status(service)
    if status:
        log_service_status(service, status)
```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day10 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day10 -v` — see `tests/day10/test_day10.py`