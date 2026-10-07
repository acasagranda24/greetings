# Session 01 · Exercises: Git as a Commit Graph

**To do after the session, on your own.** In class you built `greetings/` step by step with the
guide, then finished it in pairs. Now you redo the same things without the guide, alone, in a
separate folder. If you can do it like that, you can do it.

Terminal only, nothing else needed. Before each command, write down what you expect, then run it and
compare. Written answers go in `answers.md` (in your practice folder). If you are stuck, jump to
`[BLOQUÉ?]` at the bottom.

On macOS use `python3` instead of `python`. On Windows use Git Bash.

## Exercise 1 · Predict the status (paper first)

In a repository whose last commit contains `a.py` and `b.py`, the following commands are run in
order. After each line, write the exact output of `git status --short`.

```bash
echo "x = 1" >> a.py
git add a.py
echo "y = 2" >> a.py
echo "z = 3" > c.py
git add c.py
git restore --staged c.py
git restore a.py
```

Then reproduce it in a scratch folder and check every line.

## Exercise 2 · Rebuild the welcome desk alone

Create a new folder `greetings-practice/` (not inside your class folder) and produce, in this
order, one commit per step, each with a Conventional Commit message you choose:

1. A `.gitignore` that ignores at least `.env` and `__pycache__/`.
2. `greetings.py` containing only `print("Hello <your first name>!")`.
3. The name stored in a variable and printed with an f-string.
4. A `greet(name)` function, called under `if __name__ == "__main__":`.
5. A `Student` class with `__init__(self, first_name, last_name)` and a `welcome()` method,
   replacing `greet`.
6. A `register(self, registry)` method that gives the student an id (`len(registry) + 1`), adds
   them to the list and returns the id.

Rules: run the script before every commit; check `git diff --staged` before every commit.

Then create a `.env` file with a fake token, run `git add -A`, and show with `git status --short`
that it is not staged. Paste `git log --oneline` in `answers.md`.

## Exercise 3 · Provoke and resolve a conflict alone

In `greetings-practice/`, from the tip of `main`:

1. Create a branch `feat/french`. Change `welcome()` so it returns
   `f"Bienvenue à Albert School, {self.first_name} !"`. Commit.
2. Switch back to `main`. Change `welcome()` so the campus name becomes `Albert School Paris`
   (message still in English). Commit.
3. Before merging, write in `answers.md`: fast-forward or three-way? Conflict or not? Why?
4. Merge `feat/french` into `main`. Resolve the conflict so that the message is in French and
   mentions Albert School Paris. Run the script before committing.
5. Paste `git log --oneline --graph --all` in `answers.md`.

## Exercise 4 · Undo the right way

For each situation, name the command (`restore`, `restore --staged`, `reset --soft`,
`reset --hard`, `revert`) and justify in one sentence.

a. You rewrote `welcome()` for ten minutes, the result is worse, nothing is staged.
b. You ran `git add .env` by mistake (your `.gitignore` was missing). Nothing committed yet.
c. Your last commit, not shared with anyone, has the message `wip`.
d. You committed `feat: print the registry size` (a line `print(f"Registry size: {len(registry)}")`
   at the end of the main block) and already sent the repository to your partner in a bundle; the
   school does not want that line.
e. Same as c., but you also want to throw away everything that commit changed.

Then do **d.** on your practice repository (make the commit, then undo it) and paste
the last three lines of `git log --oneline` in `answers.md`.

## Exercise 5 · Lose a commit, find it again

1. Make a throwaway commit `docs: temporary comment` that adds a comment line at the top of
   `greetings.py`.
2. Run `git reset --hard HEAD~1`. Check with `git log` that the commit is gone.
3. Use `git reflog` to find it and bring `main` back to it.
4. In `answers.md`, explain in two sentences why the commit was recoverable, and when it would not
   have been.

## Exercise 6 (bonus) · A local PR with a review round

1. On a branch `feat/farewell`, add a method `farewell(self)` returning
   `f"See you soon, {self.first_name}!"` and call it at the end of the main block. Commit.
2. Review your own PR as your partner would: `git log --oneline main..feat/farewell` and
   `git diff main...feat/farewell`. Find one thing to improve (a clearer message, a docstring...)
   and fix it with a second commit on the same branch.
3. Merge with `git merge --no-ff feat/farewell -m "Merge feat/farewell (PR #3)"` and delete the
   branch. Paste the graph.

## `[BLOQUÉ?]`

If you got stuck, write down which exercise, the exact command you ran, its full output
(copy-paste it, no summary) and what you expected instead. Then ask me.
