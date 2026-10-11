# Day 23 — Magic Methods & Operator Overloading

Keywords: `class`, `__str__`, `__repr__`, `__eq__`, `__hash__`, `__len__`, `__getitem__`, `__call__`, `__enter__`, `__exit__`

## Keywords + Methods

### Dunder Methods: String and Representation
- **Type:** Default representations for objects
- **Methods:** `__str__`, `__repr__`
- **Example:**
  ```python
  class Config:
      def __init__(self, host: str, port: int):
          self.host = host
          self.port = port

      def __repr__(self) -> str:
          return f"Config(host='{self.host}', port={self.port})"

      def __str__(self) -> str:
          return f"{self.host}:{self.port}"

  cfg = Config("192.168.1.1", 8080)
  print(repr(cfg))  # Config(host='192.168.1.1', port=8080)
  print(str(cfg))   # 192.168.1.1:8080
  ```

### Equality and Hashing
- **Type:** Identity and collection membership
- **Methods:** `__eq__`, `__hash__`
- **Example:**
  ```python
  class ServerPool:
      def __init__(self, name: str):
          self.name = name

      def __eq__(self, other):
          return isinstance(other, ServerPool) and self.name == other.name

      def __hash__(self):
          return hash(self.name)

  pool1 = ServerPool("web")
  pool2 = ServerPool("web")
  pools = {pool1, pool2}
  print(len(pools))  # 1 (duplicates merged)
  ```

### Length and Indexing
- **Type:** Size and data access
- **Methods:** `__len__`, `__getitem__`
- **Example:**
  ```python
  class LogBuffer:
      def __init__(self):
          self.lines = []

      def __len__(self):
          return len(self.lines)

      def __getitem__(self, idx):
          return self.lines[idx]

      def append(self, line: str):
          self.lines.append(line)

  lb = LogBuffer()
  lb.append("ERROR: disk full")
  lb.append("INFO: service restarted")
  print(len(lb))    # 2
  print(lb[0])     # ERROR: disk full
  ```

### Callable and Context Manager
- **Type:** Invokability and resource management
- **Methods:** `__call__`, `__enter__`, `__exit__`
- **Example:**
  ```python
  class SSHConnection:
      def __call__(self, command: str) -> str:
          print(f"Running: {command}")
          return f"Output: {command} executed"

      def __enter__(self):
          print("Opening SSH session")
          return self

      def __exit__(self, exc_type, exc_val, exc_tb):
          print("Closing SSH session")

  with SSHConnection() as ssh:
      result = ssh("ls -la /etc")
      print(result)
  ```

## DevOps Context: Configuration, Logging, and Resource Handling
Magic methods simplify using Python objects as proxies for system configuration, log collections, and context-managed connections (e.g., file handles, database links).

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day23 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day23 -v` — see `tests/day23/test_day23.py`
