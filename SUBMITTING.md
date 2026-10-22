# Submitting Your Computer Science I Work

The browser exercises can **Run**, **Check**, **Save draft**, and **Copy code**. They do not automatically commit or open pull requests yet.

## First choose the correct track

| Student activity | Live website | Official GitHub submission repository | File to edit |
|---|---|---|---|
| Guided Units 01–06 | [Lessons](https://www.mswhitby.com/computer-science-1/units/) or [Unit 01](https://www.mswhitby.com/computer-science-1/) | [computer-science-1](https://github.com/mswhitby/computer-science-1) | Unit-specific `practice/<lesson>/main.py` |
| Weekly or reusable questions | [Challenge Lab](https://www.mswhitby.com/computer-science-1/challenges/) | [October 26 challenges](https://github.com/mswhitby/python_problems_20261026) | Problem-specific `problems/<challenge>/solution.py` |

For guided Units 02–06, [the unit directories](units/) show each lesson, starter and prerequisite. The full interactive course unit lab is on the school-approved domain, not `github.io`.

## Submit using GitHub

1. Sign in with your own GitHub account.
2. **Fork the relevant repository** from the table above to your own GitHub account. If you already forked it, **sync your fork with upstream** before starting newly added lessons.
3. On the learning website, choose an exercise, write your code, and use **Run** or **Check** to practice.
4. Use **Copy code** from the website. In your fork, open the **matching file** in the same folder as the assignment.
5. Paste your code into `main.py` (lessons) or `solution.py` (challenges), and **commit** the changes.
6. Open a pull request from your fork's `main` into the original repository's `main`. Keep the PR **open**, and **do not merge it**.
7. Correct errors by committing changes to the same branch and PR. The GitHub Actions checks run again automatically.

**Your code stays in your GitHub fork.** You can come back to it later, sync upstream to get new starter files, and update your own solutions. Do not overwrite working code when syncing.

## Important distinction

The website's **Check** button uses published practice examples. It helps you debug but is **not** an official grade. GitHub Actions handles submitted work. Units 02–06 have a separate PR workflow; it checks **only changed exercises** and doesn't treat unfinished or unchanged lessons as zeros.

The browser currently saves drafts on **this device/browser only**. Clearing site data or switching devices can erase these drafts. Always commit completed work to your fork, or use Copy code for a backup.

## Future workflow

We plan to offer secure **Sign in with GitHub**, **Resume from GitHub**, and **Submit** controls. They require a connected authentication service and explicit access to the student's GitHub repositories. No GitHub passwords, access tokens, teacher secrets, journal responses, or private gradebook data will be placed in this public repository.
