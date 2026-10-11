# Day 26 — Standard Library Tour

Keywords: `collections`, `functools`, `itertools`, `contextlib`, `dataclasses`, `enum`, `abc`, `math`, `random`, `hashlib`, `base64`

## Keywords + Methods

### Core Collections
- **Type:** Data structures with specialized methods
- **Methods:** `Counter`, `defaultdict`, `deque`, `namedtuple`
- **Example:**
  ```python
  from collections import Counter, defaultdict, deque, namedtuple

  # Count package versions in logs
  log_lines = ["Install nginx", "Update nginx", "Install nginx", "Update apache"]
  counts = Counter(log_lines)
  print(counts.most_common(2))

  # Default service health map
  health_map = defaultdict(lambda: "unknown")
  health_map["web"] = "healthy"
  print(health_map["db"])  # unknown

  # FIFO queue for task processing
  task_queue = deque(["clean_cache", "rotate_logs"])
  print(task_queue.popleft())

  # Named service specification
  Service = namedtuple("Service", "name port type")
  web = Service("web", 80, "http")
  print(web.port)
  ```

### Functional Utilities
- **Type:** Higher-order functions and caching decorators
- **Methods:** `lru_cache`, `partial`, `reduce`, `total_ordering`
- **Example:**
  ```python
  from functools import lru_cache, partial
  from operator import add
  from collections import namedtuple

  @lru_cache(maxsize=None)
  def get_service_status(host: str) -> str:
      return subprocess.getoutput(f"systemctl is-active {host}")

  cached_get_service = partial(get_service_status, host="nginx")
  print(cached_get_service())

  Service = namedtuple("Service", "name port")
  ServiceWithOrder = total_ordering(Service)
  s1 = ServiceWithOrder("web", 80)
  s2 = ServiceWithOrder("web", 80)
  print(s1 == s2)
  ```

### Context Managers
- **Type:** Resource handling with `with` statements
- **Methods:** `contextlib.contextmanager`, `closing`, `nullcontext`
- **Example:**
  ```python
  from contextlib import contextmanager
  from tempfile import NamedTemporaryFile

  @contextmanager
  def temp_config_file():
      with NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
          f.write('host: localhost\nport: 8080')
          yield f.name

  with temp_config_file() as path:
      print(f"Created config at {path}")
  ```

### Data Classes, Enums, and ABCs
- **Type:** Simplified classes and type grouping
- **Methods:** `@dataclass`, `@unique`, `@abstractmethod`
- **Example:**
  ```python
  from dataclasses import dataclass
  from enum import Enum
  from abc import ABC, abstractmethod

  @dataclass
  class ServiceConfig:
      host: str
      port: int
      ssl: bool = False

  cfg = ServiceConfig("prod.db", 5432, True)
  print(cfg)

  class Health(Enum):
      HEALTHY = "healthy"
      DEGRADED = "degraded"
      FAILED = "failed"

  print(Health.HEALTHY.value)

  class ServiceMonitor(ABC):
      @abstractmethod
      def check(self):
          pass
  ```

## DevOps Focus: Infrastructure Data Modeling
Standard library constructs provide the building blocks for representing configuration, monitoring results, and safe resource handling in automation scripts.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day26 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day26 -v` — see `tests/day26/test_day26.py`
