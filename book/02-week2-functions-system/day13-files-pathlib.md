# Day 13 — Files and Pathlib

Keywords: `open, read, write, close`

## Keywords + Methods

### File Opening
- **Type:** Open file for reading/writing
- **Methods:** `open(file, mode='r', buffering=-1, encoding=None)` - standard file operations
- **Example:**
  ```python
  def read_config_file(config_path='/etc/service-config.json'):
      """Read and parse configuration file"""
      try:
          with open(config_path, 'r') as config_file:
              config_data = json.load(config_file)
          print(f"✓ Loaded configuration from {config_path}")
          return config_data
      except FileNotFoundError:
          print(f"✗ Configuration file {config_path} not found")
          return None
      except json.JSONDecodeError as e:
          print(f"✗ Invalid JSON in {config_path}: {e}")
          return None
      except PermissionError:
          print(f"✗ No permission to read {config_path}")
          return None
  
  def write_log_entry(log_file='/var/log/service.log', message="Service started"):
      """Append log entry to log file"""
      try:
          with open(log_file, 'a') as log_file_handle:
              timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
              log_entry = f"[{timestamp}] {message}\n"
              log_file_handle.write(log_entry)
          print(f"✓ Logged to {log_file}: {message}")
      except PermissionError:
          print(f"✗ No permission to write to {log_file}")
      except Exception as e:
          print(f"✗ Failed to write log: {e}")
  
  # Usage in service script
  config = read_config_file()
  if config:
      setup_service(config)
  
  write_log_entry("Service initialized successfully")
  ```

### File Reading
- **Type:** Read file content
- **Methods:** `file.read()` reads entire file, `file.readlines()` reads lines
- **Example:**
  ```python
  def read_hosts_file(hosts_path='/etc/hosts'):
      """Read hosts file and return IP-host mappings"""
      hosts = {}
      
      try:
          with open(hosts_path, 'r') as f:
              for line in f:
                  line = line.strip()
                  if not line or line.startswith('#'):
                      continue
                  
                  parts = line.split()
                  if len(parts) >= 2:
                      ip = parts[0]
                      hostnames = parts[1:]
                      hosts[ip] = hostnames
          
          print(f"✓ Read {len(hosts)} host entries from {hosts_path}")
          return hosts
      except FileNotFoundError:
          print(f"✗ Hosts file {hosts_path} not found")
          return {}
      except PermissionError:
          print(f"✗ No permission to read {hosts_path}")
          return {}
  
  def read_large_file_line_by_line(file_path):
      """Read large file efficiently line by line"""
      processed_lines = []
      
      try:
          with open(file_path, 'r') as f:
              for i, line in enumerate(f):
                  # Skip empty lines
                  if not line.strip():
                      continue
                  
                  # Process every 1000th line
                  if i % 1000 == 0:
                      processed = process_log_line(line)
                      processed_lines.append(processed)
          
          print(f"✓ Processed {len(processed_lines)} lines from {file_path}")
          return processed_lines
      except Exception as e:
          print(f"✗ Failed to read {file_path}: {e}")
          return []
  
  # Usage
  hosts = read_hosts_file()
  print(f"Found hosts: {hosts}")
  
  processed = read_large_file_line_by_line('/var/log/system.log')
  print(f"Processed {len(processed)} log entries")
  ```

### File Writing
- **Type:** Write content to file
- **Methods:** `file.write(content)`, `file.writelines(list)` write multiple lines
- **Example:**
  ```python
  def write_service_report(report_file='/tmp/service_report.txt', services=None):
      """Write service status report to file"""
      if not services:
          services = ['nginx', 'apache', 'mysql']
      
      try:
          with open(report_file, 'w') as f:
              f.write("Service Status Report\n")
              f.write("=" * 50 + "\n\n")
              
              for service in services:
                  status = check_service_status(service)
                  f.write(f"Service: {service}\n")
                  f.write(f"  Status: {status.get('status', 'unknown')}\n")
                  f.write(f"  Uptime: {status.get('uptime', 'N/A')}\n")
                  f.write(f"  PID: {status.get('pid', 'N/A')}\n")
                  f.write("\n")
          
          print(f"✓ Report written to {report_file}")
          return True
      except Exception as e:
          print(f"✗ Failed to write report: {e}")
          return False
  
  def append_json_lines(json_file='/tmp/log_entries.json', data=None):
      """Append JSON data as separate lines (JSONL format)"""
      if not data:
          return
      
      try:
          with open(json_file, 'a') as f:
              for entry in data:
                  json_line = json.dumps(entry) + "\n"
                  f.write(json_line)
          
          print(f"✓ Appended {len(data)} entries to {json_file}")
      except Exception as e:
          print(f"✗ Failed to write JSON lines: {e}")
  
  # Usage
  services = ['nginx', 'apache']
  write_service_report('/tmp/service_report.txt', services)
  
  log_entries = [
      {'timestamp': '2023-08-15 10:30:45', 'level': 'INFO', 'message': 'Service started'},
      {'timestamp': '2023-08-15 10:31:00', 'level': 'WARN', 'message': 'High memory usage'}
  ]
  append_json_lines('/tmp/service_logs.jsonl', log_entries)
  ```

### File Closing
- **Type:** Close file handle
- **Methods:** `file.close()` - automatically handled by context manager
- **Example:**
  ```python
  # Files are automatically closed by 'with' statement
  # Explicit closing (not recommended for production)
  def read_without_context(file_path):
      """Example of explicit file closing"""
      f = None
      try:
          f = open(file_path, 'r')
          content = f.read()
          return content
      finally:
          if f:
              f.close()
  
  # Never do this in production:
  # f = open("file.txt")
  # data = f.read()
  # f.close()  # If exception occurs before close, file is leaked
  
  # Best practice - always use 'with'
  def read_with_context(file_path):
      """Always use context manager for file operations"""
      with open(file_path, 'r') as f:
          content = f.read()
      # File is automatically closed here
      return content
  ```

## Pathlib
- **Type:** Object-oriented file paths
- **Methods:** `Path('/path')` create path object, `Path.exists()`, `Path.read_text()`, `Path.write_text()`
- **Example:**
  ```python
  from pathlib import Path
  
  def manage_log_directory(log_dir='/var/log/app'):
      """Manage log directory using pathlib"""
      log_path = Path(log_dir)
      
      # Check if directory exists
      if not log_path.exists():
          log_path.mkdir(parents=True, exist_ok=True)
          print(f"✓ Created log directory: {log_path}")
      
      # Create log file
      log_file = log_path / f"service_{datetime.now().strftime('%Y%m%d')}.log"
      
      # Write to file
      with open(log_file, 'w') as f:
          f.write(f"Log file created at {datetime.now()}\n")
      
      # List all log files
      log_files = list(log_path.glob('*.log'))
      print(f"Found {len(log_files)} log files in {log_path}")
      
      return log_file
  
  def find_config_files(search_path='/etc', extension='.conf'):
      """Find configuration files using pathlib"""
      config_files = []
      
      for path in Path(search_path).rglob(f'*{extension}'):
          if path.is_file():
              try:
                  with open(path, 'r') as f:
                      # Check if it's valid JSON/ YAML
                      content = f.read()
                      if content.strip().startswith('{') or content.strip().startswith('{'):
                          config_files.append(path)
              except:
                  pass
      
      print(f"Found {len(config_files)} config files in {search_path}")
      return config_files
  
  # Usage
  log_file = manage_log_directory('/tmp/test_logs')
  configs = find_config_files('/etc')
  ```

## DevOps Context
File operations are fundamental for DevOps automation:

- **Configuration management**: Read/write service configs
- **Log management**: Rotate, analyze, and process log files
- **Data export**: Generate reports and backup data
- **Path management**: Cross-platform path manipulation

### Log Rotation with Pathlib
```python
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def rotate_logs(log_dir='/var/log/app', max_size_mb=100, keep_days=7):
    """Rotate log files based on size and age"""
    log_path = Path(log_dir)
    
    # Create backup directory
    backup_dir = log_path / 'backup'
    backup_dir.mkdir(exist_ok=True)
    
    current_time = datetime.now()
    
    # Process each log file
    for log_file in log_path.glob('*.log'):
        if log_file.name.startswith('.'):
            continue
        
        # Check file size
        file_size_mb = log_file.stat().st_size / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            # Rotate based on size
            timestamp = current_time.strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f"{log_file.stem}_{timestamp}{log_file.suffix}"
            
            shutil.move(str(log_file), str(backup_file))
            print(f"✓ Rotated {log_file.name} to {backup_file.name}")
        
        # Check age for cleanup
        file_age = current_time - datetime.fromtimestamp(log_file.stat().st_mtime)
        
        if file_age.days > keep_days and 'backup' not in log_file.name:
            log_file.unlink()
            print(f"✓ Deleted old log: {log_file.name}")

def create_log_archive(log_dir='/var/log/app/archive'):
    """Create compressed archive of old logs"""
    log_path = Path(log_dir)
    archive_file = log_path.parent / f"app_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    
    # Create list of files to archive (older than 30 days)
    files_to_archive = []
    cutoff_date = datetime.now() - timedelta(days=30)
    
    for log_file in log_path.glob('*.log'):
        if log_file.name.startswith('.'):
            continue
        
        file_date = datetime.fromtimestamp(log_file.stat().st_mtime)
        if file_date < cutoff_date:
            files_to_archive.append(log_file)
    
    if files_to_archive:
        # Create tar.gz archive
        with tarfile.open(archive_file, 'w:gz') as tar:
            for file in files_to_archive:
                tar.add(file, arcname=file.name)
        
        print(f"✓ Created archive: {archive_file} with {len(files_to_archive)} files")
        
        # Remove archived files
        for file in files_to_archive:
            file.unlink()
        
        return archive_file
    
    return None

# Usage
rotate_logs('/tmp/test_logs', max_size_mb=10, keep_days=3)
archive = create_log_archive('/tmp/test_logs/archive')
if archive:
    print(f"Log archive created: {archive}")
```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day13 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day13 -v` — see `tests/day13/test_day13.py`