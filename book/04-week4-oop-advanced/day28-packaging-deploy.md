# Day 28 — Packaging & Deployment

Keywords: `venv`, `pip`, `requirements.txt`, `pyproject.toml`, `setup.py`, `entry_points`, `setuptools`, `pipenv`, `poetry`

## Keywords + Methods

### Virtual Environments & Dependency Management
- **Type:** Isolated Python environments
- **Methods:** `venv` module, `pip install`, `pip freeze`, `pip install -r requirements.txt`
- **Example:**
  ```python
  import subprocess
  import sys

  def create_venv(path: str = ".venv"):
      subprocess.run([sys.executable, "-m", "venv", path], check=True)

  def install_deps(venv_path: str, req_path: str):
      pip = os.path.join(venv_path, "bin", "pip")
      subprocess.run([pip, "install", "-r", req_path], check=True)

  # Create and populate virtual environment
  create_venv()
  install_deps(".venv", "requirements.txt")
  ```

### Modern Packaging with `pyproject.toml`
- **Type:** Configuration-driven packaging (PEP 621, PEP 508)
- **Methods:** `[build-system]`, `[project]`, `[project.optional-dependencies]`, `[tool.*]` sections
- **Example:**
  ```python
  # Generated pyproject.toml content (not executed)
  # [build-system]
  # requires = ["hatchling"]
  # build-backend = "hatchling.build"
  # [project]
  # name = "infra-monitor"
  # version = "0.1.0"
  # dependencies = ["requests", "pyyaml", "typer[all]"]
  # [project.scripts]
  # infra = "infra_monitor:main"
  ```

### Building and Installing Tools
- **Type:** Package building and entry-point creation
- **Methods:** `python -m build`, `pip install .`, `entry_points`
- **Example:**
  ```python
  import subprocess
  import shlex

  def build_package():
      subprocess.run([sys.executable, "-m", "build"], check=True)

  def install_locally():
      subprocess.run([sys.executable, "-m", "pip", "install", "--user", "."], check=True)

  # Build and install the package
  build_package()
  install_locally()
  ```

## DevOps Context: Distributing Automation Scripts
Proper packaging enables reproducible deployment of configuration management tools across environments, with single-command installation and clean dependency specification.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day28 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day28 -v` — see `tests/day28/test_day28.py`
