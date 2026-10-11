# Day 30 — Final Exam

Keywords: `False, None, True, and, as, await, async, break, class, continue, def, del, elif, else, except, finally, for, from, global, if, import, in, is, lambda, match, nonlocal, not, or, pass, raise, return, try, while, with, yield`

Soft keywords: `match, case, type, _` + OOP/dunder (`self, super, __init__, __str__, __repr__, __eq__, __hash__, __len__, __getitem__, __call__, __enter__, __exit__`) + decorators (`@staticmethod, @classmethod, @property`) + builtins (`isinstance, list, tuple, dict, set, frozenset, range, len, str, int, float, bool, bytes, bytearray, memoryview, complex`) + stdlib (`re, math, datetime, time, json, os, sys, subprocess, pathlib, argparse, logging, requests, urllib, urllib.request, urllib.parse, socket, threading, multiprocessing, asyncio, concurrent.futures, collections, Counter, defaultdict, deque, namedtuple`) + third-party (`boto3, paramiko, rich, click, typer`) + testing (`pytest, unittest, mock`)

## Exam Overview

This exam covers every keyword and concept from Days 1–29. Work without AI assistance. Total: 35 points. Target time: 2 hours.

---

## Part A — Multiple Choice Questions (1 point each, 20 points)

**1.** Which operator checks object identity rather than value equality?
- A) `==`
- B) `is`
- C) `in`
- D) `and`

**2.** In `match` statements, which case acts as the default/fallback?
- A) `case _:`
- B) `case None:`
- C) `case default:`
- D) `default case:`

**3.** What does `yield` produce when called inside a function?
- A) A list
- B) A generator object
- C) A tuple
- D) A dictionary

**4.** Which of these is NOT a valid use of `nonlocal`?
- A) Inside a nested function to modify an enclosing variable.
- B) At module scope to declare a global variable.
- C) Referencing a variable from the enclosing scope.
- D) Modifying a variable in the nearest enclosing scope.

**5.** What is the output of `bool(0) or bool(0.0) or bool('')`?
- A) `0`
- B) `0.0`
- C) `''`
- D) `False`

**6.** Which statement imports all names from a module into the current namespace?
- A) `import module`
- B) `import module as alias`
- C) `from module import *`
- D) `from module import name`

**7.** What will `del` on a list index do?
- A) Set the element to `None`.
- B) Remove the element, shifting remaining elements.
- C) Create a copy without that element.
- D) Raise a `RuntimeError`.

**8.** A context manager's exit logic is defined by which dunder method?
- A) `__enter__`
- B) `__init__`
- C) `__exit__`
- D) `__call__`

**9.** Which decorator converts an instance method into a method callable without an instance?
- A) `@property`
- B) `@classmethod`
- C) `@staticmethod`
- D) `@abstractmethod`

**10.** `async def` combined with which keyword creates a coroutine suspension point?
- A) `await`
- B) `yield`
- C) `raise`
- D) `assert`

**11.** In `try/except`, which clause always executes regardless of exception?
- A) `except`
- B) `finally`
- C) `else`
- D) `raise`

**12.** What does `assert` raise if its condition is false?
- A) `ValueError`
- B) `TypeError`
- C) `AssertionError`
- D) `RuntimeError`

**13.** Which keyword declares a variable as belonging to the module (global) scope inside a function?
- A) `local`
- B) `nonlocal`
- C) `global`
- D) `module`

**14.** What will this code print?
```python
def outer():
    x = 5
    def inner():
        nonlocal x
        x = 10
    inner()
    return x
print(outer())
```
- A) `5`
- B) `10`
- C) `None`
- D) `UnboundLocalError`

**15.** Which built-in function returns the number of items in a container?
- A) `count()`
- B) `len()`
- C) `size()`
- D) `num()`

**16.** A class defines `__len__` and `__getitem__`. After `del obj[key]`, which method may be called?
- A) `__delitem__`
- B) `__delattr__`
- C) The element is removed; `__len__` reflects the count.
- D) `__getitem__` raises `KeyError`.

**17.** When is `else` allowed after a `for` loop?
- A) Always, as a separator.
- B) When the loop completed without `break`.
- C) Only with `while` loops.
- D) Never—`else` is only for `if`.

**18.** Which of these is a soft keyword (contextual identifier)?
- A) `for`
- B) `class`
- C) `match`
- D) `return`

**19.** What is the result of calling a `lambda` directly?
```python
(lambda x: x + 1)(5)
```
- A) `4`
- B) `5`
- C) `6`
- D) `SyntaxError`

**20.** In `with` statements, what does `Exit Stack` pattern help with?
- A) Exiting a stack data structure.
- B) Entering an exit gate.
- C) Dynamically managing multiple context managers.
- D) Replacing `return` with `yield`.

---

## Part B — Coding Challenges (3–5 points each, 15 points)

**Challenge 1 (3 pts).** Implement `filter_evens` using a **generator** (`yield`) that yields even numbers from a list. Use `if/else` for filtering.
```python
# tests/day30 expects: list(filter_evens([1,2,3,4,5])) == [2,4]
```

**Challenge 2 (3 pts).** Write a `Counter` class using OOP concepts (`class`, `self`, `__init__`, `__str__`, `__repr__`). It must count how many times `increment()` is called. `__str__` returns the current count as `f"Count: {n}"`.

**Challenge 3 (4 pts).** Build `safe_read(path)` using `try/except/finally` and `with` (`pathlib.Path`). It returns file contents or `None` on `OSError`. A `@staticmethod` named `default()` returns `"default"`.

**Challenge 4 (4 pts).** Create `async fetch_all(urls)` using `async def`, `await`, and `concurrent.futures`. Return dict mapping `url → len(body)` for simulated bodies. Must be runnable: `asyncio.run(fetch_all([...]))`.

**Challenge 5 (1 pt).** Use `@property` and `@classmethod` in any small class to demonstrate the pattern. One-line description of difference between them.

---

## Scoring Rubric

| Section         | Points                       |
|-----------------|------------------------------|
| Part A (MC)     | 1 pt per correct answer (20) |
| Challenge 1     | 3 pts (generator + yield)    |
| Challenge 2     | 3 pts (class + dunder init/str/repr) |
| Challenge 3     | 4 pts (try/except/finally + with + staticmethod) |
| Challenge 4     | 4 pts (async/await/concurrency + futures) |
| Challenge 5     | 1 pt (@property/@classmethod demonstration) |
| **Total**       | **35**                       |

Grading scale: 32–35 A, 28–31 B, 24–27 C, 20–23 D, <20 needs review.

## Example: Full runnable snippet (Day 30 integration)

```python
import asyncio
import concurrent.futures

def filter_evens(values):
    for v in values:
        if v % 2 == 0:
            yield v

class Counter:
    def __init__(self):
        self._n = 0
    def increment(self):
        self._n += 1
    def __str__(self):
        return f"Count: {self._n}"
    def __repr__(self):
        return f"Counter({self._n})"

with Counter() as c:
    del c

try:
    raise ValueError("demo")
except ValueError as e:
    msg = e
finally:
    msg = msg  # no-op cleanup
```

## Todo
- [ ] Read + type every example
- [ ] Complete exercises (no copy-paste)
- [ ] Pass `pytest tests/day30 -v`
- [ ] Build mini-script for Linux

## Test
Run: `pytest tests/day30 -v`
