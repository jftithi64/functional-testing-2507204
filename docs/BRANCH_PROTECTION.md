# Protect the main branch

Do this after the workflow has run at least once (GitHub only offers checks it has seen).

1. **Settings -> Rules -> Rulesets -> New branch ruleset** (or **Branches -> Add branch protection rule**), target branch `main`.
2. Enable **Require a pull request before merging**.
3. Enable **Require status checks to pass** and add the three checks `test (3.10)`, `test (3.11)` and `test (3.12)`.
4. Save, then open a pull request with a failing test and confirm **Merge** is blocked.

Do this *after* recording the "failing push is blocked from deploying" part of the demo (see `DEMO_CHECKLIST.md`), because that part needs one direct push to `main`.
