# Day 19 — Testing & Typing

Keywords: `import`, `from`, `as`, `def`, `return`, `if`, `elif`, `else`, `try`, `except`, `with`, `None`, `List`, `Dict`, `Optional`, `Union`

## Why This Matters for DevOps

Automations are critical infrastructure. Formal tests ensure they never silently fail. Python’s `typing` module encodes contracts and enables static analysis (mypy), reducing runtime bugs. For DevOps scripts, typing clarifies expectations for inputs, config schemas, and return types, making them more maintainable and self-documenting.

## Keywords + Methods

### `pytest` (Test Harness)
- **Type:** Test runner and assertion library
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `def test_name(): ...` | Basic test function |
  | `import pytest` | Skip/warning decorators |
  | `pytest.raises(exc)` | Context manager for exception testing |
  | `monkeypatch.setattr(obj, name, value)` | Mock attribute in tests |

- **Example:**
  ```python
  import pytest

  def test_addition():
      assert 2 + 2 == 4

  def test_division_by_zero():
      with pytest.raises(ZeroDivisionError):
          _ = 1 / 0

  # Use monkeypatch for mocking
  def test_mock_os_path(monkeypatch):
      monkeypatch.setattr("os.path.exists", lambda _: True)
      assert os.path.exists("/any")
  ```

### `unittest` (Legacy Support + Mocking)
- **Type:** Built-in test framework
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `unittest.TestCase` | Base class |
  | `self.assertEqual(a, b)` | Assertion methods |
  | `setUp()` / `tearDown()` | Per-test setup/cleanup |

- **Example:**
  ```python
  import unittest

  class TestCalculator(unittest.TestCase):
      def test_add(self):
          self.assertEqual(1 + 1, 2)

      def setUp(self):
          self.x = 5

      def tearDown(self):
          pass
  ```

### `unittest.mock` (Mocking)
- **Type:** Replace parts of modules with dummy objects
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `mock.patch("module.object")` | Context manager or decorator |
  | `MagicMock()` | Generic mock object |
  | `Mock(return_value=...)` | Mock with return value |

- **Example:**
  ```python
  from unittest.mock import patch, MagicMock, Mock

  # Method 1: patch in with-statement
  with patch("requests.get") as mock_get:
      mock_get.return_value.status_code = 200
      mock_get.return_value.json.return_value = {"ok": True}
      resp = requests.get("https://api.example.com")
      mock_get.assert_called_once_with("https://api.example.com", timeout=5)

  # Method 2: decorator
  @patch("os.path.exists")
  def test_exists_true(mock_exists):
      mock_exists.return_value = True
      assert os.path.exists("/fake")

  # Method 3: Mock instance attribute
  mock_socket = Mock()
  mock_socket.create_connection.return_value.__enter__.return_value = None
  with patch("socket.create_connection", return_value=mock_socket):
      check_tcp({"host": "localhost", "port": 22})
  ```

### `typing` (Type Annotations)
- **Type:** Type hints for variables, function signatures, containers
- **Methods:** Generic aliases in Python 3.9+ (`list`, `dict`)
- **Key constructs:**

  | Syntax | Meaning |
  |--------|---------|
  | `None` | singleton None |
  | `bool` / `int` / `float` | Primitive types |
  | `List[T]` / `list[T]` | Homogenous list (typing import) |
  | `Dict[K, V]` / `dict[K, V]` | Homogenous dict |
  | `Optional[T]` / `T | None` | May be None |
  | `Union[A, B]` / `A | B` | Either A or B |
  | `Any` | Any type |

- **Example:**
  ```python
  from typing import List, Dict, Optional, Union

  def process(
      services: List[Dict[str, str]],
      timeout: Optional[float] = None,
  ) -> Dict[str, Union[int, str]]:
      """Process list of service dicts.
      Returns mapping of service->status.
      """
      result: Dict[str, Union[int, str]] = {}
      for svc in services:
          status = check_one(svc, timeout)
          result[svc["name"]] = 0 if status == "up" else 1
      return result
  ```

### `assert` Keyword
- **Type:** Runtime assertion statement
- **Methods:** `assert condition, message`
- **Example:**
  ```python
  # Basic assertions
  assert result.returncode == 0, f"Command failed with {result.stderr}"

  # Multi-line with variables
  def test_file_exists():
      path = Path("/etc/nginx/nginx.conf")
      assert path.is_file(), f"Expected {path} to exist"

  # Use in loops
  for svc in services:
      assert svc["name"], f"Missing name in {svc}"
  ```

### `match` (Pattern Matching, Python 3.10+)
- **Type:** Structural pattern matching; can match data from `json`, `yaml`
- **Methods:** `match value: case pattern:`
- **Example:**
  ```python
  from dataclasses import dataclass

  @dataclass
  class Service:
      name: str
      typ: str  # "http" | "tcp"

  def run_check(service: Service) -> str:
      match service.typ:
          case "http":
              return "http_check"
          case "tcp":
              return "tcp_check"
          case _:
              raise ValueError(f"Unsupported type: {service.typ}")
  ```

### `type` (Type Checking, PEP 484)
- **Type:** Overloading function signatures, typing decorators
- **Methods:** `isinstance(obj, type)`
- **Example:**
  ```python
  def parse_config(text: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
      try:
          return json.loads(text)
      except json.JSONDecodeError:
          # Fallback to YAML
          return yaml.safe_load(text)

  # Guard against runtime type errors
  def safe_get(config: Dict[str, Any], key: str, default: Any = None) -> Any:
      if isinstance(config, dict):
          return config.get(key, default)
      return default
  ```

## DevOps Context: Testing Your Automation

```python
import pytest
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# helper utilities
def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_command_exists():
    # find command on PATH
    path = shutil.which("systemctl")
    assert path is not None, "systemctl not found on PATH"

# Test health_checker.py
import health_checker

def test_load_config(tmp_path):
    config = {"services": [{"name": "web", "type": "http", "host": "localhost"}]}
    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text(yaml.dump(config))
    services = health_checker.load_config(str(yaml_file))
    assert services[0]["name"] == "web"

def test_http_check(monkeypatch):
    mock_resp = MagicMock(status_code=200, elapsed=MagicMock(total_seconds=lambda: 0.123))
    monkeypatch.setattr(health_checker.requests, "get", return_value=mock_resp)
    result = health_checker.check_http({"name": "test", "host": "example.com", "port": 80})
    assert result["status"] == "up"
    assert result["status_code"] == 200
    assert result["latency_ms"] is not None

def test_tcp_check(monkeypatch):
    mock_conn = MagicMock()
    monkeypatch.setattr(health_checker.socket, "create_connection", return_value=mock_conn)
    result = health_checker.check_tcp({"name": "test", "host": "localhost", "port": 22})
    assert result["status"] == "up"
    mock_conn.close.assert_called_once()

def test_exit_codes(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["health_checker.py", "--services", "missing.yaml"])
    with pytest.raises(SystemExit) as exc:
        health_checker.main()
    assert exc.value.code == 2

if __name__ == "__main__":
    pytest.main(["-v"])
```

## Exercises

1. Write `test_ports.py`: uses `pytest` and `monkeypatch` to mock `socket.create_connection` and verify it is called with correct host/port.
2. Write `test_yaml_configs.py`: creates several temp YAML configs, runs `health_checker.load_config`, asserts parsed data shape.
3. Write `test_report_schema.py`: validates the JSON report against a strict schema (use `jsonschema` if available, else manual field check).
4. Write `test_assert_patterns.py`: uses `assert` statements and custom helper assertions (e.g., `assert_all_up()`).

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day19 -v`
- [ ] Write tests for automation scripts

## Test
Run: `pytest tests/day19 -v` — see `tests/day19/test_day19.py`
