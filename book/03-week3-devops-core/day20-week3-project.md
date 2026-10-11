# Day 20 — Week 3 Project: Build `health_checker.py`

Keywords: `import`, `from`, `as`, `if`, `elif`, `else`, `try`, `except`, `with`, `None`, `for`, `in`, `def`, `return`, `raise`, `SystemExit`, `argparse`, `json`, `yaml`, `logging`, `subprocess`, `requests`

## Why This Project

A health-checker is the most fundamental DevOps tool: It pings HTTP/HTTPS endpoints, runs TCP port checks, captures process status via `subprocess`, aggregates results into a machine-readable report, and exits with a non-zero code if any service is down. Build it once, and you can reuse it across environments, CI pipelines, or orchestrate entire service-mesh topologies.

## Project: `health_checker.py`

### Spec

A Python CLI tool that:

1. **CLI Arguments**
   - `--services` (required): Path to a YAML config file with:
     ```yaml
     services:
       - name: "nginx"
         type: "http" | "tcp"
         host: "localhost"
         port: 80
         path: "/health"           # http only, optional (default "/")
         timeout: 5              # seconds
       - name: "redis"
         type: "tcp"
         host: "127.0.0.1"
         port: 6379
         timeout: 3
     ```
   - `--report` (optional): Output path for JSON report (default: `health_report.json`)
   - `--verbose` (-v): Enable debug logging (repeat for more verbose)

2. **Checks**
   - **HTTP / HTTPS**: Use `requests` with `timeout`, validate status in `[200, 300)`, and optional response time.
   - **TCP**: Use `socket.create_connection`, `timeout` is immediate, no HTTP handshake.
   - Capture all outputs: `stdout`, `stderr`, `returncode` for subprocess.

3. **Results**
   - JSON report containing:
     ```json
     {
       "timestamp": "2024-10-11T12:34:56Z",
       "host": "example-host",
       "total_services": 3,
       "failed_services": 1,
       "successful_services": 2,
       "checks": [
         {
           "name": "nginx",
           "type": "http",
           "host": "localhost",
           "port": 80,
           "path": "/health",
           "timeout": 5,
           "status": "up", "down", or "error"
           "status_code": 200,
           "latency_ms": 123.4,
           "error": "Timeout"
         },
         {
           "name": "redis",
           "type": "tcp",
           "host": "127.0.0.1",
           "port": 6379,
           "status": "up" or "down"
           "error": "Connection refused"
         }
       ]
     }
     ```

4. **Exit Codes**
   - `0`: All services reported `up`
   - `1`: One or more services `down` (non-zero failure count)
   - `2`: Config file not found or invalid
   - `3`: Any internal error (e.g., missing imports)

5. **Logging**
   - Debug level: each check start/end, raw exception message
   - Info level: service status, final summary (total, failed, successful)
   - Error level: fatal config errors, unexpected exceptions
   - Output to `stdout` for human readability
   - Also write log entries to a file named `health_checker.log` (append)

6. **Starter Code**

```python
#!/usr/bin/env python3
"""health_checker.py – multi-service health monitor.
Usage: health_checker.py --services CONFIG_YAML [--report REPORT.json] [-v]
"""

import argparse
import json
import logging
import socket
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import requests
import yaml

def load_config(path: str) -> List[Dict[str, Any]]:
    """Load service definitions from YAML config.
    Raises SystemExit on file not found or YAML parse error.
    """
    if not Path(path).exists():
        print(f"ERROR: Config file not found: {path}")
        sys.exit(2)
    try:
        return yaml.safe_load(Path(path).read_text()).get("services", [])
    except Exception as e:
        print(f"ERROR: Failed to parse config: {e}")
        sys.exit(2)

def check_http(service: Dict[str, Any]) -> Dict[str, Any]:
    """Check HTTP/HTTPS service.
    Returns dict with check results.
    """
    name = service["name"]
    host = service["host"]
    port = service.get("port", 80)
    path = service.get("path", "/")
    timeout = service.get("timeout", 5)
    url = f"http{'s' if port == 443 else ''}://{host}:{port}{path}"

    result = {
        "name": name,
        "type": "http",
        "host": host,
        "port": port,
        "path": path,
        "timeout": timeout,
        "status": "down",
        "status_code": None,
        "latency_ms": None,
        "error": None
    }

    try:
        start = time.perf_counter()
        response = requests.get(url, timeout=timeout)
        elapsed = (time.perf_counter() - start) * 1000

        if 200 <= response.status_code < 300:
            result.update({
                "status": "up",
                "status_code": response.status_code,
                "latency_ms": round(elapsed, 2)
            })
        else:
            result["error"] = f"Status {response.status_code}"
    except Exception as e:
        result["error"] = str(e)

    return result

def check_tcp(service: Dict[str, Any]) -> Dict[str, Any]:
    """Check TCP service.
    Returns dict with check results.
    """
    name = service["name"]
    host = service["host"]
    port = service["port"]
    timeout = service.get("timeout", 5)

    result = {
        "name": name,
        "type": "tcp",
        "host": host,
        "port": port,
        "timeout": timeout,
        "status": "down",
        "error": None
    }

    try:
        with socket.create_connection((host, port), timeout=timeout):
            result["status"] = "up"
    except Exception as e:
        result["error"] = str(e)

    return result

def run_checks(services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Run checks for all services.
    """
    results = []
    for svc in services:
        logging.debug(f"Checking {svc['name']} ({svc['type']})...", extra={"service": svc["name"]})
        if svc["type"] == "http":
            results.append(check_http(svc))
        elif svc["type"] == "tcp":
            results.append(check_tcp(svc))
        else:
            logging.error(f"Unsupported service type: {svc['type']}")
            results.append({
                "name": svc["name"],
                "type": svc["type"],
                "status": "error",
                "error": f"Unsupported type: {svc['type']}"
            })
        logging.info(f"{svc['name']}: {results[-1]['status']}", extra={"service": svc["name"]})

    return results

def generate_report(host: str, checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary report.
    """
    successful = sum(1 for c in checks if c.get("status") == "up")
    failed = sum(1 for c in checks if c.get("status") == "down")

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "host": host,
        "total_services": len(checks),
        "successful_services": successful,
        "failed_services": failed,
        "checks": checks
    }

def write_report(report: Dict[str, Any], path: str) -> None:
    """Write JSON report to file.
    """
    Path(path).write_text(json.dumps(report, indent=2))

def setup_logging(verbose: int) -> None:
    level = logging.DEBUG if verbose >= 2 else logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("health_checker.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    parser = argparse.ArgumentParser(description="Multi-service health monitor")
    parser.add_argument("--services", required=True, help="Path to YAML services config")
    parser.add_argument("--report", default="health_report.json", help="Output JSON report path")
    parser.add_argument("-v", "--verbose", action="count", default=0)

    args = parser.parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    services = load_config(args.services)
    checks = run_checks(services)
    report = generate_report(socket.gethostname(), checks)
    write_report(report, args.report)

    # Human readable summary
    print(f"\nHealth check complete. Host: {socket.gethostname()}")
    print(f"Total: {report['total_services']}, Up: {report['successful_services']}, Down: {report['failed_services']}")

    if report["failed_services"] > 0:
        for c in report["checks"]:
            if c["status"] == "down":
                print(f"- {c['name']} ({c['type']}): {c.get('error', 'Unknown')}")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### Success Criteria

- ✅ Load services from valid YAML config.
- ✅ Execute HTTP checks using `requests` with timeout handling.
- ✅ Execute TCP port checks using `socket`.
- ✅ Produce JSON report matching the spec.
- ✅ Exit with `0` on all-up, `1` on any-down.
- ✅ Exit with `2` on config errors (file not found, parse error).
- ✅ Exit with `3` on unhandled exceptions (e.g., import error).
- ✅ Structured logging to both console and `health_checker.log`.
- ✅ Report includes timestamp, host, total/ success/ failure counts.
- ✅ Each check includes appropriate fields: status, error, status_code, latency.

### Unit Test Skeleton (copy into `tests/day20/test_day20.py`)

```python
import pytest
from pathlib import Path
import tempfile
import yaml
import json

def test_http_check(monkeypatch):
    import health_checker
    from health_checker import check_http

    # Mock requests.get
    mock_resp = pytest.Mock(status_code=200, elapsed=pytest.Mock(total_seconds=lambda: 0.123))
    monkeypatch.setattr(health_checker.requests, "get", lambda *a, **k: mock_resp)

    service = {"name": "test", "type": "http", "host": "example.com", "port": 80, "path": "/"}
    result = check_http(service)
    assert result["status"] == "up"
    assert result["status_code"] == 200
    assert result["latency_ms"] is not None

def test_tcp_check(monkeypatch):
    import health_checker
    from health_checker import check_tcp

    # Mock socket.create_connection to succeed
    mock_conn = pytest.Mock()
    monkeypatch.setattr(health_checker.socket, "create_connection", lambda *a, **k: mock_conn)

    service = {"name": "test", "type": "tcp", "host": "localhost", "port": 6379}
    result = check_tcp(service)
    assert result["status"] == "up"
    mock_conn.close.assert_called_once()

def test_yaml_config(tmp_path):
    config = {"services": [
        {"name": "web", "type": "http", "host": "localhost", "port": 80, "path": "/health"}
    ]}
    config_path = tmp_path / "services.yaml"
    config_path.write_text(yaml.dump(config))
    from health_checker import load_config
    services = load_config(str(config_path))
    assert services[0]["name"] == "web"

def test_report_generation():
    from health_checker import generate_report
    checks = [{"name": "s1", "status": "up"}, {"name": "s2", "status": "down"}]
    report = generate_report("hostX", checks)
    assert report["total_services"] == 2
    assert report["successful_services"] == 1
    assert report["failed_services"] == 1
    assert report["checks"] == checks

def test_exit_codes(monkeypatch):
    import health_checker
    from health_checker import main

    monkeypatch.setattr(sys, "argv", ["health_checker.py", "--services", "missing.yaml"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 2
```

### Running Tests

```bash
pytest tests/day20 -v
```

### Extension Opportunities

- Add `--subprocess` check to monitor running processes (e.g., `pgrep nginx`).
- Implement `--threshold` per-service latency alert.
- Use `multiprocessing` to run checks in parallel.

## Exercises

1. Copy the starter code into `health_checker.py`.
2. Run `pytest tests/day20 -v` to see failing tests; fix until all pass.
3. Create a sample YAML config `services.yaml` in the project root and run `./health_checker.py --services services.yaml --verbose`.
4. Add a new service type (e.g., `dns`) that performs a DNS lookup via `socket.gethostbyname`.
5. Validate the JSON report schema against a simple JSON schema validator.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day20 -v`
- [ ] Build health_checker.py for Linux

## Test
Run: `pytest tests/day20 -v` — see `tests/day20/test_day20.py`
