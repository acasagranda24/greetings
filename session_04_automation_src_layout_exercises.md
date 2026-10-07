# Session 04 · Exercises: Automation, pre-commit, CI and the src Layout

To do after the session, on your own and with your partner. In class you automated `greetings`
with the guide. Here you redo it without the guide on `desk-notes` (your Session 3 exercise
repository: `notes.py`, tests, uv, toolchain merged). One branch and one PR per exercise, reviewed
by your partner. Answers in `answers.md`. Stop at `[BLOQUÉ?]` if stuck.

On macOS use `python3` outside `uv run`. On Windows use Git Bash for everything, scripts included.

## Exercise 1 · pre-commit, and watch it say no

1. `uv add --dev pre-commit`, then create `.pre-commit-config.yaml` with: `trailing-whitespace`,
   `end-of-file-fixer`, `check-yaml`, `check-added-large-files`, `detect-private-key` (from
   `pre-commit/pre-commit-hooks`), `ruff-check --fix` and `ruff-format` (from
   `astral-sh/ruff-pre-commit`), and local hooks for mypy and pytest running through `uv run`.
2. `uv run pre-commit install`, then `uv run pre-commit run --all-files` until everything is green.
3. Add `import os` at the top of `notes.py` and trailing spaces at the end of a line. Try to commit.
   Paste the output in `answers.md`.
4. Was the commit created? What changed in your working directory, and what do you do next?
5. Why are mypy and pytest `local` hooks and not remote ones?

## Exercise 2 · Predict which hooks run (paper first)

With the configuration of Exercise 1, predict for each commit which hooks show `Passed`, `Failed`
or `Skipped`, then check:

a. A commit that only changes `README.md`.
b. A commit that only changes `pyproject.toml`.
c. A commit that adds a file `key.pem` starting with `-----BEGIN RSA PRIVATE KEY-----`.

## Exercise 3 · CI on every push and PR

1. Create `.github/workflows/ci.yml`: triggers on push to `main` and on pull requests; one job
   `quality` on `ubuntu-latest`; checkout, `astral-sh/setup-uv` (with cache), `uv sync --locked`,
   then the four tools (formatter in `--check` mode).
2. Open the PR, watch the run in the **Actions** tab and on the PR. Merge when green.
3. Add `quality` as a required status check in the `main` ruleset.
4. Open a PR that breaks one test on purpose, committed with `--no-verify` so the local hook does
   not stop it. Paste the link to the red run and describe the merge button. Close without merging.
5. Give two reasons the CI check is needed even though everyone has pre-commit installed.

## Exercise 4 · Migrate to the src layout

1. Before migrating: from the repository root, with the venv not activated and without
   `uv run`, run `python -c "import notes"`. Note what happens and why it will be the same for a
   package.
2. On `refactor/src-layout`, create the package `desk_notes` in `src/` with `git mv`: the function
   `format_notes` goes in `src/desk_notes/notes.py`, a `main(argv: list[str] | None = None) -> None`
   in `cli.py` (no argument: print the three default notes; one argument: read the notes from that
   text file, one per line), plus `__init__.py`, `__main__.py` and an empty `py.typed`.
3. Add `[build-system]` (copy the block from `uv init --lib` in a scratch folder) and a console
   script `desk-notes = "desk_notes.cli:main"`. Remove `pythonpath = ["."]` from the pytest config.
   Update test imports and the `files` setting of mypy.
4. `uv sync`, then `uv run desk-notes`, `uv run python -m desk_notes` and
   `uv pip list | grep desk-notes`. Paste the outputs.
5. `git log --follow --oneline src/desk_notes/notes.py`: what does `--follow` show and why did
   `git mv` matter?
6. Add a test where `main([path])` reads a file created with `tmp_path`.

## Exercise 5 · Break the package on purpose

On a throwaway branch rename the folder `src/desk_notes/` to `src/desknotes/` (folder only) and run
`uv sync` then `uv run pytest`. Paste the errors. Explain why the flat layout would let the
equivalent mistake pass, and what the first person to `pip install` your project would get. Delete
the branch.

## Exercise 6 · A Bash script of your own

Write `scripts/daily_notes.sh`, building it in steps and running it after each one (shebang,
default date, `set -euo pipefail`, `.env`, download, hand over to Python):

1. It takes an optional date (default: yesterday, working on macOS and Linux/Git Bash).
2. It reads `NOTES_URL` from `.env` and stops with a clear message when it is missing.
3. It downloads `${NOTES_URL}/<date>.txt` with `curl --fail` to `data/raw/<date>.txt`, through a
   `.part` file, and does nothing when the file is already there.
4. It then runs `uv run desk-notes data/raw/<date>.txt`.

Serve the files from a `fake_server/` folder containing `2026-10-04.txt` (two or three lines) with
`uv run python -m http.server 8001 --directory fake_server`.

Commit `.env.example`, ignore `data/raw/` and `.env`, add `.gitattributes` with `*.sh text eol=lf`.
In `answers.md` paste: the first run, the second run, a run with a date that does not exist (with its
exit code) and the output of `shellcheck`. Explain what `--fail` and the `.part` file protect you from.

## Exercise 7 · Make it a template

1. Add `README.md` (setup in three commands, usage, checks), a `LICENSE` (MIT), and add `shellcheck
   scripts/*.sh` as a step of your CI.
2. Merge, check that CI is green on `main`, then tick **Template repository** in the settings.
3. Your partner creates a new repository from your template, clones it and follows only your
   README. Every step they had to guess is a README bug: fix it in a PR.

## Exercise 8 (bonus) · The daily workflow

Write `.github/workflows/daily.yml` that runs your script every morning at 06:00 UTC (`schedule:`
with a cron expression) with `NOTES_URL` taken from the repository's Actions secrets. Do not merge
it unless you have a working endpoint. In `answers.md`: why can you never write the URL or a token
directly in the YAML?

## `[BLOQUÉ?]`

Which exercise, exact command, full output, expected result. For CI problems paste the link to the
failing run and the name of the failing step. For script problems add `bash --version` and
`file scripts/daily_notes.sh`.
