# Session 03 · Exercises: Environments and the Quality Toolchain

To do after the session, on your own. In class you equipped `greetings` with the guide. Here you
redo it without the guide on the small `desk-notes` repository of Session 2 (a `notes.py` that
prints numbered notes), on a branch `chore/quality-toolchain`. Each exercise ends with something you
paste in `answers.md`. Stop at `[BLOQUÉ?]` if stuck.

On macOS use `python3` outside `uv run`. On Windows use Git Bash.

## Exercise 1 · Constraint or pin? (paper first)

A `pyproject.toml` declares `dependencies = ["requests>=2.31"]`. The committed `uv.lock` contains
`requests` version `2.32.5`. The newest `requests` on PyPI is also `2.32.5`.

a. A teammate clones the repo six months from now, when `2.33.0` exists, and runs
   `uv sync --locked`. Which version do they get?
b. Same teammate, but `uv.lock` was never committed. Which version, and why is that a problem?
c. What do `requests==2.32.5`, `requests>=2.31` and `requests~=2.31` each accept?
d. Why should a library published on PyPI declare ranges rather than `==` pins, while an
   application like `desk-notes` relies on a lockfile?

## Exercise 2 · A uv project in your repository

1. Run `uv init --bare` and set `requires-python` to `">=3.12"`.
2. Add `ruff`, `mypy` and `pytest` as dev dependencies.
3. In `answers.md` note: the line `uv add --dev` wrote in `pyproject.toml` for `pytest`, and the exact
   `pytest` version pinned in `uv.lock`.
4. Make sure `.venv/` is gitignored, then commit `pyproject.toml` and `uv.lock`.

## Exercise 3 · Delete and rebuild

1. Save `uv pip freeze` to `before.txt` (outside the repo, or gitignored).
2. Delete `.venv/` entirely.
3. Rebuild with `uv sync --locked`, save `uv pip freeze` to `after.txt`, and `diff` the two.
4. Edit `pyproject.toml` by hand to add `"rich>=13"` to `dependencies`, without `uv add`. Run
   `uv sync --locked`. Paste the error and explain in one sentence what `--locked` protected you
   from. Then fix it properly (`uv lock`) or remove the line.

## Exercise 4 · requirements.txt for a pip-only colleague

1. Export the dependencies (no hashes, no project itself) to `requirements.txt`.
2. In another folder, with plain Python and no uv: create a venv, activate it, install from that
   file, run `pip list`.
3. Why is this file better exported from the lock than produced by `pip freeze`?

## Exercise 5 · Configure and run the tools

1. Add `[tool.ruff]` (line length 100), `[tool.ruff.lint]` (rules `E, F, I, B, UP, SIM, RUF`),
   `[tool.mypy]` (`strict = true`) and `[tool.pytest.ini_options]` (with `pythonpath = ["."]`) to
   `pyproject.toml`.
2. Refactor `notes.py` so that a function `format_notes(notes: list[str]) -> list[str]` returns the
   numbered lines (`"1. buy stamps"`, numbering from 1) and `main() -> None` prints the title
   `Desk notes` then those lines, under `if __name__ == "__main__":`. The output must not change.
3. Make `ruff format --check`, `ruff check` and `mypy` pass. Paste the summary line of each.

## Exercise 6 · Tests that can fail

In `tests/test_notes.py` write at least four tests, among them:

1. numbering starts at 1;
2. an empty list gives no line;
3. a `@pytest.mark.parametrize` test (one case per list length you choose);
4. `main()` prints the title first (use `capsys`).

For each test, break `notes.py` on purpose and check that this test turns red. Note in
`answers.md` the break you used for each.

## Exercise 7 · The toolchain PR

Push the branch, open the PR `chore: introduce quality toolchain`. Your partner reviews it on their
machine: `git switch` to the branch, `rm -rf .venv`, `uv sync --locked`, the four commands green,
`.venv/` absent from the diff. Merge with **Create a merge commit** once approved.

## Exercise 8 (bonus) · Let mypy find the bug

Add this function, with no test:

```python
def find_note(notes: list[str], word: str) -> str:
    for note in notes:
        if word in note:
            return note
```

Run mypy. Explain the error, then the runtime behaviour it predicts when no note matches. Fix the
function (two valid fixes with different return types) and update the annotation accordingly.

## `[BLOQUÉ?]`

Which exercise, exact command, full output, expected result. For uv problems add `uv --version`.
