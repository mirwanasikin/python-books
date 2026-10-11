# Day 21 — OOP Basics

Keywords: `class`

## Keywords + Methods

### `class`
- **Type:** Object-oriented programming definition keyword
- **Methods:** `__init__`, `__str__`, custom methods, class methods (`@classmethod`), static methods (`@staticmethod`)
- **Example:**
  ```python
  class Server:
      # Class attribute shared across all instances
      os_type = "Linux"
      total_servers = 0

      def __init__(self, hostname: str, ip: str, cpu_cores: int):
          self.hostname = hostname
          self.ip = ip
          self.cpu_cores = cpu_cores
          self.is_running = False
          Server.total_servers += 1

      def start(self) -> None:
          self.is_running = True
          print(f"Server {self.hostname} ({self.ip}) started.")

      def stop(self) -> None:
          self.is_running = False
          print(f"Server {self.hostname} stopped.")

      @classmethod
      def get_total(cls) -> int:
          return cls.total_servers

      @staticmethod
      def validate_ip(ip: str) -> bool:
          parts = ip.split(".")
          return len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

  # Usage
  if Server.validate_ip("192.168.1.10"):
      srv = Server("web-01", "192.168.1.10", 4)
      srv.start()
      print(f"Total servers: {Server.get_total()}")
  ```

### Encapsulation and Properties
- **Type:** Data hiding and getter/setter property mechanism
- **Methods:** `@property`, `@<property_name>.setter`
- **Example:**
  ```python
  class ServiceConfig:
      def __init__(self, port: int):
          self._port = port

      @property
      def port(self) -> int:
          return self._port

      @port.setter
      def port(self, value: int):
          if not (1 <= value <= 65535):
              raise ValueError("Port must be between 1 and 65535")
          self._port = value

  config = ServiceConfig(80)
  config.port = 443
  # config.port = 99999  # Raises ValueError
  ```

## DevOps Context: Server and Service Modeling
In infrastructure automation, object-oriented design allows abstracting physical or virtual servers, container deployments, and network configurations into manageable code units with clear state control and encapsulation.

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day21 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day21 -v` — see `tests/day21/test_day21.py`
