# Lab 5 – Static Code Analysis  
### Identified and Fixed Issues

| **Issue** | **Type** | **Line(s)** | **Description** | **Fix Approach** |
|------------|-----------|-------------|------------------|------------------|
| Mutable default argument (`logs=[]`) | Bug | 12 | A mutable list was shared across function calls, causing data carry-over. | Changed default value to `None` and created a new list inside the function. |
| Bare `except:` used | Error Handling | 45 | Broad `except` hides real exceptions and makes debugging hard. | Replaced with `except KeyError` and other specific exception types. |
| Use of `eval()` | Security | 59 | `eval()` can execute arbitrary code → critical security risk. | Removed `eval()` and replaced with safe, explicit logic. |
| File opened without context manager | Resource Management | 80 | File not closed automatically if exception occurs. | Used `with open(..., encoding="utf-8")` to ensure safe file handling. |
| Function names not in `snake_case` | Style | Multiple | Violated PEP 8 naming conventions (`addItem`, `removeItem`). | Renamed to `add_item`, `remove_item`, etc. |
| Missing docstrings | Documentation | Multiple | Functions lacked descriptions, reducing readability. | Added concise docstrings for every function. |
| `global` statement used | Design | 103 | `load_data()` modified global variable directly. | Refactored to return dictionary and assigned result at call site. |
| Broad `Exception` caught | Error Handling | 173 | `_demo_operations()` caught all exceptions. | Replaced with specific `(ValueError, KeyError)` handlers. |
| Long lines (> 79 chars) | Style | Multiple | Lines exceeded PEP 8 length limit. | Wrapped lines and set `max-line-length = 100` in `.flake8`. |

✅ **Total Issues Fixed:** 9  
All high and medium severity issues resolved (confirmed via Bandit, Pylint, Flake8 reports).
