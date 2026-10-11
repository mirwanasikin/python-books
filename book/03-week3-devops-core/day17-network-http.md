# Day 17 — Network & HTTP

Keywords: `import`, `from`, `as`, `try`, `except`, `with`

## Why This Matters for DevOps

Every automation script touches the network: ping a host, download a script, hit an API, check a service’s health, stream logs, or invoke a web hook. Knowing the core network APIs—`socket`, `urllib`, and the third‑party standard `requests`—lets you replace shell commands like `curl`, `wget`, or `netcat` with robust, retry‑ready Python code.

## Keywords + Methods

### `socket` (Raw Network Sockets)
- **Type:** Low‑level networking primitives
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `socket.socket(family, type)` | `s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` |
  | `s.connect((host, port))` | `s.connect(("127.0.0.1", 80))` |
  | `s.settimeout(sec)` | `s.settimeout(2.0)` |
  | `s.close()` | `s.close()` |

- **Example:**
  ```python
  import socket

  def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
      """Check if TCP port is open (tcp health check)."""
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          s.settimeout(timeout)
          try:
              s.connect((host, port))
              return True
          except (socket.timeout, socket.error):
              return False

  print(f"Port 22 on localhost open? {check_port('127.0.0.1', 22)}")
  ```

### `urllib.request` (Stdlib HTTP)
- **Type:** URL fetching without third‑party dependencies
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `urllib.request.urlopen(url, timeout)` | `resp = urllib.request.urlopen("https://example.com")` |
  | `resp.status` | `200`, `404`, `500` |
  | `resp.read()` | `html_bytes = resp.read()` |
  | `urllib.request.urlretrieve(url, filename)` | `urllib.request.urlretrieve(url, "/tmp/file.tar.gz")` |

- **Example:**
  ```python
  import urllib.request
  import urllib.error

  url = "https://httpbin.org/status/200"
  try:
      with urllib.request.urlopen(url, timeout=5) as resp:
          print(f"Status: {resp.status}")
          print(f"Headers: {resp.headers.get('Content-Type')}")
          body = resp.read().decode("utf-8")
          print(f"Body length: {len(body)}")
  except urllib.error.HTTPError as e:
      print(f"HTTP error: {e.code}")
  except urllib.error.URLError as e:
      print(f"Network error: {e.reason}")
  ```

### `requests` (The Third‑Party Standard)
- **Type:** Human‑friendly HTTP library
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `requests.get(url, params, headers, timeout)` | `r = requests.get("https://api.github.com/users/octocat")` |
  | `requests.post(url, json, data, headers)` | `r = requests.post("https://...", json={"key": "val"})` |
  | `r.status_code` / `r.ok` | `if r.ok: ...` (`ok` means < 400) |
  | `r.json()` | `data = r.json()` |
  | `r.text` / `r.content` | `text = r.text` |
  | `r.raise_for_status()` | Raises `HTTPError` if >= 400 |

- **Example:**
  ```python
  import requests

  try:
      resp = requests.get(
          "https://httpbin.org/json",
          headers={"User-Agent": "DevOpsBot/1.0"},
          timeout=5
      )
      resp.raise_for_status() # raises on 4xx/5xx
      
      data = resp.json()
      print("JSON keys:", list(data.keys()))
  except requests.exceptions.Timeout:
      print("Request timed out")
  except requests.exceptions.HTTPError as e:
      print(f"HTTP error: {e.response.status_code}")
  except requests.exceptions.ConnectionError:
      print("Failed to connect to host")
  ```

### `http.client` (Low‑Level HTTP)
- **Type:** Low‑level HTTP protocol client
- **Methods:** `HTTPConnection(host, port)`, `.request(method, path)`, `.getresponse()`
- **Example:**
  ```python
  import http.client

  conn = http.client.HTTPConnection("httpbin.org", timeout=5)
  try:
      conn.request("GET", "/get")
      resp = conn.getresponse()
      print(f"Status: {resp.status}, Reason: {resp.reason}")
      data = resp.read().decode()
      print(data[:100])
  finally:
      conn.close()
  ```

## DevOps Context: Health Checker Script

```python
import requests
import sys
import time

def check_endpoint(url: str, expected_status: int = 200, timeout: int = 5) -> bool:
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == expected_status:
            print(f"[PASS] {url} -> {r.status_code} ({r.elapsed.total_seconds():.3f}s)")
            return True
        else:
            print(f"[FAIL] {url} -> Expected {expected_status}, got {r.status_code}")
            return False
    except requests.RequestException as e:
        print(f"[ERROR] {url} -> {e}")
        return False

if __name__ == "__main__":
    urls = sys.argv[1:] if len(sys.argv) > 1 else ["https://httpbin.org/status/200"]
    all_ok = all(check_endpoint(u) for u in urls)
    sys.exit(0 if all_ok else 1)
```

## Exercises

1. Write `port_scanner.py`: takes a hostname and a list of ports (e.g. 22, 80, 443, 3306), uses `socket` to check each, and prints open/closed status.
2. Write `downloader.py`: downloads a file from URL using `requests` with chunked streaming (`stream=True`), writes to disk with progress indicator (MB downloaded).
3. Write `api_ping.py`: sends a POST request with JSON payload to `https://httpbin.org/post`, validates response status and returned JSON.
4. Compare `urllib` vs `requests`: write a small script fetching the same URL with both, measure lines of code and exception handling complexity.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day17 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day17 -v` — see `tests/day17/test_day17.py`
