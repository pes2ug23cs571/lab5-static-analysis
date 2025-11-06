# Reflection – Lab 5 Static Code Analysis

### 1️⃣ Which issues were the easiest to fix, and which were the hardest? Why?
- **Easiest:** Style and formatting warnings from Flake8 (e.g., line length, snake_case names). They just required renaming and spacing adjustments.  
- **Hardest:** Eliminating the `global` statement and designing safe data flow without breaking functionality. It required code refactoring and rethinking how data is passed around.

---

### 2️⃣ Did the static analysis tools report any false positives? If so, describe one example.
- **Example:** Pylint flagged the demo exception handling as “too broad” even though it was intentional for a test function. This is acceptable in limited, non-production code.

---

### 3️⃣ How would you integrate static analysis tools into a real software workflow?
- Add **Pylint**, **Flake8**, and **Bandit** to a GitHub Actions CI pipeline so that every push or pull request is scanned automatically.  
- Use **pre-commit hooks** to run Flake8 and Bandit locally before committing changes.  
- Define a minimum Pylint score threshold (≥ 9/10) to enforce consistent code quality.

---

### 4️⃣ What tangible improvements did you observe after fixes?
- Bandit now reports **0 security issues** ✅  
- Pylint score improved from **4.8 → 9.9/10** ✅  
- Flake8 clean with no errors ✅  
- Code is now safer (no `eval`), readable (docstrings, style consistency), and maintainable (type-checked and validated inputs).  
- Logging and error messages make the program easier to debug and extend.
