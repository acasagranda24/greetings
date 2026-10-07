# Session 01 · Follow-Along Guide: Git as a Commit Graph

**Course:** Python Environments & Engineering Workflows (MSA-DATI07-01) · MSc 1 · 2h

## What we build today

We start from a one-line script, `greetings.py`, and turn it, commit by commit, into a small
`Student` class for the school's welcome desk: it welcomes a new student, registers them,
and enrolls them in their class. The Python is simple, because today is about Git.

- **First hour, with me:** everyone types the same commands on their own laptop while I project my
  terminal. You learn the three areas, commits, diffs, undoing and branches.
- **Second hour, in pairs:** you finish the script with a classmate. You build two features in
  parallel on branches, review them like pull requests (PRs), then merge them. The second merge
  gives you a conflict, and you resolve it together.

Every step has the same four parts:

- **Predict**: say out loud what you expect before pressing Enter (the course rule).
- **Run**: the command(s).
- **You should see**: the output. Your commit hashes (`94af2d1`...) will differ, everything else
  should match.
- **Why**: what just happened, in one or two sentences.

> **On the board** boxes say what to draw. **If it goes wrong** boxes cover the usual accidents.

**End of session deliverable:** a repository whose `git log --oneline --graph --all` shows atomic
commits with Conventional Commit messages, two merged "PRs" (one with a resolved conflict), one
revert, and no `.env` anywhere in history.

| Part | Topic | Mode |
|---|---|---|
| 0 | Setup | all together |
| 1 | First commits, the three areas | all together |
| 2 | Changing code safely: diff, restore, reset | all together |
| 3 | A branch for the Student class | all together |
| | Break (15 min) | |
| 4 | Pairs and the local PR protocol | pairs |
| 5 | Two features in parallel | pairs |
| 6 | Review, merge, conflict | pairs |
| 7 | Revert | pairs |
| 8 | Deliverable and sharing the repo | pairs |

On macOS, type `python3` wherever this guide says `python`. On Windows, use Git Bash (installed
with Git) for every command, not PowerShell.

---

## Part 0 · Setup

### 0.1 Check the tools

```bash
git --version
python --version
```

You should see `git version 2.x.x` and `Python 3.x.x`.

> **If it goes wrong:** `command not found`. Install Git (macOS: `xcode-select --install`;
> Windows: Git for Windows) and Python 3 from python.org, then open a new terminal.

### 0.2 Tell Git who you are (once per machine)

```bash
git config --global user.name "Firstname Lastname"
git config --global user.email "you@example.org"      # later: the email of your GitHub account
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor "code --wait"         # VS Code opens for commit messages
git config --global --list
```

**Why:** every commit records an author, so Git refuses to commit without a name and an email.
`core.editor` keeps you out of Vim when Git asks for a message.

> **If it goes wrong:** you are in Vim anyway (a screen full of `~`). Press `Esc`, type `:wq`,
> press Enter.

### 0.3 The starting script

```bash
mkdir greetings
cd greetings
```

Create `greetings.py` with exactly one line:

```python
print("Hello Tuka!")
```

```bash
python greetings.py
```

```
Hello Tuka!
```

> **If it goes wrong:** do not create this folder inside another Git repository. Before `git init`,
> `git rev-parse --show-toplevel` must answer `fatal: not a git repository`.

---

## Part 1 · First commits and the three areas

> **On the board:** draw three boxes and keep them all session.
>
> ```
>  WORKING DIRECTORY        STAGING AREA (index)         REPOSITORY
>  files on your disk  --add-->  next commit being   --commit-->  history (commits)
>                                prepared
> ```
>
> "Index" and "staging area" are two names for the same thing.

### 1.1 Turn the folder into a repository

**Predict:** what does `git init` create?

```bash
git init
git status --short
```

```
Initialized empty Git repository in .../greetings/.git/

?? greetings.py
```

**Why:** `git init` creates a hidden `.git/` folder, and that folder is the repository. `??` means
untracked: the file is on disk, Git does not follow it yet.

### 1.2 The first commit is the .gitignore

Some files must never enter history. A `.env` file holds passwords and tokens, and once a secret is
committed it stays in history forever. So the first commit of a project lists what Git ignores.

Create `.gitignore`:

```
.env
__pycache__/
.DS_Store
```

```bash
git add .gitignore
git status --short
```

```
A  .gitignore
?? greetings.py
```

**Why:** `git add` copies the file into the staging area. The left column shows the staging
area: `A` means added. The script is still untracked.

> **On the board:** move `.gitignore` from the first box to the second.

```bash
git commit -m "chore: add .gitignore"
```

```
[main (root-commit) b152563] chore: add .gitignore
 1 file changed, 3 insertions(+)
 create mode 100644 .gitignore
```

**Why:** a commit is a snapshot of the project plus author, date, message and a pointer to its
parent (none here, this is the root commit). `b152563` is the start of its unique id, its hash.

### 1.3 Commit messages: Conventional Commits

Every message follows `<type>: <short summary in the imperative>`.

| Type | For |
|---|---|
| `feat` | a new capability |
| `fix` | a bug fix |
| `refactor` | restructuring, no behaviour change |
| `docs` | documentation only |
| `style` | formatting, naming |
| `test` | tests |
| `chore` | config, tooling |

`update`, `fix stuff` and `wip` are not messages. In six months nobody knows what they contain.

### 1.4 Commit the script

```bash
git add greetings.py
git commit -m "feat: add greetings script"
git log --oneline
```

```
94af2d1 feat: add greetings script
b152563 chore: add .gitignore
```

### 1.5 Prove that .env is ignored

```bash
echo "TOKEN=s3cr3t" > .env
git status --short
git check-ignore -v .env
```

```

.gitignore:1:.env	.env
```

**Why:** `status` shows nothing. `.env` is invisible to Git and `git add` will never pick it up.
`check-ignore -v` tells you which line of which file ignores it.

---

## Part 2 · Changing code safely

### 2.1 A first change: see it before committing it

Replace the content of `greetings.py` with:

```python
name = "Tuka"
print(f"Hello {name}!")
```

**Predict:** what does `git status --short` show?

```bash
git status --short
git diff
```

```
 M greetings.py

diff --git a/greetings.py b/greetings.py
index 1649bc9..5e65bd7 100644
--- a/greetings.py
+++ b/greetings.py
@@ -1 +1,2 @@
-print("Hello Tuka!")
+name = "Tuka"
+print(f"Hello {name}!")
```

**Why:** ` M` in the right column means modified on disk, not staged. `git diff` shows the change
line by line: `-` removed, `+` added. The `@@ ... @@` block is a hunk, a group of consecutive
changed lines.

Check it still works, then stage:

```bash
python greetings.py
git add greetings.py
git status --short
git diff
git diff --staged
```

```
Hello Tuka!

M  greetings.py

(git diff prints nothing)

@@ -1 +1,2 @@
-print("Hello Tuka!")
+name = "Tuka"
+print(f"Hello {name}!")
```

**Why:** two diffs, two questions.

- `git diff`: working directory vs staging area, so what is not staged yet. Empty now.
- `git diff --staged`: staging area vs last commit, so what will be committed.

```bash
git commit -m "refactor: store the name in a variable"
```

### 2.2 A bad commit message, fixed: reset --soft

Replace the content of `greetings.py` with a function:

```python
def greet(name):
    return f"Hello {name}!"


if __name__ == "__main__":
    print(greet("Tuka"))
```

```bash
python greetings.py
git commit -am "wip"
git log --oneline -2
```

```
Hello Tuka!

5ebdd54 wip
4e49b67 refactor: store the name in a variable
```

`-a` stages every tracked modified file before committing. But `wip` breaks our rule. Nobody else
has this commit, so we can undo it:

```bash
git reset --soft HEAD~1
git status --short
git commit -m "refactor: extract a greet function"
git log --oneline
```

```
M  greetings.py

6919c39 refactor: extract a greet function
4e49b67 refactor: store the name in a variable
94af2d1 feat: add greetings script
b152563 chore: add .gitignore
```

**Why:** `HEAD` means "where I am" and `HEAD~1` is its parent. `reset --soft HEAD~1` moves the
branch back one commit and keeps the changes staged (`M` on the left), ready to be recommitted with a
proper message. Only do this on commits you have not shared.

### 2.3 Throw away a bad edit: restore

Break the file:

```bash
echo 'print("oops, I broke everything")' > greetings.py
git status --short
git restore greetings.py
git status --short
python greetings.py
```

```
 M greetings.py


Hello Tuka!
```

**Why:** `git restore <file>` puts back the version from the staging area (here the same as the
last commit). The broken edit is gone: it was never committed, so Git cannot bring it back.
Commit often.

> **On the board:** the three undo tools so far.
>
> | Command | Undoes | Safe once shared? |
> |---|---|---|
> | `git restore <file>` | an edit on disk, not committed | yes |
> | `git restore --staged <file>` | a `git add` (keeps the edit) | yes |
> | `git reset --soft HEAD~1` | the last commit (keeps the changes staged) | no |

---

## Part 3 · A branch for the Student class

> **On the board:** redraw history as a chain of circles, newest on top, each pointing to its
> parent. Put a sticky label `main` on the top circle and `HEAD` pointing at `main`.
>
> - A commit is a snapshot plus a pointer to its parent.
> - A branch is a label on a commit. Creating one copies nothing.
> - HEAD is "where I am". Normally it points at a branch.

### 3.1 Create the branch

```bash
git switch -c feat/student-class
```

```
Switched to a new branch 'feat/student-class'
```

### 3.2 First commit on the branch: welcome a student

Replace the content of `greetings.py` with:

```python
class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def welcome(self):
        return f"Welcome to Albert School, {self.first_name}!"


if __name__ == "__main__":
    student = Student("Tuka", "Bade")
    print(student.welcome())
```

```bash
python greetings.py
git commit -am "feat: add Student class with a welcome message"
```

```
Welcome to Albert School, Tuka!

[feat/student-class 805cf76] feat: add Student class with a welcome message
```

**Python reminder:** `__init__` runs when you write `Student("Tuka", "Bade")` and stores the data
on the object (`self.first_name`). `welcome` is a method: a function attached to the object,
which receives the object as `self`.

### 3.3 Second commit: register the student

Replace the content of `greetings.py` with:

```python
class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = None

    def welcome(self):
        return f"Welcome to Albert School, {self.first_name}!"

    def register(self, registry):
        self.student_id = len(registry) + 1
        registry.append(self)
        return self.student_id


if __name__ == "__main__":
    registry = []
    student = Student("Tuka", "Bade")
    student.register(registry)
    print(student.welcome())
    print(f"Registered as student #{student.student_id}")
```

```bash
python greetings.py
git commit -am "feat: register students in a registry"
git log --oneline --graph --all
```

```
Welcome to Albert School, Tuka!
Registered as student #1

* a5b4d7a feat: register students in a registry
* 805cf76 feat: add Student class with a welcome message
* 6919c39 refactor: extract a greet function
* 4e49b67 refactor: store the name in a variable
* 94af2d1 feat: add greetings script
* b152563 chore: add .gitignore
```

**Atomic commits:** each commit does one thing, you can describe it in one line without "and", and
the script works at every one of them.

### 3.4 Back on main: where did my class go?

**Predict:** what does `greetings.py` contain on `main`?

```bash
git switch main
cat greetings.py
```

```python
def greet(name):
    return f"Hello {name}!"


if __name__ == "__main__":
    print(greet("Tuka"))
```

**Why:** switching branch moves HEAD and rewrites your files to match that commit. Nothing is
lost, the class is still on `feat/student-class`.

### 3.5 Merge: fast-forward

**Predict:** `main` has not moved since the branch was created. What will the merge do?

```bash
git merge feat/student-class
git branch -d feat/student-class
```

```
Updating 6919c39..a5b4d7a
Fast-forward
 greetings.py | 21 ++++++++++++++++++---
 1 file changed, 18 insertions(+), 3 deletions(-)
Deleted branch feat/student-class (was a5b4d7a).
```

**Why:** this is a fast-forward. There is nothing to combine, so Git just slides the `main` label up
to the branch's last commit. No new commit. Deleting the branch removes the label, not the commits.

---

## Break (15 min)

---

## Part 4 · Pairs and the local PR protocol

### 4.1 Form pairs, pick one laptop

Pair up. You work on one laptop, Partner A's repository (A and B should be at the same point: the
end of Part 3). Partner B keeps their own repo untouched and gets a copy of the final result in
Part 8.

**Pair programming:** the driver types, the navigator reads, thinks ahead and catches mistakes.
You swap at each feature.

> **If it goes wrong:** Partner A's repo is not in the right state? Use Partner B's instead. If both
> are broken, start a fresh repository: `git init`, the `.gitignore`, then paste the final code of
> Part 3.3 into `greetings.py` and commit it with `feat: add Student class with welcome and register`.
> One commit instead of six. You lose the history, but you keep the session.

### 4.2 What a pull request is, and how we do it today without GitHub

On a team, nobody changes `main` directly. Every change goes through a pull request: "here is
my branch, please review it, then merge it into `main`". On GitHub (Session 2) it is a web page with
buttons. Underneath it is plain Git, and today we run it by hand:

| PR step | Command today |
|---|---|
| 1. Start from an up-to-date `main` | `git switch main` |
| 2. Create a feature branch | `git switch -c feat/<name>` |
| 3. Commit on it | `git commit -am "feat: ..."` |
| 4. Ask for review: which commits? | `git log --oneline main..feat/<name>` |
| 5. Reviewer reads the change | `git diff main...feat/<name>` |
| 6. Approve, or request changes (new commit on the same branch) | talk, then commit |
| 7. Merge with a merge commit | `git merge --no-ff feat/<name> -m "Merge feat/<name> (PR #n)"` |
| 8. Delete the branch | `git branch -d feat/<name>` |

**Review checklist** (the navigator answers out loud before approving):

- [ ] The script runs and prints what is expected.
- [ ] The branch does one thing, and its commit messages follow Conventional Commits.
- [ ] Names are clear, no leftover debug `print`, no `.env` in the diff.

`--no-ff` ("no fast-forward") forces a merge commit even when a fast-forward is possible. It is
what GitHub's "Create a merge commit" button does, and it leaves a visible trace of each PR.

---

## Part 5 · Two features in parallel

Both features start from the same `main`. On a team, two people work at the same time without
waiting for each other, so this is the normal situation.

> **On the board:** draw `main` with two branches leaving from the same circle:
> `feat/enroll` (PR #1) and `feat/email` (PR #2).

### 5.1 PR #1: enroll the student in a class (A drives, B navigates)

```bash
git switch main
git switch -c feat/enroll
```

In `greetings.py`, make three additions:

1. In `__init__`, after `self.student_id = None`, add:
   ```python
           self.classroom = None
   ```
2. After the `register` method, add a new method:
   ```python
       def enroll(self, classroom):
           self.classroom = classroom
           return f"{self.first_name} {self.last_name} joins {classroom}."
   ```
3. At the very end of the file, add:
   ```python
       print(student.enroll("MSc 1 Data"))
   ```

```bash
python greetings.py
git commit -am "feat: enroll a student in a classroom"
```

```
Welcome to Albert School, Tuka!
Registered as student #1
Tuka Bade joins MSc 1 Data.

[feat/enroll 5ca5731] feat: enroll a student in a classroom
 1 file changed, 6 insertions(+)
```

### 5.2 PR #2: store the student's email (B drives, A navigates)

Swap seats. And start again from `main`, not from `feat/enroll`:

```bash
git switch main
git switch -c feat/email
```

**Predict:** is the `enroll` method in the file now?

No: `main` does not have it yet. In `greetings.py`, make three changes:

1. Change the `__init__` line to accept an email, and store it after `last_name`:
   ```python
       def __init__(self, first_name, last_name, email):
           self.first_name = first_name
           self.last_name = last_name
           self.email = email
           self.student_id = None
   ```
2. In the main block, give Tuka an email:
   ```python
       student = Student("Tuka", "Bade", "tuka@albertschool.com")
   ```
3. At the very end of the file, add:
   ```python
       print(f"Confirmation sent to {student.email}")
   ```

```bash
python greetings.py
git commit -am "feat: store the student email and confirm registration"
git switch main
git log --oneline --graph --all
```

```
Welcome to Albert School, Tuka!
Registered as student #1
Confirmation sent to tuka@albertschool.com

* 84fec46 feat: store the student email and confirm registration
| * 5ca5731 feat: enroll a student in a classroom
|/
* a5b4d7a feat: register students in a registry
* 805cf76 feat: add Student class with a welcome message
...
```

**Why:** the history now forks. Two branches grew from the same commit `a5b4d7a`, their
common ancestor, and neither knows about the other.

---

## Part 6 · Review, merge, conflict

### 6.1 Review PR #1

The author of PR #1 (A) asks B for a review. B runs:

```bash
git log --oneline main..feat/enroll
git diff main...feat/enroll
```

```
5ca5731 feat: enroll a student in a classroom

@@ -3,6 +3,7 @@ class Student:
         self.first_name = first_name
         self.last_name = last_name
         self.student_id = None
+        self.classroom = None
 ...
+    def enroll(self, classroom):
+        self.classroom = classroom
+        return f"{self.first_name} {self.last_name} joins {classroom}."
 ...
+    print(student.enroll("MSc 1 Data"))
```

**Why:** `main..feat/enroll` (two dots) lists the commits on the branch that `main` does not have.
`main...feat/enroll` (three dots) shows what the branch changed since it left `main`, which is what
a reviewer reads in a PR.

B goes through the checklist out loud, then approves. If B asks for a change, A makes a new commit
on `feat/enroll` and B reviews again.

### 6.2 Merge PR #1

**Predict:** will this merge conflict?

```bash
git merge --no-ff feat/enroll -m "Merge feat/enroll (PR #1)"
python greetings.py
```

```
Merge made by the 'ort' strategy.
 greetings.py | 6 ++++++
 1 file changed, 6 insertions(+)

Welcome to Albert School, Tuka!
Registered as student #1
Tuka Bade joins MSc 1 Data.
```

No conflict: `main` had not changed since the branch started.

### 6.3 Review and merge PR #2: the conflict

A reviews PR #2 the same way (`git log` and `git diff main...feat/email`), approves, and merges.

**Predict:** `main` has now changed (PR #1 is in). Both PRs touched `__init__` and the end of
the file. Conflict or not?

```bash
git merge --no-ff feat/email -m "Merge feat/email (PR #2)"
```

```
Auto-merging greetings.py
CONFLICT (content): Merge conflict in greetings.py
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
git status --short
```

```
UU greetings.py
```

`UU` means modified on both sides, not resolved yet. Open `greetings.py`:

```python
class Student:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.student_id = None
        self.classroom = None
    ...

if __name__ == "__main__":
    registry = []
    student = Student("Tuka", "Bade", "tuka@albertschool.com")
    student.register(registry)
    print(student.welcome())
    print(f"Registered as student #{student.student_id}")
<<<<<<< HEAD
    print(student.enroll("MSc 1 Data"))
=======
    print(f"Confirmation sent to {student.email}")
>>>>>>> feat/email
```

**Why:** Git does a three-way merge: it compares each side with the common ancestor.

- In `__init__`, PR #1 added `classroom` and PR #2 added `email` on different lines, so Git
  combined both on its own. Look, both lines are there.
- At the end of the file, both PRs added a line at the same place. Git cannot know which order
  you want, so it stops and shows both:
  - between `<<<<<<< HEAD` and `=======`: our side (`main`, which already contains PR #1);
  - between `=======` and `>>>>>>> feat/email`: their side (the branch being merged).

### 6.4 Resolve together

We want both lines. Replace the five lines from `<<<<<<<` to `>>>>>>>` with:

```python
    print(f"Confirmation sent to {student.email}")
    print(student.enroll("MSc 1 Data"))
```

**Rule: a resolved file that does not run is not resolved.**

```bash
grep -n "<<<<<<<\|=======\|>>>>>>>" greetings.py
python greetings.py
```

The `grep` prints nothing (no marker left), and:

```
Welcome to Albert School, Tuka!
Registered as student #1
Confirmation sent to tuka@albertschool.com
Tuka Bade joins MSc 1 Data.
```

Mark it resolved (stage it), then finish the merge:

```bash
git add greetings.py
git commit --no-edit
git branch -d feat/enroll feat/email
git log --oneline --graph --all
```

```
*   7dc41aa Merge feat/email (PR #2)
|\
| * 84fec46 feat: store the student email and confirm registration
* |   459774d Merge feat/enroll (PR #1)
|\ \
| |/
|/|
| * 5ca5731 feat: enroll a student in a classroom
|/
* a5b4d7a feat: register students in a registry
...
```

> **On the board:** redraw the same graph, but clean. Both branches leave `a5b4d7a`. PR #1 merges into
> `main` (merge commit `459774d`, two parents). PR #2 merges after it (merge commit `7dc41aa`, two
> parents). Each merge commit is a point where two lines of history join.

> **If it goes wrong:** lost in the middle of a merge? `git merge --abort` puts everything back as
> it was before the `git merge`. Then start again.

---

## Part 7 · Revert: undo a shared commit

Someone adds a "fun" feature. In `welcome`, add `.upper()` at the end of the return line:

```python
        return f"Welcome to Albert School, {self.first_name}!".upper()
```

```bash
git commit -am "feat: shout the welcome message"
python greetings.py
```

```
WELCOME TO ALBERT SCHOOL, TUKA!
...
```

The school does not like it. Pretend this commit was already shared: then we must not rewrite history.

```bash
git revert --no-edit HEAD
python greetings.py
git log --oneline -3
```

```
Welcome to Albert School, Tuka!
...
4929f3c Revert "feat: shout the welcome message"
bc387d9 feat: shout the welcome message
7dc41aa Merge feat/email (PR #2)
```

**Why:** `revert` erases nothing. It adds a new commit that does the opposite, so history stays
consistent for everyone who already has the old commit. It is the only undo that is safe on shared
history.

| Shared yet? | Use |
|---|---|
| No (only on my laptop) | `git reset --soft HEAD~1` to redo the last commit |
| Yes (someone may have it) | `git revert <commit>` |

---

## Part 8 · Deliverable and sharing the repo

### 8.1 Check

```bash
git log --oneline --graph --all
git log --all --oneline -- .env
cat .git/HEAD
```

- [ ] atomic commits with Conventional Commit messages
- [ ] two merge commits `Merge feat/... (PR #n)`, one of them with the conflict resolved and the
      script running
- [ ] one `Revert "..."` commit
- [ ] `git log --all --oneline -- .env` prints nothing
- [ ] `cat .git/HEAD` shows `ref: refs/heads/main`

### 8.2 Give Partner B a copy, with the whole history

Without GitHub, a whole repository fits in one file, a bundle. On A's laptop:

```bash
git bundle create ../greetings.bundle --all
```

Send `greetings.bundle` to B (AirDrop, USB key, mail). On B's laptop, in the folder where the file
is:

```bash
git clone greetings.bundle greetings-pair
cd greetings-pair
git log --oneline -3
python greetings.py
```

```
Cloning into 'greetings-pair'...

4929f3c Revert "feat: shout the welcome message"
bc387d9 feat: shout the welcome message
7dc41aa Merge feat/email (PR #2)

Welcome to Albert School, Tuka!
Registered as student #1
Confirmation sent to tuka@albertschool.com
Tuka Bade joins MSc 1 Data.
```

**Why:** `git clone` copies the whole history along with the files. Next session the same
repository goes to GitHub and the PRs become web pages: what you did by hand today turns into
buttons.

Each of you hands in the output of `git log --oneline --graph --all`.

---

## Glossary

| Term | Meaning |
|---|---|
| repository | the `.git/` folder: all commits, branches and settings |
| working directory | the files on your disk, as you edit them |
| staging area / index | the next commit being prepared; filled by `git add` |
| commit | a snapshot of the project + author, date, message, parent(s) |
| hash | the unique id of a commit (`94af2d1...`); the first 7 characters are enough |
| branch | a movable label pointing at one commit |
| HEAD | "where I am"; normally points at a branch |
| `HEAD~1` | the parent of HEAD |
| fast-forward | merge where the label simply slides forward; no new commit |
| merge commit | a commit with two parents, where two branches join |
| conflict | both sides changed the same lines; Git asks you to choose |
| hunk | a block of consecutive changed lines in a diff |
| pull request (PR) | a request to review a branch and merge it into `main` |
| revert | a new commit that undoes an older one |
| bundle | a whole repository in one file, clonable with `git clone` |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Screen full of `~`, cannot quit | Vim opened for a message | `Esc`, then `:wq`, Enter. Then set `core.editor` (Part 0) |
| `Author identity unknown` | name / email not configured | Part 0.2 |
| `fatal: not a git repository` | you are not in the project folder | `cd greetings` |
| Everything in your home folder shows as untracked | `git init` run in the wrong folder | delete that `.git` (`rm -rf ~/.git`), go to the project, `git init` again |
| `.env` shows up in `git status` | `.gitignore` missing or misspelled | check with `git check-ignore -v .env` |
| `.env` already committed | ignored too late | `git rm --cached .env`, commit, revoke the secret if real |
| `error: Your local changes would be overwritten` when switching | uncommitted edits | commit them, or `git stash`, switch, then `git stash pop` |
| `HEAD detached at ...` | you switched to a commit, not a branch | `git switch main` |
| `TypeError: Student.__init__() missing 1 required positional argument: 'email'` | a `Student(...)` call without the email after PR #2 | add the email argument to every `Student(...)` call |
| Merge went badly | conflict resolution is a mess | `git merge --abort` and start again |
| "My commits disappeared" after a reset | the label moved | `git reflog`, then `git reset --hard HEAD@{n}` |
| `python: command not found` (macOS) | Python 3 is called `python3` | use `python3` |

---

## Appendix · Final `greetings.py`

```python
class Student:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.student_id = None
        self.classroom = None

    def welcome(self):
        return f"Welcome to Albert School, {self.first_name}!"

    def register(self, registry):
        self.student_id = len(registry) + 1
        registry.append(self)
        return self.student_id

    def enroll(self, classroom):
        self.classroom = classroom
        return f"{self.first_name} {self.last_name} joins {classroom}."


if __name__ == "__main__":
    registry = []
    student = Student("Tuka", "Bade", "tuka@albertschool.com")
    student.register(registry)
    print(student.welcome())
    print(f"Registered as student #{student.student_id}")
    print(f"Confirmation sent to {student.email}")
    print(student.enroll("MSc 1 Data"))
```
