# Day 16 — Automation Toolkit

Keywords: `import`, `from`, `as`, `None`

## Why This Matters for DevOps

High-level file operations (`shutil`), pattern matching files (`glob`), safe temporary spaces (`tempfile`), CLI argument parsing (`argparse`), structured logging (`logging`), and timestamping (`datetime`). This day provides the professional-grade toolkit for building CLI tools that replace "one-liner" hacks.

## Keywords + Methods

### `shutil` (Shell Utilities)
- **Type:** High-level file/directory operations
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `shutil.copy(src, dst)` | `shutil.copy("config.yaml", "/etc/app/")` |
  | `shutil.copy2(src, dst)` | `shutil.copy2("p", "p2")` (copies metadata) |
  | `shutil.move(src, dst)` | `shutil.move("/tmp/pkg.tar.gz", "/var/lib/pkgs")` |
  | `shutil.rmtree(path, ignore_errors)` | `shutil.rmtree("/tmp/old_deploy")` |
  | `shutil.chown(path, user, group)` | `shutil.chown("/opt/app", "www-data")` |
  | `shutil.which(cmd)` | `shutil.which("git")` (returns full path) |
  | `shutil.disk_usage(path)` | `shutil.disk_usage("/")` → `(total, used, free)` |

- **Example:**
  ```python
  import shutil
  import os

  def backup_configs(src="/etc/nginx", dst="/var/backups/nginx"):
      if os.path.exists(dst):
          shutil.rmtree(dst)
      shutil.copytree(src, dst, symlinks=True)
      print(f"Backup complete to {dst}")

  usage = shutil.disk_usage("/")
  gb = 1024**3
  print(f"Disk: {usage.free // gb}GB free of {usage.total // gb}GB")
  ```

### `glob`
- **Type:** Unix-style pathname expansion
- **Methods:** `glob.glob(pattern, recursive=True)`, `glob.iglob(pattern)` (iterator)
- **Example:**
  ```python
  import glob
  import os

  # Find all log files recursively
  logs = glob.glob("/var/log/**/*.log", recursive=True)
  for log in logs:
      size = os.path.getsize(log)
      if size > 100 * 1024**2: # > 100MB
          print(f"Heavy log: {log} ({size // 1024**2}MB)")

  # Using glob patterns
  configs = glob.glob("/etc/nginx/sites-enabled/[0-9]*.conf")
  ```

### `tempfile`
- **Type:** Safe temporary file/dir generation
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `tempfile.TemporaryFile()` | `with tempfile.TemporaryFile() as f:` |
  | `tempfile.NamedTemporaryFile()` | `with tempfile.NamedTemporaryFile(delete=False) as f:` |
  | `tempfile.TemporaryDirectory()` | `with tempfile.TemporaryDirectory() as tmp_dir:` |
  | `tempfile.gettempdir()` | `os.path.join(tempfile.gettempdir(), "myapp")` |

- **Example:**
  ```python
  import tempfile
  import subprocess

  # Build package in temp dir, clean up automatically
  with tempfile.TemporaryDirectory(prefix="build-") as build_dir:
      print(f"Working in {build_dir}")
      # run build command in build_dir...
      # subprocess.run(["make"], cwd=build_dir)
  # build_dir is deleted here
  ```

### `argparse`
- **Type:** CLI argument parsing (Standard Library)
- **Methods:** `ArgumentParser()`, `add_argument()`, `parse_args()`
- **Example:**
  ```python
  import argparse
  import sys

  parser = argparse.ArgumentParser(description="Service Deployer")
  parser.add_argument("service", help="Service name to deploy")
  parser.add_argument("--env", choices=["dev", "prod"], default="dev")
  parser.add_argument("--version", required=True)
  parser.add_argument("--dry-run", action="store_true")
  parser.add_argument("-v", "--verbose", action="count", default=0)

  args = parser.parse_args()

  if args.dry_run:
      print(f"DRY RUN: deploying {args.service} v{args.version} to {args.env}")
  ```

### `logging`
- **Type:** Structured event logging
- **Methods:**

  | Level | Example |
  |-------|---------|
  | `logging.DEBUG` | `logging.debug("Detail...")` |
  | `logging.INFO` | `logging.info("Step X complete")` |
  | `logging.WARNING` | `logging.warning("Disk low")` |
  | `logging.ERROR` | `logging.error("Failed to connect")` |
  | `logging.CRITICAL` | `logging.critical("Security breach!")` |
  | `logging.basicConfig(...)` | Configure format, level, file/stream |

- **Example:**
  ```python
  import logging
  import sys

  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
      handlers=[
          logging.FileHandler("deploy.log"),
          logging.StreamHandler(sys.stdout)
      ]
  )
  logger = logging.getLogger("deployer")

  logger.info("Starting deployment")
  try:
      # simulation
      raise Exception("Connection timeout")
  except Exception as e:
      logger.error(f"Deployment failed: {e}", exc_info=True)
  ```

### `datetime` + `time`
- **Type:** Time manipulation + execution control
- **Methods:**

  | Signature | Example |
  |-----------|---------|
  | `datetime.now()` | `datetime.now()` |
  | `datetime.fromisoformat(s)` | `datetime.fromisoformat("2023-10-11T12:00:00")` |
  | `dt.strftime(fmt)` | `dt.strftime("%Y-%m-%d_%H-%M-%S")` |
  | `timedelta(days=X)` | `now - timedelta(days=7)` |
  | `time.sleep(sec)` | `time.sleep(0.5)` |
  | `time.time()` | `start = time.time()` |

- **Example:**
  ```python
  from datetime import datetime, timedelta
  import time

  now = datetime.now()
  print(f"Start: {now.isoformat()}")

  # Log rotation logic
  seven_days_ago = now - timedelta(days=7)
  # if file_mtime < seven_days_ago.timestamp(): delete()

  # Execution timing
  start = time.time()
  time.sleep(0.1)
  print(f"Elapsed: {time.time() - start:.4f}s")

  # Format for backup filename
  fname = f"backup_{now.strftime('%Y%m%d_%H%M%S')}.tar.gz"
  print(fname)
  ```

## DevOps Context: The "Janitor" Script

Common task: clean up logs older than X days.

```python
import os
import shutil
import time
import logging
from datetime import datetime, timedelta
import argparse

def cleanup(path, days, dry_run=False):
    cutoff = time.time() - (days * 86400)
    count = 0
    size_freed = 0

    for root, dirs, files in os.walk(path):
        for f in files:
            fpath = os.path.join(root, f)
            if os.path.getmtime(fpath) < cutoff:
                size_freed += os.path.getsize(fpath)
                count += 1
                if dry_run:
                    logging.info(f"[DRY] Would remove: {fpath}")
                else:
                    logging.info(f"Removing: {fpath}")
                    os.remove(fpath)
    
    logging.info(f"Summary: Removed {count} files, freed {size_freed // 1024}KB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    cleanup(args.path, args.days, args.dry_run)
```

## Exercises

1. Build `bulk_rename.py`: finds all `*.txt` in a dir and renames them to `*.log` using `glob` and `os.rename`.
2. Build `temp_runner.py`: creates a `TemporaryDirectory`, writes a file into it, runs a `cat` command via `subprocess` on that file, and then lets the directory vanish.
3. Build `heartbeat.py`: every 5 seconds, logs "OK" with a timestamp to `heartbeat.log`. Stop after 5 loops.
4. Enhance the "Janitor" script: use `shutil.rmtree` if a subdirectory is empty and older than X days.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day16 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day16 -v` — see `tests/day16/test_day16.py`
