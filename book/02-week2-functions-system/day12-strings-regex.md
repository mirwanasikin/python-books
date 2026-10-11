# Day 12 — Strings and Regular Expressions

Keywords: `split, join, replace, strip`

## Keywords + Methods

### String Splitting
- **Type:** Split string into list
- **Methods:** `str.split(sep=None, maxsplit=-1)` splits by whitespace or separator
- **Example:**
  ```python
  def parse_log_line(line):
      """Parse log line into components"""
      # Split by spaces, tabs, or multiple spaces
      parts = line.strip().split()
      
      if len(parts) >= 6:
          # Parse typical log format: TIMESTAMP LEVEL MESSAGE
          timestamp = parts[0] + ' ' + parts[1]
          level = parts[2]
          message = ' '.join(parts[3:])
          
          return {
              'timestamp': timestamp,
              'level': level,
              'message': message
          }
      
      return None
  
  # Usage in log analysis
  log_lines = [
      "2023-08-15 10:30:45 INFO Starting service",
      "2023-08-15 10:31:12 ERROR Failed to connect to database",
      "2023-08-15 10:32:45 WARN High memory usage detected"
  ]
  
  for line in log_lines:
      parsed = parse_log_line(line)
      if parsed:
          print(f"✓ {parsed['level']}: {parsed['message']}")
  
  # Split with custom separator
  config_line = "host:localhost;port:3306;user:root;password:secret"
  config_parts = config_line.split(';')
  config_dict = {}
  
  for part in config_parts:
      key, value = part.split(':')
      config_dict[key] = value
  
  print(config_dict)
  # Output: {'host': 'localhost', 'port': '3306', 'user': 'root', 'password': 'secret'}
  ```

### String Joining
- **Type:** Join list into string
- **Methods:** `sep.join(iterable)` joins elements with separator
- **Example:**
  ```python
  def create_path(*directories):
      """Create file path from directory components"""
      return '/'.join(directories)
  
  # DevOps: Create log file paths
  log_dir = '/var/log'
  services = ['nginx', 'apache', 'mysql']
  
  for service in services:
      log_file = create_path(log_dir, f"{service}.log")
      print(f"Log file: {log_file}")
  
  # Join service names for commands
  service_list = ['webserver', 'database', 'cache', 'queue']
  command = 'service '.join(service_list) + ' restart'
  print(f"Command: {command}")
  # Output: Command: webserver service database service cache service queue restart
  
  # Join IP addresses for firewall rules
  allowed_ips = ['192.168.1.0', '10.0.0.0', '172.16.0.0']
  cidr_ranges = [f"{ip}/24" for ip in allowed_ips]
  firewall_rule = ','.join(cidr_ranges)
  print(f"Firewall rule: {firewall_rule}")
  # Output: Firewall rule: 192.168.1.0/24,10.0.0.0/24,172.16.0.0/24
  ```

### String Replacement
- **Type:** Replace substrings
- **Methods:** `str.replace(old, new, count=-1)` replace occurrences
- **Example:**
  ```python
  def sanitize_log_message(message):
      """Remove sensitive information from log messages"""
      # Replace passwords
      message = message.replace('password=secret', 'password=***')
      message = message.replace('pwd=admin', 'pwd=***')
      
      # Replace API keys
      import re
      message = re.sub(r'api_key=[a-f0-9]{32}', 'api_key=***', message)
      
      # Replace IP addresses in dev environment
      message = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'xxx.xxx.xxx.xxx', message)
      
      return message
  
  # Usage in log processing
  sensitive_log = "[ERROR] Failed login for user admin from 192.168.1.100 with password=secret"
  sanitized = sanitize_log_message(sensitive_log)
  print(f"Original: {sensitive_log}")
  print(f"Sanitized: {sanitized}")
  # Output: Sanitized: [ERROR] Failed login for user admin from xxx.xxx.xxx.xxx with password=***
  
  # Fix service names in logs
  def normalize_service_name(service_log):
      replacements = {
          'web-server': 'webserver',
          'data-base': 'database',
          'mem-cache': 'cache',
          'message-queue': 'queue'
      }
      
      normalized = service_log
      for old, new in replacements.items():
          normalized = normalized.replace(old, new)
      
      return normalized
  
  log_entry = "[INFO] Restarting service web-server failed"
  fixed = normalize_service_name(log_entry)
  print(f"Fixed log: {fixed}")
  ```

### String Stripping
- **Type:** Remove leading/trailing characters
- **Methods:** `str.strip(chars=None)`, `lstrip(chars)`, `rstrip(chars)`
- **Example:**
  ```python
  def clean_service_name(name):
      """Clean service name by removing extra whitespace and hyphens"""
      # Strip whitespace
      cleaned = name.strip()
      
      # Strip hyphens
      cleaned = cleaned.strip('-_')
      
      # Convert to lowercase
      cleaned = cleaned.lower()
      
      return cleaned
  
  # Usage in service management
  raw_names = ['  nginx  ', '-apache-', '--mysql--', '  redis  ']
  
  for raw_name in raw_names:
      clean_name = clean_service_name(raw_name)
      print(f"'{raw_name}' -> '{clean_name}'")
  
  # Strip whitespace from log lines
  def parse_command_from_log(log_line):
      """Extract and clean command from log line"""
      # Find command between quotes
      start = log_line.find('"') + 1
      end = log_line.rfind('"')
      
      if start > 0 and end > start:
          command = log_line[start:end]
          # Remove extra whitespace
          return ' '.join(command.split())
      
      return None
  
  log_entry = '[COMMAND] Executed "  systemctl   restart   nginx  "'
  command = parse_command_from_log(log_entry)
  print(f"Extracted command: {command}")
  # Output: Extracted command: systemctl restart nginx
  ```

## Regular Expressions
- **Type:** Pattern matching in strings
- **Methods:** `re.match()`, `re.search()`, `re.findall()`, `re.sub()`, `re.compile()`
- **Example:**
  ```python
  import re
  
  def extract_ip_addresses(text):
      """Extract IP addresses from text using regex"""
      # Pattern for IPv4 addresses
      ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
      
      ips = re.findall(ip_pattern, text)
      return ips
  
  log_text = """
  [INFO] Server started on 192.168.1.100:8080
  [WARN] Connected to database at 10.0.0.5:3306
  [ERROR] Failed to connect to 172.16.0.10:5432
  [INFO] Backup completed to 192.168.1.100:9090
  """
  
  ips = extract_ip_addresses(log_text)
  print(f"Found IP addresses: {ips}")
  # Output: ['192.168.1.100', '10.0.0.5', '172.16.0.10', '192.168.1.100']
  
  def extract_log_components(line):
      """Extract log components using regex patterns"""
      patterns = {
          'timestamp': r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
          'level': r'\b(INFO|WARN|ERROR|DEBUG)\b',
          'message': r'(?<=ERROR|INFO|WARN|DEBUG).*'
      }
      
      components = {}
      for key, pattern in patterns.items():
          match = re.search(pattern, line)
          if match:
              components[key] = match.group()
      
      return components
  
  log_line = "2023-08-15 10:30:45 ERROR Failed to connect to database at 192.168.1.100:3306"
  components = extract_log_components(log_line)
  print(f"Log components: {components}")
  # Output: {'timestamp': '2023-08-15 10:30:45', 'level': 'ERROR', 'message': ' Failed to connect to database at 192.168.1.100:3306'}
  ```

## DevOps Context
Strings and regex are essential for log parsing, command construction, and data processing:

- **Log parsing**: Extract timestamps, levels, messages, and metadata
- **Configuration parsing**: Parse service configurations and command-line arguments
- **Data sanitization**: Remove sensitive information before logging
- **Pattern matching**: Match IPs, service names, and error patterns

### Log Processing with Regex
```python
import re
import json
from datetime import datetime

def parse_nginx_access_log(log_file):
    """Parse nginx access log and extract statistics"""
    # Common nginx log format: $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) '           # Remote IP
        r'- (?P<user>\S+) '                        # Remote user
        r'\[(?P<time>.+?)\] '                      # Time
        r'"(?P<request>.+?)" '                     # Request
        r'(?P<status>\d{3}) '                       # Status
        r'(?P<size>\d+) '                            # Body bytes sent
        r'"(?P<referer>.+?)" '                       # Referer
        r'"(?P<agent>.+?)"'                         # User agent
    )
    
    stats = {
        'status_counts': {},
        'ip_counts': {},
        'endpoint_counts': {},
        'user_agent_counts': {}
    }
    
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            match = log_pattern.match(line)
            if match:
                data = match.groupdict()
                
                # Parse request into method and endpoint
                request_parts = data['request'].split()
                if len(request_parts) >= 2:
                    method, endpoint = request_parts[0], request_parts[1]
                    stats['endpoint_counts'][endpoint] = stats['endpoint_counts'].get(endpoint, 0) + 1
                
                # Count status codes
                status = data['status']
                stats['status_counts'][status] = stats['status_counts'].get(status, 0) + 1
                
                # Count IPs
                ip = data['ip']
                stats['ip_counts'][ip] = stats['ip_counts'].get(ip, 0) + 1
                
                # Count user agents
                agent = data['agent']
                stats['user_agent_counts'][agent] = stats['user_agent_counts'].get(agent, 0) + 1
    
    return stats

def format_stats(stats):
    """Format statistics for human-readable output"""
    output = "Log Statistics:\n"
    output += "=" * 50 + "\n"
    
    output += "\nStatus Code Distribution:\n"
    for status, count in sorted(stats['status_counts'].items()):
        output += f"  {status}: {count}\n"
    
    output += "\nTop IP Addresses:\n"
    for ip, count in sorted(stats['ip_counts'].items(), key=lambda x: x[1], reverse=True)[:5]:
        output += f"  {ip}: {count}\n"
    
    output += "\nTop Endpoints:\n"
    for endpoint, count in sorted(stats['endpoint_counts'].items(), key=lambda x: x[1], reverse=True)[:5]:
        output += f"  {endpoint}: {count}\n"
    
    output += "\nUnique User Agents:\n"
    for agent, count in sorted(stats['user_agent_counts'].items(), key=lambda x: x[1], reverse=True)[:3]:
        # Truncate long user agents
        display_agent = agent[:100] + "..." if len(agent) > 100 else agent
        output += f"  {display_agent}: {count}\n"
    
    return output

# Create sample log for testing
sample_log = '''\n192.168.1.100 - - [15/Aug/2023:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"\n192.168.1.100 - - [15/Aug/2023:10:31:22 +0000] "POST /api/users HTTP/1.1" 201 5678 "https://example.com" "curl/7.68.0"\n192.168.1.101 - - [15/Aug/2023:10:32:10 +0000] "GET /api/products HTTP/1.1" 404 123 "-" "Mozilla/5.0"\n192.168.1.100 - - [15/Aug/2023:10:33:45 +0000] "GET /api/users HTTP/1.1" 200 4567 "-" "Python-urllib/3.10"\n192.168.1.102 - - [15/Aug/2023:10:34:12 +0000] "GET /api/orders HTTP/1.1" 500 8901 "-" "Apache-HttpClient/4.5"\n'''

# Write sample log and process it
with open('/tmp/sample_nginx.log', 'w') as f:
    f.write(sample_log)

stats = parse_nginx_access_log('/tmp/sample_nginx.log')
print(format_stats(stats))
```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day12 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day12 -v` — see `tests/day12/test_day12.py`