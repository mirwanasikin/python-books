# Day 22 — OOP Inheritance & Polymorphism

Keywords: `class`, `super`

## Keywords + Methods

### Inheritance and `super()`
- **Type:** Object-oriented extension mechanism
- **Methods:** `super().__init__()`, method overriding
- **Example:**
  ```python
  from abc import ABC, abstractmethod

  class BaseService(ABC):
      def __init__(self, name: str):
          self.name = name
          self.status = "stopped"

      @abstractmethod
      def start(self) -> None:
          pass

      def stop(self) -> None:
          self.status = "stopped"
          print(f"Service {self.name} stopped.")

  class NginxService(BaseService):
      def __init__(self, port: int = 80):
          super().__init__("nginx")
          self.port = port

      def start(self) -> None:
          self.status = "running"
          print(f"Nginx started on port {self.port}.")

  class ApacheService(BaseService):
      def __init__(self, port: int = 8080):
          super().__init__("apache2")
          self.port = port

      def start(self) -> None:
          self.status = "running"
          print(f"Apache started on port {self.port}.")

  # Polymorphism in action
  services = [NginxService(80), ApacheService(8080)]
  for s in services:
      s.start()
  ```

### Mixins and Multiple Inheritance
- **Type:** Reusable behavior classes
- **Methods:** Multiple inheritance lookup via MRO (Method Resolution Order)
- **Example:**
  ```python
  class LoggingMixin:
      def log(self, message: str):
          print(f"[LOG] {self.__class__.__name__}: {message}")

  class DatabaseService(LoggingMixin):
      def connect(self):
          self.log("Connecting to database...")

  db = DatabaseService()
  db.connect()
  print(DatabaseService.__mro__)
  ```

## DevOps Context: Abstracting Infrastructure Daemons
Base classes define standard interfaces for all system daemons (start, stop, reload), while derived classes handle service-specific commands (systemctl, service files).

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day22 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day22 -v` — see `tests/day22/test_day22.py`
