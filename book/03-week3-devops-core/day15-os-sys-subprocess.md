# Day 15 — os, sys, subprocess

Keywords: `as` (reuse), `import`, `from`

## Why This Matters for DevOps

Every automation script touches the OS: read env vars, parse CLI args, run shell commands, capture output, exit with correct codes. `os` + `sys` + `subprocess` form the core trio. Master these and you can replace most bash scripts with Python.

## Keywords + Methods

### `import` / `as` (reuse)
- **Type:** Module aliasing
- **Methods:** `import subprocess as sp`, `from os import environ as env`
- **Example:**
  ```python
  import subprocess as sp
  import os.path as osp
  from sys import argv as args, exit as die

  print(args[0])
  print(osp.join("/var", "log", "app.log"))
  ```

### `os.environ`
- **Type:** `os._Environ` (dict-like mapping of environment variables)
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `os.environ.get(key, default)` | `os.environ.get("HOME", "/root")` |
  | `os.environ[key]` | `os.environ["DEPLOY_ENV"]` |
  | `os.getenv(key, default)` | `os.getenv("LOG_LEVEL", "INFO")` |
  | `os.putenv(key, value)` | `os.putenv("STAGE", "prod")` |

- **Example:**
  ```python
  import os

  deploy_env = os.environ.get("DEPLOY_ENV", "dev")
  print(f"Deploying to: {deploy_env}")

  # Required variable pattern — fail fast
  try:
      api_token = os.environ["API_TOKEN"]
  except KeyError:
      print("API_TOKEN not set")
      raise SystemExit(1)

  # Set default for child processes
  os.environ.setdefault("LOG_LEVEL", "INFO")

  # Iterate safe subset
  for key in ("PATH", "HOME", "USER", "HOSTNAME"):
      print(f"{key}={os.getenv(key, '<unset>')}")
  ```

### `os.path` + `os.listdir` / `os.scandir`
- **Type:** Path manipulation + directory listing
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `os.path.join(a, *p)` | `os.path.join("/etc", "nginx")` |
  | `os.path.exists(path)` | `os.path.exists("/var/log/app.log")` |
  | `os.path.isfile(path)` | `os.path.isfile("/etc/hosts")` |
  | `os.path.isdir(path)` | `os.path.isdir("/opt/app")` |
  | `os.path.basename(p)` / `dirname(p)` | `os.path.basename("/a/b/c.log")` |
  | `os.listdir(path)` | `os.listdir("/var/log")` |
  | `os.scandir(path)` | `for e in os.scandir("/tmp"): print(e.name)` |
  | `os.makedirs(path, exist_ok=True)` | `os.makedirs("/opt/app/data", exist_ok=True)` |

- **Example:**
  ```python
  import os

  log_dir = "/var/log/myapp"
  os.makedirs(log_dir, exist_ok=True)

  # listdir: simple names
  for name in os.listdir(log_dir):
      full = os.path.join(log_dir, name)
      if os.path.isfile(full) and name.endswith(".log"):
          size = os.path.getsize(full)
          print(f"{name}: {size} bytes")

  # scandir: faster, gives stat without extra syscall
  with os.scandir(log_dir) as entries:
      for entry in entries:
          if entry.is_file() and entry.name.endswith(".log"):
              st = entry.stat()
              print(f"{entry.name} mtime={st.st_mtime}")
  ```

### `sys.argv`
- **Type:** `list[str]` — CLI arguments, `argv[0]` is script name
- **Methods:** List methods — `len(sys.argv)`, slicing `sys.argv[1:]`, unpacking
- **Example:**
  ```python
  import sys

  # usage: python deploy.py <env> <version>
  if len(sys.argv) != 3:
      print(f"Usage: {sys.argv[0]} <env> <version>")
      sys.exit(2)

  _, env, version = sys.argv
  print(f"Deploy {version} to {env}")

  # Flags without argparse
  verbose = "--verbose" in sys.argv[1:]
  dry_run = "--dry-run" in sys.argv[1:]
  if dry_run:
      print("DRY RUN — no changes applied")
  ```

### `sys.exit` / `sys.stdin` / `sys.stdout` / `sys.stderr`
- **Type:** Interpreter control + standard streams
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `sys.exit(code)` | `sys.exit(0)` success, `sys.exit(1)` failure |
  | `sys.stderr.write(msg)` | `sys.stderr.write("error: disk full\n")` |
  | `sys.stdin.read()` | `data = sys.stdin.read()` |
  | `sys.platform` | `"linux"`, `"darwin"`, `"win32"` |

- **Example:**
  ```python
  import sys

  if sys.platform != "linux":
      sys.stderr.write("Only Linux supported\n")
      sys.exit(1)

  # Pipe-friendly: echo "nginx" | python check.py
  if not sys.stdin.isatty():
      for line in sys.stdin:
          service = line.strip()
          if service:
              print(f"checking {service}...")
      sys.exit(0)
  ```

### `subprocess.run`
- **Type:** Run command, wait, return `CompletedProcess`
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `subprocess.run(args, check, capture_output, text, timeout, env, cwd)` | See below |
  | `result.returncode` | `0` means success |
  | `result.stdout` / `result.stderr` | Captured output with `capture_output=True` |

- **Example:**
  ```python
  import subprocess

  # Basic — list form preferred (no shell injection)
  result = subprocess.run(
      ["systemctl", "is-active", "nginx"],
      capture_output=True, text=True, timeout=10,
  )
  print(result.returncode, result.stdout.strip())

  # check=True raises on failure
  try:
      r = subprocess.run(
          ["df", "-h", "/"],
          check=True, capture_output=True, text=True, timeout=10,
      )
      print(r.stdout)
  except subprocess.CalledProcessError as e:
      print(f"df failed: rc={e.returncode}")
      print(e.stderr)

  # Custom env + working dir
  import os
  env = {**os.environ, "DEPLOY_ENV": "prod"}
  subprocess.run(["./deploy.sh"], cwd="/opt/app", env=env, check=True)

  # Timeout handling
  try:
      subprocess.run(["sleep", "30"], timeout=5, check=True)
  except subprocess.TimeoutExpired:
      print("Command timed out — killing")
  ```

### `subprocess.check_output` / `check_call`
- **Type:** Convenience wrappers around `run`
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `subprocess.check_output(args, text=True)` → str/bytes | `out = subprocess.check_output(["uptime"])` |
  | `subprocess.check_call(args)` → returncode | `subprocess.check_call(["true"])` |

- **Example:**
  ```python
  import subprocess

  # check_output: get stdout directly
  try:
      out = subprocess.check_output(
          ["git", "rev-parse", "--short", "HEAD"],
          text=True, timeout=10,
      )
      print(f"Commit: {out.strip()}")
  except subprocess.CalledProcessError:
      print("Not a git repo")

  # check_call: run for side effect, raise on failure
  subprocess.check_call(["mkdir", "-p", "/tmp/deploy-staging"])
  ```

### `subprocess.Popen` (streaming + pipelines)
- **Type:** Low-level process handle — non-blocking I/O, pipes
- **Methods:** `Popen(args, stdout=PIPE, stderr=PIPE, text=True)`, `.communicate()`, `.poll()`, `.wait()`, `.kill()`
- **Example:**
  ```python
  import subprocess

  # Stream output line-by-line (tail -f style)
  proc = subprocess.Popen(
      ["journalctl", "-f", "-n", "20", "-u", "nginx"],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
  )
  try:
      assert proc.stdout is not None
      for _ in range(5):
          line = proc.stdout.readline()
          if not line:
              break
          print(f"LOG: {line}", end="")
  finally:
      proc.kill()
      proc.wait(timeout=5)

  # Pipeline: dpkg -l | grep nginx (no shell=True)
  p1 = subprocess.Popen(["dpkg", "-l"], stdout=subprocess.PIPE, text=True)
  assert p1.stdout is not None
  p2 = subprocess.Popen(
      ["grep", "nginx"], stdin=p1.stdout,
      stdout=subprocess.PIPE, text=True,
  )
  p1.stdout.close()
  out, _ = p2.communicate(timeout=10)
  print(out)
  ```

## DevOps Context: Safe Command Runner

```python
import subprocess
import sys

def run(cmd: list[str], timeout: int = 30) -> str:
    """Run command, return stdout. Exit 1 with stderr on failure."""
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=True,
        )
        return r.stdout.strip()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"FAIL {' '.join(cmd)}: {e.stderr.strip()}\n")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        sys.stderr.write(f"TIMEOUT {' '.join(cmd)}\n")
        sys.exit(1)

if __name__ == "__main__":
    print(run(["systemctl", "is-active", sys.argv[1] if len(sys.argv) > 1 else "ssh"]))
```

Rules: list form over `shell=True`. Use `shell=True` only with static strings, never with user input. Always set `timeout`. Use `check=True` and handle `CalledProcessError`.

## Exercises

1. Write `env_check.py` — requires `DEPLOY_ENV` and `API_TOKEN`, prints masked token (`****` + last 4), exits 2 if missing.
2. Write `disk_alert.py` — runs `df -h /`, parses `%` usage, exits 1 if over threshold from `sys.argv`.
3. Write `tail_n.py` — uses `Popen` to stream first 10 lines of `journalctl -f`, then kills proc cleanly.
4. Convert a bash deploy script to Python using `run()` helper above with `cwd` and custom `env`.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day15 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day15 -v` — see `tests/day15/test_day15.py`
