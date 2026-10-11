# Appendix C — DevOps Recipes

Common Python snippets for DevOps tasks.

## 1. Safe Command Runner
```python
import subprocess
def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
```

## 2. Environment Variable Loader
```python
import os
def get_config(key, default=None, required=False):
    val = os.environ.get(key, default)
    if required and val is None:
        raise EnvironmentError(f"Missing required env var: {key}")
    return val
```

## 3. Fast JSON File Loader
```python
import json
def load_json(path):
    with open(path) as f:
        return json.load(f)
```

## 4. IP Validator
```python
import ipaddress
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
```

## 5. Port Scanner (Simple)
```python
import socket
def is_port_open(ip, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return s.connect_ex((ip, port)) == 0
```
