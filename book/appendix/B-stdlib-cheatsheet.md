# Appendix B — Standard Library Cheatsheet

DevOps-essential modules in the Python Standard Library.

## System & OS
- `os`: File paths, env vars, low-level OS calls.
- `sys`: Interpreter control, `argv`, `path`, `exit`.
- `subprocess`: Running shell commands and managing pipes.
- `shutil`: High-level file operations (copy, move, rmtree).
- `pathlib`: Object-oriented path manipulation.

## Data & Config
- `json`: Parsing and encoding JSON.
- `csv`: Reading and writing CSV files.
- `configparser`: Handling `.ini` files.
- `argparse`: Building robust CLI interfaces.
- `logging`: Event logging with levels and handlers.

## Networking
- `socket`: Low-level network interface.
- `urllib.request`: Simple HTTP client (use `requests` for more).
- `ipaddress`: Validating and manipulating IP/Network addresses.

## Development & Debug
- `pytest`: (External, but standard in DevOps) testing.
- `unittest`: Built-in testing framework.
- `pdb`: The Python debugger.
- `time` / `datetime`: Handling timestamps and durations.
- `hashlib`: MD5, SHA-1, SHA-256 for file verification.
- `base64`: Encoding binary data to text.

## Concurrency
- `threading`: I/O bound concurrency.
- `multiprocessing`: CPU bound parallelism.
- `asyncio`: Single-thread concurrent I/O.
