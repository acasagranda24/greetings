# Session 04 · Follow-Along Guide: Automation, pre-commit, CI and the src Layout

**Course:** Python Environments & Engineering Workflows (MSA-DATI07-01) · MSc 1 · 2h

## What we build today

Session 3 ended with four commands to remember before every commit. People forget. Today the machine
remembers for you, and `greetings` becomes an installable project:

1. `pre-commit`: the checks run by themselves on every `git commit`.
2. The src layout: `greetings.py` becomes a package, installed in your environment, so tests run
   against what you ship.
3. Bash: we write shell today. A small script downloads the day's roster
   (a CSV of new students) and hands it to a new Python command that welcomes, registers and enrolls
   everyone in it.
4. CI (GitHub Actions): the same checks run on GitHub for every PR, and `main` refuses a merge
   until they are green.
5. Template: the repo is cleaned up (README, LICENSE, `.env.example`) and turned into a GitHub
   template repository, your starting point for the semester project.

Same four-part rhythm as before: **Predict**, **Run**, **You should see**, **Why**. Hashes, versions and
paths will differ on your machine. GitHub's own web pages (the Actions tab, the ruleset form) are not
shown here.

**End of session deliverable:** your `greetings` repository as a template repository, with
pre-commit installed, the src layout, the daily roster script, a CI workflow that is green on
`main` and required by the ruleset, a README and a LICENSE.

| Part | Topic | Mode |
|---|---|---|
| 0 | Where we stand | all together |
| 1 | pre-commit | all together |
| 2 | src layout | all together |
| | Break (15 min) | |
| 3 | Bash: the daily roster | all together, then pairs |
| 4 | CI with GitHub Actions | pairs |
| 5 | Template and wrap-up | all together |

On macOS type `python3` where a command needs plain `python`. On Windows use **Git Bash** for
everything, including the shell script of Part 3.

---

## Part 0 · Where we stand

You have the merged Session 3 toolchain on `main`. Check, and start the first branch of the day:

```bash
cd greetings
git switch main
git pull
uv sync --locked
uv run pytest -q
git switch -c chore/automation
```

```
.......                                                                  [100%]
7 passed in 0.01s
```

If `pytest` does not pass, stop and fix `main` first: today's tools refuse to commit on top of red.

---

## Part 1 · pre-commit

### 1.1 The idea

A **Git hook** is a script Git runs automatically at a given moment. The `pre-commit` hook runs just
before a commit is created and can refuse it. The tool called `pre-commit` manages those hooks
from one versioned file, so the whole team gets the same checks.

> **On the board:** `git commit` → pre-commit runs hooks on the staged files → all pass: commit is
> created. One fails: no commit, you fix and retry.

### 1.2 Install it and write the config

```bash
uv add --dev pre-commit
```

```
Resolved 24 packages in 221ms
...
 + pre-commit==4.6.2
 + pyyaml==6.0.3
 + virtualenv==21.14.5
```

Create `.pre-commit-config.yaml` at the root of the repo:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ["--maxkb=500"]
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.10
    hooks:
      - id: ruff-check
        args: ["--fix"]
      - id: ruff-format

  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run mypy
        language: system
        types: [python]
        pass_filenames: false
      - id: pytest
        name: pytest
        entry: uv run pytest -q
        language: system
        types: [python]
        pass_filenames: false
```

**Why two kinds of hooks:**

| Kind | Example | Where its code comes from |
|---|---|---|
| **remote** (`repo: https://...`, pinned by `rev`) | trailing whitespace, ruff | pre-commit downloads it into its own cache |
| **local** (`repo: local`) | mypy, pytest | your own `.venv`, through `uv run` |

mypy and pytest have to be local: they need your project's dependencies and your code. Set the
ruff `rev` to the same version as in `uv.lock` (`uv run ruff --version`, prefix it with `v`),
otherwise two ruffs disagree.

### 1.3 Activate it, run it on everything

**Predict:** the config exists. Will the next `git commit` already be checked?

No: hooks are installed per clone, with one command.

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

```
pre-commit installed at .git/hooks/pre-commit
```

```
[INFO] Installing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Once installed this environment will be reused.
...
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check yaml...........................................(no files to check)Skipped
check for added large files..............................................Passed
detect private key.......................................................Passed
ruff check...............................................................Passed
ruff format..............................................................Passed
mypy.....................................................................Passed
pytest...................................................................Passed
```

The first run downloads the remote hooks (a few seconds), later ones are instant. `Skipped` means no
staged file matched that hook's types (no YAML file yet).

```bash
git add pyproject.toml uv.lock .pre-commit-config.yaml
git commit -m "chore: add pre-commit hooks"
```

```
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check yaml...............................................................Passed
check for added large files..............................................Passed
detect private key.......................................................Passed
ruff check...........................................(no files to check)Skipped
ruff format..........................................(no files to check)Skipped
mypy.................................................(no files to check)Skipped
pytest...............................................(no files to check)Skipped
[chore/automation 7abac79] chore: add pre-commit hooks
 3 files changed, 179 insertions(+)
 create mode 100644 .pre-commit-config.yaml
```

The commit went through the hooks. The Python hooks were skipped because no `.py` file
was in this commit.

### 1.4 A commit that gets refused

Add a small method to the class in `greetings.py` and write it sloppily: put `import os` as the
very first line, add the method below, and put trailing spaces after the `return`:

```python
def initials(self) -> str:
    return f"{self.first_name[0]}{self.last_name[0]}"
```

(Two spaces after `return`, three trailing spaces at the end.)

**Predict:** which hooks will fail? Will the commit be created?

```bash
git commit -am "feat: add initials"
```

```
trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

Fixing greetings.py

fix end of files.........................................................Passed
ruff check...............................................................Failed
- hook id: ruff-check
- files were modified by this hook

Found 1 error (1 fixed, 0 remaining).

ruff format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted

mypy.....................................................................Passed
pytest...................................................................Passed
```

No commit was created. The hooks rewrote your file, so look at what they did.

```bash
git status --short
git diff
```

```
 M greetings.py
```

```
@@ -14,6 +14,9 @@ class Student:
         registry.append(self)
         return self.student_id

+    def initials(self) -> str:
+        return f"{self.first_name[0]}{self.last_name[0]}"
+
     def enroll(self, classroom: str) -> str:
```

The unused `import os`, the double space and the trailing spaces are gone. Re-add and commit again:

```bash
git add greetings.py
git commit -m "feat: add initials"
```

```
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
ruff check...............................................................Passed
ruff format..............................................................Passed
[chore/automation 7bd95de] feat: add initials
 1 file changed, 3 insertions(+)
```

**Why:** two kinds of failure.

- "files were modified by this hook" (whitespace, ruff, format): the tool fixed it, you only
  `git add` the result and commit again.
- A hook that only reports (mypy, pytest): you must fix the code yourself. Try it later:
  change `len(registry) + 1` into `len(registry)` and commit; the `pytest` hook prints the red tests
  and the commit is refused.

> **Rule.** `git commit --no-verify` skips every hook. Using it is how a broken commit ends up on a
> branch; the CI of Part 4 will catch it again, but do not make a habit of it.

> **If it goes wrong:**
> - The hooks do nothing: you skipped `uv run pre-commit install` in this clone.
> - `uv: command not found` inside the hook (Windows/macOS GUI clients): commit from the terminal.
> - `[WARNING] Unstaged files detected` followed by a restore message: harmless; pre-commit set your
>   other changes aside while checking the staged ones.

---

## Part 2 · The src layout

### 2.1 Why

Today `greetings.py` sits at the root and the tests only work thanks to the `pythonpath = ["."]` hack
of Session 3. That is the flat layout, and it has a flaw: whatever is in the current folder can
be imported, so your tests can pass without the package ever being installed. A project that
passes locally but cannot be installed is a classic broken release.

The src layout puts the code in `src/<package>/`. Now the only way to import it is to install
it, so the tests run against what a user will actually get.

```
greetings/
├── pyproject.toml
├── src/greetings/
│   ├── __init__.py      # what the package exposes: Student
│   ├── __main__.py      # makes `python -m greetings` work
│   ├── cli.py           # main()
│   ├── student.py       # the Student class
│   └── py.typed         # marker: "this package ships type hints"
└── tests/
    └── test_student.py
```

> **On the board:** the flat layout (`greetings.py`, `tests/`) and the src layout side by side, with
> the arrow "import" going into `src/` only through "install".

### 2.2 Move the code, keeping history

```bash
mkdir -p src/greetings
git mv greetings.py src/greetings/student.py
git status --short
```

```
R  greetings.py -> src/greetings/student.py
```

`git mv` records a rename, so `git log --follow` keeps the history of the file.

Now split. In `src/greetings/student.py` keep only the `Student` class: delete `main()` and the
`if __name__` block at the bottom. Then create the other files:

`src/greetings/cli.py`:

```python
from greetings.student import Student


def main() -> None:
    registry: list[Student] = []
    student = Student("Tuka", "Bade", "tuka@albertschool.com")
    student.register(registry)
    print(student.welcome())
    print(f"Registered as student #{student.student_id}")
    print(f"Confirmation sent to {student.email}")
    print(student.enroll("MSc 1 Data"))
```

`src/greetings/__init__.py`:

```python
from greetings.student import Student

__all__ = ["Student"]
```

`src/greetings/__main__.py`:

```python
from greetings.cli import main

main()
```

and an empty `src/greetings/py.typed` (`touch src/greetings/py.typed`).

### 2.3 Tell pyproject how to build and where things are

Three edits to `pyproject.toml`:

```toml
[project.scripts]
greetings = "greetings.cli:main"
```

(after `dependencies = []`, before `[dependency-groups]`), then a build backend. Ask uv which block
fits your uv version rather than copying one from the internet:

```bash
uv init --lib ../greetings-scratch
cat ../greetings-scratch/pyproject.toml
rm -rf ../greetings-scratch
```

Copy its `[build-system]` block (it looks like the following, your version number will differ):

```toml
[build-system]
requires = ["uv_build>=0.12.23,<0.13.0"]
build-backend = "uv_build"
```

Finally, in `[tool.mypy]` set `files = ["src", "tests"]`, and in `[tool.pytest.ini_options]`
delete the `pythonpath = ["."]` line: the hack is no longer needed. In `tests/test_student.py`
change the import line to:

```python
from greetings import Student
from greetings.cli import main
```

### 2.4 Install and check

**Predict:** `uv run pytest` before `uv sync`: will it find `greetings`?

```bash
uv sync
uv run greetings
uv run python -m greetings | head -1
uv run pytest -q
uv pip list | grep -i greetings
```

```
Resolved 24 packages in 1ms
Checked 23 packages in 0.44ms
```

```
Welcome to Albert School, Tuka!
Registered as student #1
Confirmation sent to tuka@albertschool.com
Tuka Bade joins MSc 1 Data.
```

```
Welcome to Albert School, Tuka!
```

```
.......                                                                  [100%]
7 passed in 0.01s
```

```
greetings         0.1.0   /path/to/greetings
```

The last line is the proof: `greetings` is now an installed package in `.venv`. The path next to
it means it is editable: the environment points to your `src/` folder, so a change in the source is
visible without reinstalling.

`uv run greetings` works because of `[project.scripts]`: pip and uv create a `greetings` command that
calls `greetings.cli:main`.

Commit. The pre-commit hooks run the whole toolchain for you:

```bash
git add -A
git commit -m "refactor: move to the src layout"
```

```
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check added large files..............................................Passed
...
ruff check...............................................................Passed
ruff format..............................................................Passed
mypy.....................................................................Passed
pytest...................................................................Passed
[chore/automation 71f6296] refactor: move to the src layout
 8 files changed, 28 insertions(+), 18 deletions(-)
 create mode 100644 src/greetings/__init__.py
 create mode 100644 src/greetings/__main__.py
 create mode 100644 src/greetings/cli.py
 create mode 100644 src/greetings/py.typed
 rename greetings.py => src/greetings/student.py (67%)
```

```bash
git push -u origin chore/automation
```

Open the PR `chore: add pre-commit hooks and the src layout`, partner reviews (checklist: three
commits, each atomic; `git mv` shown as a rename in *Files changed*; `pythonpath` hack gone; checks
pass on the reviewer's machine after `rm -rf .venv && uv sync --locked && uv run pre-commit run
--all-files`), **Create a merge commit**, delete the branch, `git switch main && git pull`.

> **If it goes wrong:**
> - `ModuleNotFoundError: greetings` in pytest: you did not run `uv sync` after editing
>   `[build-system]`, or `uv run` ran with a stale `.venv`. `rm -rf .venv && uv sync`.
> - A copied project folder fails with strange paths: a `.venv` cannot be moved or copied
>   (its scripts hold absolute paths). Delete it and `uv sync`.
> - mypy: `Skipping analyzing "greetings"`: `py.typed` is missing.

---

## Break (15 min)

---

## Part 3 · Bash: the daily roster

Every morning the school publishes the list of new students as a CSV file. We want one command
that downloads it and registers everybody. Two parts: a Python command that reads a roster
(we write it together), and a Bash script that fetches it and calls Python.

```bash
git switch -c feat/daily-roster
```

### 3.1 The Python side: `greetings roster <file>`

*I give you these files to paste. We read them together and run the tests; save your typing for
the Bash script of 3.2.*

`src/greetings/roster.py`:

```python
import csv
from pathlib import Path

from greetings.student import Student


def load_roster(path: Path) -> list[tuple[Student, str]]:
    """Read a roster CSV: one (student, classroom) pair per row."""
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            (Student(row["first_name"], row["last_name"], row["email"]), row["classroom"])
            for row in csv.DictReader(handle)
        ]


def process_roster(path: Path) -> list[Student]:
    """Welcome, register and enroll every student of a roster file."""
    registry: list[Student] = []
    for student, classroom in load_roster(path):
        student.register(registry)
        print(student.welcome())
        print(student.enroll(classroom))
    print(f"{len(registry)} students registered")
    return registry
```

`src/greetings/cli.py` becomes (the old `main` is renamed `demo`):

```python
import sys
from pathlib import Path

from greetings.roster import process_roster
from greetings.student import Student


def demo() -> None:
    registry: list[Student] = []
    student = Student("Tuka", "Bade", "tuka@albertschool.com")
    student.register(registry)
    print(student.welcome())
    print(f"Registered as student #{student.student_id}")
    print(f"Confirmation sent to {student.email}")
    print(student.enroll("MSc 1 Data"))


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    if len(args) == 2 and args[0] == "roster":
        process_roster(Path(args[1]))
    else:
        demo()
```

Update `tests/test_student.py`: `from greetings.cli import main` still works (`main()` with no
argument runs the demo). Add `tests/test_roster.py`:

```python
from pathlib import Path

import pytest

from greetings.cli import main
from greetings.roster import load_roster, process_roster

CSV = (
    "first_name,last_name,email,classroom\n"
    "Ada,Lovelace,ada@albertschool.com,MSc 1 Data\n"
    "Alan,Turing,alan@albertschool.com,MSc 1 AI\n"
)


@pytest.fixture
def roster_file(tmp_path: Path) -> Path:
    path = tmp_path / "2026-10-04.csv"
    path.write_text(CSV, encoding="utf-8")
    return path


def test_load_roster_reads_one_pair_per_row(roster_file: Path) -> None:
    pairs = load_roster(roster_file)
    assert [(s.first_name, room) for s, room in pairs] == [
        ("Ada", "MSc 1 Data"),
        ("Alan", "MSc 1 AI"),
    ]


def test_process_roster_numbers_students_in_file_order(roster_file: Path) -> None:
    registry = process_roster(roster_file)
    assert [s.student_id for s in registry] == [1, 2]


def test_cli_roster_prints_a_summary(roster_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    main(["roster", str(roster_file)])
    assert capsys.readouterr().out.splitlines()[-1] == "2 students registered"
```

`tmp_path` is a pytest fixture giving each test its own empty temporary folder: no test ever touches
your real files.

Create the stand-in for the school's server: a folder `fake_server/` containing
`fake_server/2026-10-04.csv`:

```
first_name,last_name,email,classroom
Ada,Lovelace,ada@albertschool.com,MSc 1 Data
Grace,Hopper,grace@albertschool.com,MSc 1 Data
Alan,Turing,alan@albertschool.com,MSc 1 AI
```

```bash
uv run pytest -q
uv run greetings roster fake_server/2026-10-04.csv
```

```
..........                                                               [100%]
10 passed in 0.05s
```

```
Welcome to Albert School, Ada!
Ada Lovelace joins MSc 1 Data.
Welcome to Albert School, Grace!
Grace Hopper joins MSc 1 Data.
Welcome to Albert School, Alan!
Alan Turing joins MSc 1 AI.
3 students registered
```

```bash
git add -A
git commit -m "feat: add a roster command"
```

(If ruff reformats a line when you commit, `git add` the result and commit again, as in Part 1.4.)

### 3.2 The Bash side, one small step at a time

We write `scripts/daily_roster.sh` in six runs. After every step we run it. If something breaks,
the culprit is the last line we added.

On every OS we start the script with `bash scripts/daily_roster.sh`. No `chmod`, no `./`, no
difference between macOS, Linux and Git Bash.

```bash
mkdir scripts
```

**Step 1: it runs.** Create `scripts/daily_roster.sh`:

```bash
#!/usr/bin/env bash
echo "daily roster"
```

```bash
bash scripts/daily_roster.sh
```

```
daily roster
```

The first line (the **shebang**) says which program interprets the file. `#!/usr/bin/env bash`
finds `bash` wherever it is installed.

**Step 2: a variable with a default.** Replace the file with:

```bash
#!/usr/bin/env bash
day="${1:-$(date -d yesterday +%F 2>/dev/null || date -v-1d +%F)}"
echo "day: $day"
```

```bash
bash scripts/daily_roster.sh
bash scripts/daily_roster.sh 2026-10-04
```

```
day: 2026-10-04
day: 2026-10-04
```

(The first run prints yesterday's date, whatever day you run it.) Three things to read out loud:

- `$1` is the first argument. `${1:-default}` means "`$1` if given, otherwise the default".
- `$(command)` runs a command and substitutes its output.
- `date -d yesterday` is the **GNU** spelling (Linux, Git Bash), `date -v-1d` is the **BSD** one
  (macOS). `A || B` tries `A`, and runs `B` if `A` fails. `2>/dev/null` hides the error of the
  failed attempt.

**Step 3: stop at the first error.** Add one line at the top and mistype the variable in the last
line (`$dya`):

```bash
#!/usr/bin/env bash
set -euo pipefail

day="${1:-$(date -d yesterday +%F 2>/dev/null || date -v-1d +%F)}"
echo "day: $dya"
```

```bash
bash scripts/daily_roster.sh 2026-10-04; echo "exit code: $?"
```

```
scripts/daily_roster.sh: line 5: dya: unbound variable
exit code: 1
```

Fix the typo (`$day`) and run again. **Why `set -euo pipefail`:**

| Flag | Effect |
|---|---|
| `-e` | stop at the first command that fails |
| `-u` | an unset variable is an error, not an empty string |
| `-o pipefail` | in `a \| b`, a failure in `a` counts |

Without them Bash keeps going after an error. A script that fails silently on the download and
then processes an empty file is worse than one that stops.

**Step 4: configuration from `.env`, secrets never in the script.** Replace the file with:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -f .env ]]; then
    set -a
    source .env
    set +a
fi

: "${ROSTER_URL:?ROSTER_URL is not set (see .env.example)}"
: "${ROSTER_TOKEN:?ROSTER_TOKEN is not set (see .env.example)}"

day="${1:-$(date -d yesterday +%F 2>/dev/null || date -v-1d +%F)}"
echo "would fetch ${ROSTER_URL}/${day}.csv"
```

- `cd "$(dirname "$0")/.."` goes to the repo root, wherever you launched the script from.
  `$0` is the script's own path.
- `source .env` runs the file's `KEY=value` lines in the current shell; `set -a` marks them as
  exported, `set +a` stops doing that.
- `: "${VAR:?message}"` is the idiom for "this variable is required": if it is missing or empty,
  stop with the message.

Create `.env.example` (committed, it documents the variables without secrets):

```
ROSTER_URL=http://localhost:8000
ROSTER_TOKEN=change-me
```

**Predict:** you have no `.env` yet. What happens?

```bash
bash scripts/daily_roster.sh 2026-10-04
```

```
scripts/daily_roster.sh: line 12: ROSTER_URL: ROSTER_URL is not set (see .env.example)
```

Now create your own `.env`, which Git ignores (it has been in your `.gitignore` since Session 1):

```bash
cat .env.example >> .env
bash scripts/daily_roster.sh 2026-10-04
```

```
would fetch http://localhost:8000/2026-10-04.csv
```

**Step 5: download, safely.** In a second terminal, start the stand-in server (leave it running):

```bash
cd greetings
uv run python -m http.server 8000 --directory fake_server
```

Back in the first terminal, add `data/raw/` to `.gitignore` (downloaded data is never committed),
then replace the end of the script (from the `day=` line):

```bash
# GNU date (Linux, Git Bash) and BSD date (macOS) spell "yesterday" differently.
day="${1:-$(date -d yesterday +%F 2>/dev/null || date -v-1d +%F)}"
target="data/raw/${day}.csv"
mkdir -p data/raw

if [[ -s "$target" ]]; then
    echo "already downloaded: $target"
else
    curl --fail --silent --show-error \
        -H "Authorization: Bearer ${ROSTER_TOKEN}" \
        -o "${target}.part" \
        "${ROSTER_URL}/${day}.csv"
    mv "${target}.part" "$target"
    echo "saved: $target ($(wc -l < "$target") lines)"
fi
```

```bash
bash scripts/daily_roster.sh 2026-10-04
bash scripts/daily_roster.sh 2026-10-04
bash scripts/daily_roster.sh 2026-10-01; echo "exit code: $?"
ls data/raw
```

```
saved: data/raw/2026-10-04.csv (4 lines)
already downloaded: data/raw/2026-10-04.csv
curl: (22) The requested URL returned error: 404
exit code: 22
2026-10-04.csv
```

Read the script like a reviewer:

- `[[ -s "$target" ]]` is true when the file exists and is not empty. Running the script twice
  does not download twice: it is idempotent.
- `curl --fail` makes an HTTP error (404, 500) a failure; without it, curl would save the
  error page as if it were data. `--show-error --silent` keeps the output quiet except for errors.
  The header `Authorization: Bearer ...` is how an API receives the token.
- We write to `...csv.part` and `mv` it at the end: if the download breaks half-way, the final
  filename never holds a partial file. (See for yourself: after the 404, `ls data/raw` shows no
  `.part`.)
- **Quote your variables** (`"$target"`). Unquoted, a path with a space becomes two arguments.

**Step 6: hand over to Python.** Add one last line at the end of the script, then run it:

```bash
uv run greetings roster "$target"
```

```bash
bash scripts/daily_roster.sh 2026-10-04
```

```
already downloaded: data/raw/2026-10-04.csv
Welcome to Albert School, Ada!
Ada Lovelace joins MSc 1 Data.
Welcome to Albert School, Grace!
Grace Hopper joins MSc 1 Data.
Welcome to Albert School, Alan!
Alan Turing joins MSc 1 AI.
3 students registered
```

Stop the server in the second terminal (`Ctrl+C`). Add the header comments at the top of the script,
right after the shebang (the Usage line documents the script):

```bash
# Download the roster of one day and register its students.
# Usage: bash scripts/daily_roster.sh [YYYY-MM-DD]     (default: yesterday)
```

### 3.3 Two pieces of hygiene

**Line endings.** Windows editors save text with `CRLF` line endings; Bash then reads a stray `\r`
at the end of each line and fails with errors like `$'\r': command not found`. Prevent it with a
one-line `.gitattributes` at the root:

```
*.sh text eol=lf
```

If a script already has CRLF: `sed -i 's/\r$//' scripts/daily_roster.sh` (in Git Bash).

**shellcheck.** A linter for shell scripts, like ruff for Python. It will run in CI in Part 4. If you
have it installed: `shellcheck scripts/daily_roster.sh`; without installing:
`uv tool run --from shellcheck-py shellcheck scripts/daily_roster.sh`. It points out one thing:

```
In scripts/daily_roster.sh line 10:
    source .env
           ^--^ SC1091 (info): Not following: .env was not specified as input
```

It cannot follow a file that does not exist in the repo. Tell it you know, with a comment on the line
above: `# shellcheck disable=SC1091`. Run it again: no output, exit code 0.

### 3.4 Commit, PR

```bash
git add scripts .env.example .gitignore .gitattributes
git commit -m "feat: add the daily roster script"
git push -u origin feat/daily-roster
```

Open the PR `feat: add a roster command and the daily roster script`. Reviewer checklist:

1. No `.env`, no `data/raw/` content in the diff (`git diff --stat main...`).
2. `.env.example` has placeholders only, no real tokens.
3. Run it yourself: second terminal with the stand-in server, then
   `bash scripts/daily_roster.sh 2026-10-04`. Then the 404 case: does it stop with a non-zero
   exit code?

Merge with **Create a merge commit**, then `git switch main && git pull && git fetch --prune`.

> **If it goes wrong:**
> - `syntax error near unexpected token` or `$'\r': command not found`: CRLF line endings
>   (see 3.3).
> - `date: illegal option -- d` on macOS: you removed the `|| date -v-1d +%F` part.
> - `curl: (7) Failed to connect`: the stand-in server is not running in the second terminal.
> - `ROSTER_URL: ... is not set`: no `.env` in the repo root, or you wrote `ROSTER_URL = http...`
>   with spaces around `=` (Bash does not allow them).
> - `uv: command not found` inside the script on Windows: start Git Bash again after installing uv.

---

## Part 4 · CI with GitHub Actions

pre-commit runs on your machine, and `--no-verify` exists. CI (continuous integration) runs
the same checks on a clean GitHub machine for every push and every PR, and nobody can skip it.

```bash
git switch -c ci/github-actions
mkdir -p .github/workflows
```

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - uses: astral-sh/setup-uv@v10
        with:
          enable-cache: true

      - name: Install the locked environment
        run: uv sync --locked

      - name: Format check
        run: uv run ruff format --check .

      - name: Lint
        run: uv run ruff check .

      - name: Type-check
        run: uv run mypy

      - name: Tests
        run: uv run pytest

      - name: Shell scripts
        run: shellcheck scripts/*.sh
```

Read it top to bottom:

- `on:` runs on every push to `main` and on every pull request.
- A **job** (`quality`) runs on a fresh Ubuntu machine, as a list of **steps**.
- `uv sync --locked` is the same command as in Session 3: the CI machine builds the exact
  environment of your lockfile, and fails if the lockfile is stale.
- The same four checks as pre-commit, plus `shellcheck` (preinstalled on GitHub's Ubuntu images).
- Versions after `@` pin the actions. Check the current major version of each action if GitHub
  warns that it is deprecated.

**CI secrets.** Never write a token in the YAML. Store it in **Settings > Secrets and variables >
Actions** and read it as `${{ secrets.NAME }}`. Our workflow needs none.

Add the README and LICENSE now too (Part 5 explains them), then commit and push:

```bash
git add .github
git commit -m "ci: add GitHub Actions workflow"
```

`README.md`:

````markdown
# greetings

Welcome desk of Albert School: welcome, register and enroll new students.

## Setup

```bash
uv sync --locked
uv run pre-commit install
```

## Use

```bash
uv run greetings                                  # demo
uv run greetings roster path/to/roster.csv        # a day's roster
bash scripts/daily_roster.sh [YYYY-MM-DD]         # download then register (needs .env)
```

Copy `.env.example` to `.env` and fill it in. `.env` is never committed.

## Check

```bash
uv run ruff format --check . && uv run ruff check . && uv run mypy && uv run pytest
```
````

`LICENSE`: the text of the MIT licence with your name and the year (copy it from
https://choosealicense.com/licenses/mit/). Without a licence, nobody may legally reuse your code.

```bash
git add README.md LICENSE
git commit -m "docs: add README and LICENSE"
git push -u origin ci/github-actions
```

Open the PR `ci: add GitHub Actions workflow`. On the PR page, at the bottom, a **Checks** box appears:
a yellow dot while the workflow runs, then **All checks have passed** and a green tick. Click
**Details** to read each step's log: this is where you look when it goes red.

### Make the check required

In your ruleset (**Settings > Rules > Rulesets > protect main**) enable **Require status checks to
pass**, **Add checks**, and select **`quality`** (the job name; it only appears in the list after the
workflow has run once, which is why we opened the PR first). Save.

**Predict:** if CI is red, can the PR still be merged?

No: the merge button stays disabled with "Required statuses must pass". The three guards are now
stacked: pre-commit (your machine, skippable), CI (GitHub, not skippable), ruleset (makes CI
mandatory).

Reviewer approves, **Create a merge commit**, delete the branch, then run:

```bash
git switch main
git pull
git fetch --prune
git log --oneline --graph -12
```

> **If it goes wrong:**
> - Red `Install the locked environment`: you changed `pyproject.toml` without committing the new
>   `uv.lock`. `uv lock`, commit, push.
> - Red `shellcheck`: read the code in the message (`SC2086`...), open
>   `https://www.shellcheck.net/wiki/SC2086`, fix, push on the same branch.
> - The workflow never starts: the file is not in `.github/workflows/` (singular `.github`,
>   plural `workflows`), or the YAML indentation is wrong (`check-yaml` catches it).
> - Green on your laptop, red on CI: the usual suspect is a file you have locally and did not commit
>   (`git status --ignored`), or a missing dependency in `pyproject.toml`.

---

## Part 5 · Template repository and wrap-up

A **template repository** is a repository GitHub can copy as a fresh start (without the history).
That suits a semester project: everyone starts from the same checked toolchain.

On GitHub: **Settings > General**, tick **Template repository**. A green **Use this template**
button now sits on the repo page.

```bash
gh repo create my-new-project --template <your-username>/greetings --public --clone
```

or the button. Your teammates (and you, next semester) get: `src/` layout, locked environment,
pre-commit config, CI workflow, README, LICENSE, `.env.example`, `.gitattributes`, `.gitignore`.

### Template hygiene checklist

Before ticking the box, check, on a fresh clone:

```bash
git clone git@github.com:<your-username>/greetings.git /tmp/greetings-check
cd /tmp/greetings-check
uv sync --locked
uv run pre-commit run --all-files
```

All green from a clean clone is what the template promises. Also check that
`git log --all --oneline -- .env` is empty (no secret in history) and that `.env.example`
contains only placeholders.

### Three files the project brief also asks for

```bash
uv python pin 3.12                                          # writes .python-version
uv export --no-dev --no-hashes -o requirements.txt          # exported from the lock, never edited by hand
```

and `.github/pull_request_template.md` with the four headings used since Session 2 (What, Why, How
to check, Checklist). Commit them in one `chore:` commit. `requirements.txt` is regenerated every time
`uv.lock` changes; the project has no runtime dependency yet, so the file only contains `-e .`.

### The graph of your day

```bash
git log --oneline --graph --all
```

It should show three merged PRs (automation, daily roster, CI), each a merge commit with its
atomic commits on the side, on top of Session 3's toolchain.

### Deliverable

Hand in the URL of the template repository and the output of `git log --oneline --graph`. The
README, the green CI on `main` and the required status check in the ruleset are what we look at.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Hooks never run | `pre-commit install` not run in this clone | `uv run pre-commit install` |
| Commit refused, file changed | a fixer hook rewrote it | `git add` the file, commit again |
| Commit refused, nothing changed | mypy or pytest failed | read the output, fix the code |
| `ModuleNotFoundError: greetings` | package not installed | `uv sync` (and rebuild `.venv` if copied) |
| `$'\r': command not found` | CRLF line endings in the script | `sed -i 's/\r$//' file`, add `.gitattributes` |
| `unbound variable` | `set -u` caught a typo or a missing variable | fix the name, check `.env` |
| `curl: (22) ... 404` | no roster for that day | pass a valid date; the script stopped correctly |
| `curl: (7) Failed to connect` | stand-in server not running | start it in a second terminal |
| CI red on `uv sync --locked` | stale lockfile | `uv lock`, commit `uv.lock` |
| Check `quality` not in the ruleset list | workflow never ran | open a PR first, then add the check |

## Glossary

- **Git hook**: a script Git runs at a given moment (`pre-commit`: before a commit is created).
- **pre-commit**: a tool that manages hooks from `.pre-commit-config.yaml`.
- **remote hook / local hook**: code downloaded by pre-commit / code from your own environment.
- **src layout**: code in `src/<package>/`, so it must be installed to be imported.
- **editable install**: the environment points at your source; edits apply without reinstalling.
- **`py.typed`**: marker file saying the package ships type hints.
- **shebang**: first line of a script naming its interpreter.
- **`set -euo pipefail`**: stop on error, on unset variables, and on failures inside pipes.
- **idempotent**: running it twice has the same effect as running it once.
- **CI (continuous integration)**: automatic checks on a clean machine for every push and PR.
- **workflow / job / step**: GitHub Actions' file / machine run / command in a run.
- **required status check**: a check that must be green before the merge button works.
- **template repository**: a repository GitHub can copy as a fresh start, without its history.
