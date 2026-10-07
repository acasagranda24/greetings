# Session 03 · Follow-Along Guide: Environments and the Quality Toolchain

**Course:** Python Environments & Engineering Workflows (MSA-DATI07-01) · MSc 1 · 2h

## What we build today

`greetings` still runs, but only on your laptop, because nothing says which Python or which tools it
needs. Today the repo learns to describe itself, then to check itself:

- **uv** creates the project, the environment (`.venv`) and a **lockfile** (`uv.lock`) so that anyone
  rebuilds exactly your versions.
- **ruff** formats and lints, **mypy** checks types, **pytest** runs real tests on `Student`
  (`welcome`, `register`, `enroll`).
- Everything goes in the way Session 2 taught you: one branch, atomic commits, one PR
  titled `chore: introduce quality toolchain`, reviewed by your partner, merged on the protected
  `main`.

Every step has the same four parts: Predict, Run, You should see, Why. Versions (`pytest 9.1.1`...)
and paths will differ on your machine.

> **On the board** boxes say what to draw. **If it goes wrong** boxes list the usual accidents.

**End of session deliverable:** a merged PR on your `greetings` repository with `pyproject.toml`,
`uv.lock`, ruff / mypy configuration and at least five passing tests. `git log --oneline --graph`
shows one atomic commit per tool.

| Part | Topic | Mode |
|---|---|---|
| 0 | Where we stand, three weaknesses of `venv` + `pip freeze` | all together |
| 1 | A uv project | all together |
| 2 | Lockfile: pin vs constraint, delete `.venv` | all together |
| | Break (15 min) | |
| 3 | ruff | all together |
| 4 | mypy | all together |
| 5 | pytest | pairs |
| 6 | The pull request | pairs |

On macOS type `python3` where this guide says `python` (only needed outside `uv run`). On Windows use
Git Bash.

---

## Part 0 · Where we stand

Start from an up-to-date `main` and a new branch. You never commit on `main` any more (Session 2).

```bash
cd greetings
git switch main
git pull
git switch -c chore/toolchain
```

In Bachelor you used `python -m venv` and `pip freeze > requirements.txt`. Say out loud what goes
wrong with that:

1. `pip freeze` mixes what you asked for with what came along. You wanted `pytest`, the file
   lists twelve packages and nothing says which one you chose.
2. Nothing records the Python version. The same file installs differently on 3.10 and 3.13.
3. The environment is a folder you maintain by hand: `activate`, `pip install`, forget to
   `freeze`, repeat.

> **On the board:** two columns. Left, "what I want": `pytest`. Right, "what I get": `pytest`,
> `pluggy`, `iniconfig`, `packaging`... Today's tool keeps both columns, in two different files.

---

## Part 1 · A uv project

### 1.1 Turn the folder into a project

**Predict:** which file will `uv init --bare` create? Which one will not be created?

```bash
uv init --bare
cat pyproject.toml
```

**You should see:**

```
Initialized project `greetings`
```

```toml
[project]
name = "greetings"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []
```

`--bare` creates only `pyproject.toml`: no sample `main.py`, no `.python-version`. Edit
`requires-python` to `">=3.12"` so that a classmate on 3.12 can use your project too.

**Why:** `pyproject.toml` is the project's identity card: name, supported Python, dependencies. It
is a standard that pip, uv, ruff, mypy and pytest all read.

### 1.2 Add the tools as dev dependencies

**Predict:** is there a `.venv` folder yet? After the next command?

```bash
uv add --dev pytest ruff mypy
cat pyproject.toml
ls -a
```

**You should see:**

```
Using CPython 3.13.16 interpreter at: /usr/bin/python3
Creating virtual environment at: .venv
Resolved 14 packages in 12ms
Installed 12 packages in 27ms
 + ast-serialize==0.12.1
 + iniconfig==2.3.0
 + librt==0.16.0
 + mypy==2.4.0
 + mypy-extensions==1.1.0
 + packaging==26.3
 + pathspec==1.1.1
 + pluggy==1.6.0
 + pygments==2.21.0
 + pytest==9.1.1
 + ruff==0.16.10
 + typing-extensions==4.16.0
```

```toml
[dependency-groups]
dev = [
    "mypy>=2.4.0",
    "pytest>=9.1.1",
    "ruff>=0.16.10",
]
```

`ls -a` now shows `.venv/`, `pyproject.toml` and `uv.lock`.

**Why:** you asked for three packages and uv installed twelve (the other nine are their
dependencies). `--dev` puts them in a separate group: the project needs them to be developed, not to
run.

### 1.3 Run the code through uv

```bash
uv run python greetings.py
```

```
Welcome to Albert School, Tuka!
Registered as student #1
Confirmation sent to tuka@albertschool.com
Tuka Bade joins MSc 1 Data.
```

**Why:** `uv run` makes sure `.venv` matches the lockfile, then runs the command inside it. No
`activate`. We use this form for the rest of the course.

### 1.4 Ignore the environment, commit the project

```bash
echo ".venv/" >> .gitignore
git status --short
```

```
 M .gitignore
?? pyproject.toml
?? uv.lock
```

`.venv` does not appear in the status, because the line we just added to `.gitignore` hides it.
Commit the three files:

```bash
git add .gitignore pyproject.toml uv.lock
git commit -m "chore: add uv project and lockfile"
```

```
[chore/toolchain 6501aee] chore: add uv project and lockfile
 3 files changed, 373 insertions(+)
 create mode 100644 pyproject.toml
 create mode 100644 uv.lock
```

**Why:** We commit `uv.lock` and never `.venv/`. The environment can be rebuilt at any time; the
lockfile is the recipe for it.

> **If it goes wrong:**
> - `uv: command not found`: install uv (`curl -LsSf https://astral.sh/uv/install.sh | sh` on
>   macOS, or the PowerShell installer on Windows, run once), then open a new terminal.
> - uv downloads a Python you did not expect: normal when your system Python is older than
>   `requires-python`. It lives in uv's cache, not in your system.

---

## Part 2 · Lockfile: a pin is not a constraint

### 2.1 Two files, two jobs

Open `pyproject.toml`: `"pytest>=9.1.1"`. Open `uv.lock` and look for the exact line:

```bash
grep -n -B1 -A1 '^name = "pytest"' uv.lock
```

```
312-[[package]]
313:name = "pytest"
314-version = "9.1.1"
```

| File | Says | Example |
|---|---|---|
| `pyproject.toml` | what my project accepts (a constraint) | `pytest>=9.1.1` |
| `uv.lock` | what was actually installed (a pin) | `pytest 9.1.1` |

> **A pin is not a constraint.** A constraint says what your code tolerates. A pin records one
> installation that worked. You need both: the first keeps you flexible, the second lets you
> reproduce.

### 2.2 Delete the environment, then rebuild it

**Predict:** have we lost anything we cannot get back?

```bash
rm -rf .venv
uv run --locked python greetings.py
ls -d .venv
```

```
Using CPython 3.13.16 interpreter at: /usr/bin/python3
Creating virtual environment at: .venv
Installed 12 packages in 20ms
Welcome to Albert School, Tuka!
Registered as student #1
Confirmation sent to tuka@albertschool.com
Tuka Bade joins MSc 1 Data.
.venv
```

**Why:** the environment came back with the same versions in a fraction of a second.
`--locked` means "fail rather than change the lockfile". Use it on every machine that is not yours,
and in CI (Session 4). Deleting `.venv` is now routine.

> **On the board:** `pyproject.toml` (constraints) → `uv lock` → `uv.lock` (pins) → `uv sync` →
> `.venv/`. Arrows go left to right only; you never edit the right-hand side by hand.

### 2.3 What `--locked` protects you from

Add a dependency by hand in `pyproject.toml` (`dependencies = ["rich>=13"]`) and run:

```bash
uv sync --locked
```

```
Resolved 17 packages in 215ms
error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.

hint: To update the lockfile, run `uv lock`.
```

**Why:** the lockfile no longer matches `pyproject.toml`. Without `--locked`, `uv sync` would quietly
update the lock. With it, a stale lockfile is an error, which is what you want on a build machine.
Run `uv sync` (it relocks and installs `rich`), look at `git diff --stat`, then undo by restoring
`dependencies = []` and running `uv sync` again: `rich` is uninstalled and `uv.lock` is back to its
committed state.

### 2.4 Export for tools that want `requirements.txt`

```bash
uv export --no-hashes --no-emit-project -o requirements.txt
head -8 requirements.txt
```

```
# This file was autogenerated by uv via the following command:
#    uv export --no-hashes --no-emit-project -o requirements.txt
ast-serialize==0.12.1
    # via mypy
colorama==0.4.6 ; sys_platform == 'win32'
    # via pytest
iniconfig==2.3.0
    # via pytest
```

Delete it again (`rm requirements.txt`): the lockfile stays the source of truth, and you
generate a `requirements.txt` only when something (Docker, an old CI) insists on it. Look at the
`# via` comments: they restore what `pip freeze` lost.

> **If it goes wrong:** `ModuleNotFoundError` in a fresh clone: you ran `python greetings.py` instead
> of `uv run python greetings.py`, so you used the system Python, not `.venv`.

---

## Break (15 min)

---

## Part 3 · ruff: format and lint

ruff does two jobs: `ruff format` rewrites the layout (like Black), `ruff check` finds mistakes
(unused imports, ambiguous names...).

```bash
uv run ruff format --check .
uv run ruff check .
```

```
2 files already formatted
All checks passed!
```

(The count of files depends on what is in your folder.) By default ruff checks few rules. Choose a
richer set and set the line length, in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RUF"]
```

| Letters | Rules |
|---|---|
| `E`, `F` | pycodestyle and pyflakes basics (syntax-level mistakes, unused names) |
| `I` | import sorting |
| `B` | likely bugs (bugbear) |
| `UP` | modernise old syntax (pyupgrade) |
| `SIM` | simplifications |
| `RUF` | ruff's own rules |

### Break it on purpose

**Predict:** how many problems does ruff find if the first line of `greetings.py` becomes
`import os`?

```bash
uv run ruff check .
```

```
I001 [*] Import block is un-sorted or un-formatted
 --> greetings.py:1:1
  |
1 | import os
  | ^^^^^^^^^
2 | class Student:
...
F401 [*] `os` imported but unused
 --> greetings.py:1:8
...
Found 2 errors.
[*] 2 fixable with the `--fix` option.
```

```bash
uv run ruff check --fix .
```

```
Found 1 error (1 fixed, 0 remaining).
```

`git diff --stat` shows that `greetings.py` is back to what it was: ruff removed the import. Commit
the configuration:

```bash
git add pyproject.toml
git commit -m "chore: configure ruff"
```

**Why:** `[*]` means ruff can fix it itself. These fixes cost almost nothing, so in Session 4 they will
run automatically on every commit.

---

## Part 4 · mypy: check the types

Python does not check types when it runs. mypy reads your annotations and tells you when they
disagree with the code. `--strict` demands annotations everywhere:

```bash
uv run mypy --strict greetings.py
```

```
greetings.py:2: error: Function is missing a type annotation  [no-untyped-def]
greetings.py:9: error: Function is missing a return type annotation  [no-untyped-def]
greetings.py:12: error: Function is missing a type annotation  [no-untyped-def]
greetings.py:17: error: Function is missing a type annotation  [no-untyped-def]
greetings.py:23: error: Need type annotation for "registry" (hint: "registry: list[<type>] = ...")  [var-annotated]
greetings.py:24: error: Call to untyped function "Student" in typed context  [no-untyped-call]
greetings.py:25: error: Call to untyped function "register" in typed context  [no-untyped-call]
greetings.py:26: error: Call to untyped function "welcome" in typed context  [no-untyped-call]
greetings.py:29: error: Call to untyped function "enroll" in typed context  [no-untyped-call]
Found 9 errors in 1 file (checked 1 source file)
```

Nine errors, but they come down to four missing annotations (`__init__`, `welcome`, `register`, `enroll`)
plus `registry`. Type the class, and while we are there, turn the bottom block into a `main()`
function so tests can call it:

```python
class Student:
    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.student_id: int | None = None
        self.classroom: str | None = None

    def welcome(self) -> str:
        return f"Welcome to Albert School, {self.first_name}!"

    def register(self, registry: list["Student"]) -> int:
        self.student_id = len(registry) + 1
        registry.append(self)
        return self.student_id

    def enroll(self, classroom: str) -> str:
        self.classroom = classroom
        return f"{self.first_name} {self.last_name} joins {classroom}."


def main() -> None:
    registry: list[Student] = []
    student = Student("Tuka", "Bade", "tuka@albertschool.com")
    student.register(registry)
    print(student.welcome())
    print(f"Registered as student #{student.student_id}")
    print(f"Confirmation sent to {student.email}")
    print(student.enroll("MSc 1 Data"))


if __name__ == "__main__":
    main()
```

(If your Session 2 branches added methods such as `farewell`, `full_name` or `is_enrolled`, keep them
and type them too: each needs `-> str` or `-> bool`.)

```bash
uv run mypy --strict greetings.py
uv run python greetings.py
```

```
Success: no issues found in 1 source file
```

**Why:** Look at `self.student_id: int | None = None`. The id is `None` until the
student is registered, and mypy now makes every caller deal with that. A forgotten empty case becomes
an error before the code runs.

```bash
git add greetings.py
git commit -m "refactor: add type hints and a main function"
```

---

## Part 5 · pytest: tests that protect the behaviour

Create `tests/test_student.py`. In pairs: one types, the other reads the test names out loud and
says what each one would catch.

```python
import pytest

from greetings import Student, main


def make_student() -> Student:
    return Student("Ada", "Lovelace", "ada@albertschool.com")


def test_welcome_uses_first_name() -> None:
    assert make_student().welcome() == "Welcome to Albert School, Ada!"


def test_register_returns_and_stores_the_id() -> None:
    registry: list[Student] = []
    student = make_student()
    assert student.register(registry) == 1
    assert student.student_id == 1
    assert registry == [student]


@pytest.mark.parametrize("already_registered", [0, 1, 5])
def test_register_numbers_after_the_registry_size(already_registered: int) -> None:
    registry = [make_student() for _ in range(already_registered)]
    assert make_student().register(registry) == already_registered + 1


def test_enroll_sets_the_classroom() -> None:
    student = make_student()
    assert student.enroll("MSc 1 Data") == "Ada Lovelace joins MSc 1 Data."
    assert student.classroom == "MSc 1 Data"


def test_main_prints_the_four_lines(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Welcome to Albert School, Tuka!"
    assert len(lines) == 4
```

**Predict:** will `uv run pytest` find `greetings`?

```bash
uv run pytest
```

```
tests/test_student.py:3: in <module>
    from greetings import Student, main
E   ModuleNotFoundError: No module named 'greetings'
=========================== short test summary info ============================
ERROR tests/test_student.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!
```

**Why:** the test file lives in `tests/`, `greetings.py` lives at the root, and Python does not look
at the root from there. Today's fix is a configuration line telling pytest where to look. Add to
`pyproject.toml`, together with the mypy configuration:

```toml
[tool.mypy]
strict = true
files = ["greetings.py", "tests"]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
addopts = ["-ra", "--strict-markers"]
```

```bash
uv run pytest
uv run mypy
uv run ruff format --check . && uv run ruff check .
```

```
collected 7 items

tests/test_student.py .......                                            [100%]

============================== 7 passed in 0.01s ===============================
```

```
Success: no issues found in 2 source files
3 files already formatted
All checks passed!
```

Seven tests: the `parametrize` line produces three of them from one function.

> **A temporary hack.** `pythonpath = ["."]` makes the tests pass but hides a structural
> problem: `greetings.py` is not an installed package. In Session 4 we fix it with the src layout
> and delete this line.

### The tests must be able to fail

A test that cannot fail protects nothing. Break `register`: replace
`len(registry) + 1` by `len(registry)`, then run:

```bash
uv run pytest -q
```

```
E       assert 5 == (5 + 1)
...
FAILED tests/test_student.py::test_register_returns_and_stores_the_id - asser...
FAILED tests/test_student.py::test_register_numbers_after_the_registry_size[0]
FAILED tests/test_student.py::test_register_numbers_after_the_registry_size[1]
FAILED tests/test_student.py::test_register_numbers_after_the_registry_size[5]
4 failed, 3 passed in 0.03s
```

Four of seven go red. Put the `+ 1` back, run again (`7 passed`), then commit:

```bash
git add pyproject.toml tests
git commit -m "test: cover Student with pytest"
git log --oneline --graph -5
```

```
* 41ce48a test: cover Student with pytest
* 6083b79 refactor: add type hints and a main function
* 385beef chore: configure ruff
* 6501aee chore: add uv project and lockfile
* 09e991f docs: add README
```

> **If it goes wrong:**
> - `7 passed` but the number of tests is smaller: a test function whose name does not start with
>   `test_` is silently ignored.
> - mypy complains in `tests/`: you forgot `-> None` on a test, or the `capsys` fixture type.
> - You broke the code and forgot to restore it before committing: `git restore greetings.py`.

---

## Part 6 · The pull request

```bash
git push -u origin chore/toolchain
```

Open the PR on GitHub:

- **Title:** `chore: introduce quality toolchain`
- **Description:** what (uv + ruff + mypy + pytest), why (anyone can rebuild and check the project),
  how to check (`uv sync --locked` then the four commands).
- **Reviewer:** your partner.

**Reviewer checklist** (say it out loud while reading the *Files changed* tab):

1. Is `uv.lock` in the diff, and is `.venv` absent from it?
2. Does each commit do one thing, with a Conventional Commit message?
3. `git fetch`, `git switch chore/toolchain`, `rm -rf .venv`, `uv sync --locked`, then the four
   commands: does everything pass on your machine, not just the author's?
4. Is there a test that fails if `register` is wrong?

Merge with **Create a merge commit** (the five commits are all meaningful), delete the branch, then
`git switch main && git pull && git fetch --prune`.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `uv: command not found` | uv not installed or terminal not restarted | install, open a new terminal |
| `error: The lockfile ... needs to be updated` | `pyproject.toml` changed without relocking | `uv lock` (or `uv sync` locally), commit both files |
| `ModuleNotFoundError` on `python greetings.py` | ran outside `.venv` | `uv run python greetings.py` |
| `ModuleNotFoundError: greetings` in pytest | tests cannot see the root | `pythonpath = ["."]` (today), src layout (Session 4) |
| mypy: `Need type annotation for ...` | an empty list or `None` with no type | annotate: `registry: list[Student] = []` |
| ruff `--fix` changed more than expected | many auto-fixable rules | read `git diff` before committing, never commit blind |
| Windows: `rm -rf .venv` fails | not in Git Bash | open Git Bash, or delete the folder in the file explorer |

## Glossary

- **dependency group (`dev`)**: packages needed to develop the project, not to run it.
- **lockfile (`uv.lock`)**: exact versions of every package, direct and indirect. Committed.
- **pin**: one exact version (`pytest 9.1.1`). **Constraint**: an acceptable range (`>=9.1.1`).
- **`uv run`**: run a command inside the project's environment, syncing it first.
- **`--locked`**: refuse to change the lockfile; fail if it is out of date.
- **lint**: static analysis that finds likely mistakes without running the code.
- **type hint**: an annotation (`str`, `int | None`) that mypy checks and Python ignores at runtime.
- **fixture** (`capsys`, `tmp_path`): something pytest hands to a test that asks for it by name.
- **parametrize**: one test function, several inputs, one result per input.
