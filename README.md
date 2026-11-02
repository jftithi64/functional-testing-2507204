# Functional Testing, CI/CD and Live Deployment

A Python functional-testing assignment built around the supplied `target.py` module. The test suite exercises all 16 functions with valid inputs, boundary values, invalid inputs, and wrong types. GitHub Actions runs linting and the tests across the assignment's Python versions and enforces 100% statement and branch coverage.

## Project structure

```text
functional-testing-2507204/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_target.py
├── .gitignore
├── README.md
├── requirements.txt
└── target.py
```

## Requirements

- Python 3.10 or newer for local use.
- Git, if you plan to push the project to GitHub.

The CI workflow tests Python 3.10, 3.11, and 3.12. The pinned development tools below support those versions.

## Setup in VS Code (Windows PowerShell)

Open this folder in VS Code, then open **Terminal → New Terminal**.

1. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

2. Activate it:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the execution-policy instructions provided by your instructor or run the commands from a terminal where activation is permitted.

3. Install the pinned development dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Run the tests:

   ```powershell
   python -m pytest tests/test_target.py -v
   ```

5. Run tests with statement and branch coverage:

   ```powershell
   python -m pytest tests/test_target.py --cov=target --cov-branch --cov-report=term-missing
   ```

6. Run the same 100% coverage gate used by CI and create XML/HTML reports:

   ```powershell
   python -m pytest tests/test_target.py --cov=target --cov-branch --cov-fail-under=100 --cov-report=term-missing --cov-report=xml --cov-report=html
   ```

The expected result for the supplied source and current tests is 128 passing tests and 100% statement and branch coverage. If your local result differs, inspect the failure before changing any test or source code.

## Code quality check

Run Ruff against the application module and tests:

```powershell
python -m ruff check target.py tests
```

## GitHub Actions CI

The workflow is located at `.github/workflows/ci.yml`. It runs on pushes to `main` and pull requests targeting `main`. The `test` job uses Python 3.10, 3.11, and 3.12, installs the pinned requirements, runs Ruff, executes the tests with a 100% coverage threshold, and uploads XML/HTML coverage reports as workflow artifacts.

After creating the GitHub repository, replace `YOUR_GITHUB_USERNAME` in the badge URL below with your actual GitHub username and keep the repository name unchanged if you use the assignment's requested name.

![CI status](https://github.com/YOUR_GITHUB_USERNAME/functional-testing-2507204/actions/workflows/ci.yml/badge.svg)

## Live application

**Live URL:** Not deployed yet. Add the public application URL here after completing the frontend and deployment parts of the assignment.

## Suspected bugs / behavior worth reviewing

The assignment instructs students not to modify `target.py` and to report suspected bugs in this README. The following observations are based on the supplied implementation; they are not changes to the source code:

1. **`greet()` with a non-string value:** The function calls `.strip()` on any non-`None` value. For example, `greet(123)` raises an incidental `AttributeError` rather than a deliberate, documented validation error. The function's stated behavior describes names but does not explicitly specify how non-string inputs should be handled.
2. **`factorial()` with a Boolean:** Python treats `bool` as a subclass of `int`, so `factorial(True)` is accepted and returns `1`. If the intended input is a non-negative integer excluding Boolean values, the function should explicitly reject booleans. This is a suspected input-validation gap, not a modification made for this assignment.

The tests may document current behavior, but unexpected runtime exceptions should not be mistaken for intentional input validation. Keep the supplied `target.py` unchanged for grading.

## Assignment submission checklist

- [ ] Create the GitHub repository named `functional-testing-2507204` (or the exact name assigned to you).
- [ ] Give the instructor the requested repository access.
- [ ] Push the project, including this README, `.gitignore`, `requirements.txt`, and `.github/workflows/ci.yml`.
- [ ] Add the real GitHub Actions badge URL above.
- [ ] Complete the frontend and deployment requirements; then replace the live URL placeholder.
- [ ] Include the required demo video link and final commit SHA in your submission.

No repository URL, instructor account, deployment URL, secret, or commit SHA is assumed in this README.
