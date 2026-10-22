# Submitting Unit 01 on GitHub

The browser editor currently supports **Run**, **Check**, **Save Draft**, and **Copy Code**. Automatic pull-request submission is a planned feature—not available yet.

## Current submission steps

1. Sign in to GitHub and [fork the Computer Science I repository](https://github.com/mswhitby/computer-science-1/fork), if you haven't already.
2. In your fork, open the matching path under `units/01-how-programs-work/practice/`.
3. Edit the `main.py` file and paste your working code from the browser editor.
4. **Commit** the change in your fork.
5. Open one pull request from your fork's `main` into `mswhitby/computer-science-1` `main`.
6. Leave the pull request open and **do not merge it**. For corrections, commit more changes to the same forked branch.

The GitHub workflow reads the changed scripts and posts test results in the pull request's **Checks / Actions** summary. No result is added to an instructor gradebook in this prototype.

## Why the app cannot submit automatically yet

A publicly hosted site cannot safely include a GitHub token with write access. A future version will use GitHub authentication and a trusted service or GitHub App to securely create branches, commit code, and open or update pull requests. Until that is built, the app never requests your GitHub password or a token.
