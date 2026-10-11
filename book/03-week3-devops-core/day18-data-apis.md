# Day 18 — Data & APIs

Keywords: `import`, `from`, `as`, `try`, `except`, `with`, `None`, `if`, `elif`, `else`

## Why This Matters for DevOps

Your automation scripts ingest and emit data: config files (JSON/YAML), reports (CSV), REST API responses. Being able to decode `application/json`, `text/csv`, and parse query parameters is essential for real-world tooling. Fast, correct serialization/deserialization eliminates edge-case bugs in CI/CD pipelines.

## Keywords + Methods

### `json` (JSON Encoding/Decoding)
- **Type:** Standard interchange format
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `json.dump(obj, fp, **kw)` | Write to file |
  | `json.dumps(obj, **kw)` | Serialize to str |
  | `json.load(fp, **kw)` | Load from file |
  | `json.loads(s, **kw)` | Parse from str |
  | `default=callable` | Custom encoder |

- **Example:**
  ```python
  import json
  from datetime import datetime

  data = {
      "service": "nginx",
      "port": 80,
      "checks": [{"success": True, "latency_ms": 12}],
      "deployed_at": datetime.now().isoformat()
  }

  # pretty JSON for config
  json_str = json.dumps(data, indent=2, default=str)
  print(json_str)

  # round-trip preserve types
  parsed = json.loads(json_str)
  print(parsed["service"], parsed["port"])
  ```

### `csv` (CSV Encoding/Decoding)
- **Type:** Comma-separated values
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `csv.reader(f)` | Iter rows as lists |
  | `csv.DictReader(f)` | Iter rows as dicts |
  | `csv.writer(f)` | Write rows |
  | `csv.DictWriter(f)` | Write headers |

- **Example:**
  ```python
  import csv
  import os

  rows = [{"host": "web1", "ip": "10.0.0.1", "ports": "22,80,443"},
          {"host": "db1", "ip": "10.0.0.2", "ports": "3306"}]

  with open("/tmp/hosts.csv", "w", newline="") as f:
      fieldnames = ["host", "ip", "ports"]
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(rows)

  with open("/tmp/hosts.csv", newline="") as f:
      reader = csv.DictReader(f)
      for row in reader:
          print(f"{row['host']} ({row['ip']}) ports: {row['ports']}")
  ```

### `yaml` (YAML Parsing)
- **Type:** Rich config format; stdlib `yaml` (PyYAML) if available
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `yaml.safe_load(s)` | Load dict/list, ignore custom tags |
  | `yaml.safe_dump(obj, **kw)` | Dump to str, default types |

- **Example:**
  ```python
  import yaml
  from pathlib import Path

  config = {
      "services": ["nginx", "redis"],
      "ports": {"nginx": 80, "redis": 6379},
      "ssl": False
  }

  # Write YAML
  yaml_str = yaml.safe_dump(config, default_flow_style=False)
  Path("/tmp/config.yaml").write_text(yaml_str)

  # Read YAML
  loaded = yaml.safe_load(Path("/tmp/config.yaml").read_text())
  print(f"Ports: {loaded['ports']['nginx']}")
  ```

### `requests` (API Responses)
- **Type:** JSON, form data, multipart upload, file downloads
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `r.json()` | Deserializes to Python object |
  | `r.text` / `r.content` | Raw string/bytes |
  | `r.headers` | Dict-like of response headers |
  | `r.cookies` | RequestsCookieJar |

- **Example:**
  ```python
  import requests

  # GET query params, decode JSON response
  r = requests.get(
      "https://httpbin.org/get",
      params={"service": "health", "port": 80},
      timeout=5
  )
  r.raise_for_status()
  data = r.json()

  print(f"Origin IP: {data['origin']}")
  print(f"URL params: {data['url']}")

  # POST with form + file
  files = {"config": ("deploy.yaml", Path("/etc/nginx/nginx.conf").read_bytes())}
  data = {"service": "restart", "dry-run": "true"}
  r = requests.post("https://api.example.com/deploy", data=data, files=files)
  r.raise_for_status()
  print("Deployment queued")
  ```

### `urllib.parse` (URL Handling)
- **Type:** Parse, quote, unquote URLs
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `urlparse(url)` | `ParseResult` (scheme, netloc, path, ...)` |
  | `urlunparse(t)` | Rebuild URL |
  | `parse_qs(qs)` | `dict[str, list[str]]` |
  | `urlencode(params)` | `key=val&foo=bar` |

- **Example:**
  ```python
  from urllib.parse import urlparse, urlencode, parse_qs

  url = "https://api.github.com/repos/octocat/hello-world/issues?state=closed&page=2"
  parsed = urlparse(url)
  print(f"Host: {parsed.netloc}")

  params = {"state": "open", "per_page": 100, "page": 1}
  encoded = urlencode(params)
  api_url = f"https://api.github.com/repos/octocat/hello-world/issues?{encoded}"

  # Query string in GET
  from urllib.parse import parse_qs
  qs = "deploy=prod&region=us-west-2"
  print(parse_qs(qs))
  ```

## DevOps Context: Configuration Loader

```python
import yaml
import json
import csv
from pathlib import Path
from typing import Dict, Any
import argparse
import logging

def load_config(path: str) -> Dict[str, Any]:
    path = Path(path)
    if path.suffix == ".yaml" or path.suffix == ".yml":
        return yaml.safe_load(path.read_text())
    elif path.suffix == ".json":
        return json.loads(path.read_text())
    elif path.suffix == ".csv":
        with path.open() as f:
            return list(csv.DictReader(f))
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file (JSON/YAML/CSV)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    try:
        cfg = load_config(args.config)
        logging.info(f"Loaded config with keys: {list(cfg.keys()) if isinstance(cfg, dict) else len(cfg)} entries")
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        raise SystemExit(2)
```

## Exercises

1. Build `process_reports.py`: reads `reports.csv`, adds new server rows, writes back to `reports_new.csv`.
2. Build `merge_configs.py`: merges JSON config files found with `glob`, outputs YAML to a target.
3. Build `cloud_ping.py`: takes a list of URLs, fetches them with `requests`, collects status codes, writes a `ping.json` report.
4. Build `url_expander.py`: given a list of relative paths, transforms them to full URLs and prints resolved full URLs.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day18 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day18 -v` — see `tests/day18/test_day18.py`
