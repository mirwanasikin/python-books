# Day 09 — Scope, Closures, and Decorators

Keywords: `global, nonlocal`

## Keywords + Methods

### `global`
- **Type:** Global variable declaration
- **Methods:** `global variable_name` allows function to modify global scope variable
- **Example:**
  ```python
  # Global configuration for monitoring
  LOG_LEVEL = 'INFO'
  ALERT_THRESHOLD = 90
  
  def update_config(new_level, new_threshold):
      """Update global configuration values"""
      global LOG_LEVEL, ALERT_THRESHOLD
      global LOG_LEVEL
      LOG_LEVEL = new_level
      ALERT_THRESHOLD = new_threshold
      print(f"Config updated: LOG_LEVEL={LOG_LEVEL}, ALERT_THRESHOLD={ALERT_THRESHOLD}")
  
  def get_disk_alert_level(usage):
      """Check if disk usage exceeds global alert threshold"""
      if usage > ALERT_THRESHOLD:
          return f"CRITICAL: Disk at {usage}% (threshold: {ALERT_THRESHOLD}%)"
      return None
  
  # Initialize global state
  update_config('WARNING', 85)
  result = get_disk_alert_level(92)
  print(result)
  ```

### `nonlocal`
- **Type:** Enclosing scope variable declaration
- **Methods:** `nonlocal variable_name` allows nested function to modify enclosing function's variable
- **Example:**
  ```python
  def create_counter():
      """Factory function that returns a closure with nonlocal state"""
      count = 0  # This is in the enclosing scope
      
      def increment():
          nonlocal count
          count += 1
          return count
      
      def get_count():
          return count
      
      return increment, get_count
  
  # Create multiple counters
  web_counter, web_get = create_counter()
  db_counter, db_get = create_counter()
  
  # Use counters independently
  for _ in range(3):
      print(f"Web requests: {web_counter()}")
  
  for _ in range(2):
      print(f"DB connections: {db_counter()}")
  ```

## Closures
- **Type:** Function that captures variables from enclosing scope
- **Methods:** Functions retain access to enclosing scope even after it's gone
- **Example:**
  ```python
  def make_disk_checker(threshold):
      """Factory function that returns a closure for disk checking"""
      def check_disk(path='/'):
          import shutil
          usage = (shutil.disk_usage(path).used / shutil.disk_usage(path).total) * 100
          return usage > threshold
      
      return check_disk
  
  # Create specialized checkers for different thresholds
  critical_checker = make_disk_checker(95)
  warning_checker = make_disk_checker(85)
  
  # Use checkers independently
  for path in ['/root', '/home', '/var']:
      if warning_checker(path):
          print(f"WARNING: {path} usage is high")
  
  if critical_checker('/root'):
      send_emergency_alert('Root partition critical!')
  ```

## Decorators
- **Type:** Function that modifies another function's behavior
- **Methods:** Use `@decorator` syntax or `decorator(function)` wrapper
- **Example:**
  ```python
  import time
  from functools import wraps
  
  def log_execution(func):
      """Decorator to log function execution time"""
      @wraps(func)
      def wrapper(*args, **kwargs):
          start = time.time()
          result = func(*args, **kwargs)
          duration = time.time() - start
          print(f"{func.__name__} executed in {duration:.3f}s")
          return result
      return wrapper
  
  def retry(max_attempts=3, delay=1):
      """Decorator to retry function execution on failure"""
      def decorator(func):
          @wraps(func)
          def wrapper(*args, **kwargs):
              attempts = 0
              while attempts < max_attempts:
                  try:
                      return func(*args, **kwargs)
                  except Exception as e:
                      attempts += 1
                      if attempts >= max_attempts:
                          raise
                      print(f"Retry {attempts}/{max_attempts} after error: {e}")
                      time.sleep(delay)
          return wrapper
      return decorator
  
  # DevOps decorators in action
  @log_execution
  def deploy_service(service_name):
      """Simulate service deployment"""
      print(f"Deploying {service_name}...")
      time.sleep(1)
      print(f"{service_name} deployed successfully")
      return True
  
  @retry(max_attempts=3, delay=2)
  def check_service_health(service_name):
      """Check if service is healthy"""
      if service_name == 'unstable':
          raise Exception(f"Service {service_name} is down")
      print(f"Service {service_name} is healthy")
      return True
  
  # Run decorated functions
  deploy_service('nginx')
  check_service_health('nginx')
  check_service_health('unstable')  # Will retry
  ```

## DevOps Context
Global and nonlocal variables with closures and decorators are powerful for DevOps:

- **Global state**: Config values like thresholds and levels shared across functions
- **Service monitoring**: Closures capture threshold values for specific checks
- **Error resilience**: Retry decorators handle transient failures in deployments
- **Performance tracking**: Execution logging helps identify slow operations

### Timing Decorator for Deployments
```python
import time
from functools import wraps

def timing_decorator(func):
    """Decorator to measure deployment time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        
        # Log to monitoring system
        print(f"Deployment completed in {duration:.2f} seconds")
        
        # Update metrics
        if result:
            update_deployment_metrics(func.__name__, duration, True)
        else:
            update_deployment_metrics(func.__name__, duration, False)
            
        return result
    return wrapper

# Deploy with timing
@timing_decorator
def deploy_with_rollback(service_name, config):
    """Deploy service with automatic rollback on failure"""
    try:
        backup_current_config(service_name)
        apply_new_config(service_name, config)
        restart_service(service_name)
        
        # Health check
        if health_check(service_name):
            print(f"✓ {service_name} deployed successfully")
            return True
        else:
            raise Exception("Health check failed")
    except Exception as e:
        print(f"✗ Deployment failed: {e}")
        rollback_service(service_name)
        return False
```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day09 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day09 -v` — see `tests/day09/test_day09.py`