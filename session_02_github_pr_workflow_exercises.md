# Session 02 · Exercises: The GitHub Pull-Request Workflow

To do after the session, on your own and with your partner. In class you followed the guide on
the `greetings` repository. Here you repeat the loop without the guide, on a new repository, so
you cannot copy anything from class.

Self-contained. Terminal and browser. Answers go in `answers.md`. Stop at `[BLOQUÉ?]` if stuck.
On macOS use `python3` instead of `python`. On Windows use Git Bash.

## Exercise 1 · A second repository, from scratch

1. Create a local folder `desk-notes/` with a `.gitignore` (ignoring `.env` and `__pycache__/`) and a
   file `notes.py` that prints `Desk notes`. Two commits, Conventional Commit messages.
2. Create an empty GitHub repository `desk-notes` and push with `push -u`.
3. Paste the output of `git status -sb` in `answers.md` and explain what `main...origin/main` means.
4. Which of your two SSH key files would be a security incident in a commit, and why is the other one
   harmless?

## Exercise 2 · fetch is not pull

1. On GitHub, edit `README.md` (create it in the browser if needed) and commit to `main`.
2. Locally, without fetching, run `git status -sb`. Write down what it says.
3. Run `git fetch`, then `git status -sb`, then `git log --oneline --graph --all`.
4. Explain in `answers.md` why the two outputs differ. Then `git pull`.

## Exercise 3 · Protect main

1. Add your partner as a collaborator. Create a ruleset on `main`: block force pushes, restrict
   deletions, require a pull request with one approval, dismiss stale approvals, empty bypass list.
2. Commit on `main` locally and try to push. Paste the rejection in `answers.md`.
3. Move that commit onto a branch and put `main` back where GitHub is, without losing the work.

## Exercise 4 · Three PRs, three merge strategies

In `desk-notes`, your partner reviews each PR (and you review theirs in their repository).

**PR A (rebase and merge).** Branch `docs/pr-template`: add `.github/pull_request_template.md` with
What / Why / How to check / Checklist. One clean commit.

**PR B (squash).** Branch `feat/count`: make `notes.py` read a list of three notes and print how many
there are. At least three commits, one of them a `wip`. Squash with a Conventional Commit
PR title.

**PR C (merge commit, with a review round).** Branch `feat/numbering`: print the notes numbered. Your
partner must **request changes** at least once with a concrete remark. Address it in a second commit
on the same branch, get the approval, merge with **Create a merge commit**.

After each merge: delete the branch on GitHub, `git switch main && git pull`, `git fetch --prune`,
delete it locally.

In `answers.md` paste `git log --oneline --graph` of `main` and, per PR, say which commit(s) it
produced and why the graph looks that way.

## Exercise 5 · A conflict through a PR

1. You and your partner each open a branch from the same tip of `main`, both changing the line
   that prints `Desk notes`, differently.
2. Merge the first PR. The second now says "This branch has conflicts".
3. Resolve locally on the second branch (`git fetch`, `git merge origin/main`, fix, run, commit,
   push). Get a fresh approval and merge.

## Exercise 6 (bonus) · A fork

Fork your partner's `desk-notes`, add a `CONTRIBUTING.md` (branch naming, commit types), open the PR
from your fork. After the merge, sync your fork's `main` with `upstream`.

## `[BLOQUÉ?]`

Which exercise, exact command, full output (including any message from GitHub), what you expected.
For authentication problems add `ssh -vT git@github.com 2>&1 | tail -20`.
