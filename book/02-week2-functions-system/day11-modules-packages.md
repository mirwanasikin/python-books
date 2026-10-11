# Day 11 — Modules and Packages

Keywords: `import, from, as, del`

## Keywords + Methods

### `import`
- **Type:** Import module
- **Methods:** `import module_name` imports entire module, loads module once, available as module attribute
- **Example:**
  ```python
  # Import standard library modules
  import os
  import sys
  import subprocess
  import json
  import time
  
  # Import third-party modules
  import psutil
  import yaml
  import requests
  
  # DevOps: System module usage
  def get_system_info():
      """Get system information using os and platform"""
      import platform
      
      info = {
          'system': platform.system(),
          'release': platform.release(),
          'python_version': sys.version,
          'cwd': os.getcwd(),
          'env': dict(os.environ)
      }
      
      print("System Information:")
      for key, value in info.items():
          print(f"  {key}: {value}")
      
      return info
  
  # Use in automation script
  system_info = get_system_info()
  log_system_info(system_info)
  ```

### `from`
- **Type:** Import from module
- **Methods:** `from module import name` imports specific name(s), avoids module namespace pollution
- **Example:**
  ```python
  # Import specific functions/classes
  from datetime import datetime, timedelta
  from pathlib import Path
  from collections import defaultdict, Counter
  
  # Import all (not recommended)
  from os import *  # Import all os functions
  
  # DevOps: Import helpers from package
  from .utils import log_error, format_bytes
  from .config import get_config
  
  def configure_logging(config_file='/etc/logging.conf'):
      """Configure logging using imported utilities"""
      try:
          config = get_config(config_file)
      except ImportError as e:
          print(f"Config not available: {e}")
          config = {}
      
      # Setup logging
      log_level = config.get('level', 'INFO')
      log_file = config.get('file', '/var/log/app.log')
      
      setup_logging(level=log_level, file=log_file)
      print(f"Logging configured: level={log_level}, file={log_file}")
  
  # Use in service automation
  configure_logging()
  
  # Import for comparison
  compare = lambda a, b: a > b
  ```

### `as`
- **Type:** Import alias
- **Methods:** `import module as alias` creates short alias for module
- **Example:**
  ```python
  # Create convenient aliases
  import pandas as pd
  import numpy as np
  import yaml as yaml_parser
  import json as json_parser
  
  # DevOps: System monitoring aliases
  import psutil as sysmon
  import docker as docker_client
  import boto3 as aws
  import requests as http_client
  
  def monitor_system_resources():
      """Monitor system resources using aliased modules"""
      # CPU monitoring
      cpu_percent = sysmon.cpu_percent(interval=1)
      print(f"CPU usage: {cpu_percent}%")
      
      # Memory monitoring
      mem = sysmon.virtual_memory()
      print(f"Memory: {mem.percent}% used")
      
      # Disk monitoring
      disk = sysmon.disk_usage('/')
      print(f"Disk: {disk.percent}% used")
      
      return {'cpu': cpu_percent, 'memory': mem.percent, 'disk': disk.percent}
  
  def check_docker_services():
      """Check Docker container status"""
      try:
          client = docker_client.from_env()
          containers = client.containers.list(all=True)
          
          running = []
          stopped = []
          
          for container in containers:
              if container.status == 'running':
                  running.append(container.name)
              else:
                  stopped.append(container.name)
          
          print(f"Running containers: {running}")
          print(f"Stopped containers: {stopped}")
          
          return {'running': running, 'stopped': stopped}
      except Exception as e:
          print(f"Failed to connect to Docker: {e}")
          return None
  
  # Use monitoring in production script
  monitor_system_resources()
  check_docker_services()
  ```

### `del`
- **Type:** Delete variable/module
- **Methods:** `del variable_name` removes variable from namespace, frees memory
- **Example:**
  ```python
  def cleanup_imported_modules():
      """Clean up unused imported modules"""
      # Import large module conditionally
      LARGE_MODULES = ['pandas', 'numpy', 'tensorflow']
      
      for module in LARGE_MODULES:
          try:
              # Try to import, delete if not available
              __import__(module)
              print(f"Module {module} is available")
              
              # Delete if not needed in current context
              if module == 'numpy' and not need_numpy_processing():
                  del np  # Delete alias if numpy not needed
          except ImportError:
              print(f"Module {module} not installed")
      
      # Clear reference to large data
      data_cache = None
      del data_cache
  
  # Use in memory-constrained environments
  if not is_memory_constrained():
      import pandas as pd
      # Use pandas for data processing
      large_data = pd.read_csv('large_dataset.csv')
      
      # Clean up when done
      large_data = None
      del pd
  
  # Module cleanup function
  def safe_import(module_name, as_name=None):
      """Safely import module with optional cleanup"""
      try:
          module = __import__(module_name)
          
          if as_name:
              globals()[as_name] = module
              print(f"Imported {module_name} as {as_name}")
          else:
              print(f"Imported {module_name}")
          
          return module
      except ImportError as e:
          print(f"Failed to import {module_name}: {e}")
          return None
  
  # Use safe import
  json_utils = safe_import('json', as_name='json_parser')
  if json_utils:
      print("JSON utilities loaded")
  ```

## Packages
- **Type:** Directory with `__init__.py` for import
- **Methods:** Create package structure, use `import package.module`, subpackages supported
- **Example:**
  ```python
  # Create directory structure
  # automation/
  #   __init__.py
  #   system/
  #     __init__.py
  #     monitoring.py
  #     config.py
  #   deployment/
  #     __init__.py
  #     k8s.py
  #     ansible.py
  
  # Package __init__.py
  from .system import monitor_cpu, monitor_memory, monitor_disk
  from .deployment import deploy_kubernetes, deploy_ansible
  
  def run_full_monitoring():
      """Run all monitoring using package"""
      print("Starting full system monitoring...")
      
      # Use imported functions
      cpu_info = monitor_cpu()
      mem_info = monitor_memory()
      disk_info = monitor_disk()
      
      return {'cpu': cpu_info, 'memory': mem_info, 'disk': disk_info}
  
  def deploy_new_service(service_config):
      """Deploy using package functions"""
      deployment_type = service_config.get('type', 'kubernetes')
      
      if deployment_type == 'kubernetes':
          return deploy_kubernetes(service_config)
      elif deployment_type == 'ansible':
          return deploy_ansible(service_config)
      else:
          raise ValueError(f"Unknown deployment type: {deployment_type}")
  
  # Use package
  monitoring_data = run_full_monitoring()
  print(f"Monitoring data: {monitoring_data}")
  
  # Deploy new service
  config = {'name': 'webapp', 'type': 'kubernetes', 'version': 'v2.0'}
  deploy_new_service(config)
  ```

## Import System
- **Type:** Python's module import mechanism
- **Methods:** `sys.path` controls import search, `__init__.py` makes directory a package
- **Example:**
  ```python
  import sys
  import os
  
  def add_script_path(script_path):
      """Add custom path to sys.path for module imports"""
      if script_path not in sys.path:
          sys.path.insert(0, script_path)
          print(f"Added {script_path} to Python path")
      else:
          print(f"{script_path} already in Python path")
  
  def find_module_in_paths(module_name):
      """Search for module in sys.path"""
      for path in sys.path:
          module_path = os.path.join(path, f"{module_name}.py")
          if os.path.exists(module_path):
              return module_path
          
          package_path = os.path.join(path, module_name, "__init__.py")
          if os.path.exists(package_path):
              return package_path
      
      return None
  
  # Set up Python path for DevOps scripts
  script_dir = '/opt/automation/scripts'
  add_script_path(script_dir)
  
  # Find custom modules
  module_path = find_module_in_paths('log_processor')
  if module_path:
      print(f"Found module at: {module_path}")
      # Dynamic import
      import importlib.util
      spec = importlib.util.spec_from_file_location("log_processor", module_path)
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)
  
  # Circular import prevention
  def create_circular_safe_import(base_module):
      """Import modules without circular dependency issues"""
      def import_module(module_name):
          if module_name == f"{base_module}.utils":
              # Import utils separately to avoid circular imports
              import importlib
              utils_module = importlib.import_module(module_name)
              return utils_module
          else:
              # Standard import
              import importlib
              return importlib.import_module(module_name)
      
      return import_module
  
  # Use with caution
  safe_import = create_circular_safe_import('web_server')
  utils = safe_import('web_server.utils')
  ```

## DevOps Context
Modules and packages organize automation scripts and tools:

- **Code organization**: Separate concerns into modules (config, monitoring, deployment)
- **Reusable components**: Package utilities for multiple scripts
- **Import management**: Control dependencies and avoid circular imports
- **Namespace management**: Use aliases for convenience and avoid conflicts

### Package Structure for Automation
```python
# automation/
#   __init__.py
#       from .system import monitor_system
#       from .deployment import deploy_service
#       from .monitoring import setup_monitoring
#   
#   system/
#       __init__.py
#       __init__.py
#           from .cpu import monitor_cpu
#           from .memory import monitor_memory  
#           from .disk import monitor_disk
#       cpu.py
#       memory.py
#       disk.py
#   
#   deployment/
#       __init__.py
#           from .k8s import deploy_kubernetes
#           from .ansible import deploy_ansible
#       k8s.py
#       ansible.py
#   
#   monitoring/
#       __init__.py
#           from .alerts import send_alert
#           from .metrics import record_metric
#       alerts.py
#       metrics.py
#   
#   utils/
#       __init__.py
#           from .helpers import format_bytes, log_error
#           from .validation import validate_config
#       helpers.py
#       validation.py

# Main automation script using package
import sys
import os

# Add automation package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from automation.system import monitor_system
from automation.deployment import deploy_service
from automation.monitoring import setup_monitoring
from automation.utils import format_bytes, validate_config

def run_automation_pipeline():
    """Run complete automation pipeline"""
    # Monitor current system
    print("Running system monitoring...")
    system_info = monitor_system()
    
    # Validate configuration
    config = validate_config('/etc/automation.conf')
    if not config:
        print("Invalid configuration, exiting")
        return
    
    # Setup monitoring
    setup_monitoring(config['monitoring'])
    
    # Deploy new version
    deployment_config = {
        'version': '2.1.0',
        'type': 'kubernetes',
        'health_check': True,
        'rollback_on_failure': True
    }
    
    result = deploy_service(deployment_config)
    if result:
        print(f"✓ Deployment successful: {result}")
    else:
        print("✗ Deployment failed")
        # Alert administrators
        send_alert("Deployment failed for critical service")
```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day11 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day11 -v` — see `tests/day11/test_day11.py`