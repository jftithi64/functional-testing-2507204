# Functional Testing, CI/CD and Live Deployment

[![CI](https://github.com/jftithi64/functional-testing-2507204/actions/workflows/ci.yml/badge.svg)](https://github.com/jftithi64/functional-testing-2507204/actions/workflows/ci.yml)

A small Python project that tests 16 supplied functions, provides a browser-based playground for running them, and demonstrates a test-gated deployment pipeline: every push is tested, and only code that passes every test reaches the live site.

**Live URL:** https://functional-testing-2507204.onrender.com

## Features

- 322 functional test cases for all 16 functions in `target.py` (valid inputs, boundaries, invalid values, wrong types), plus Flask route/API integration tests.
- 100% statement and branch coverage of `target.py`, enforced in CI.
- Ruff linting locally and in GitHub Actions.
- A Flask frontend and JSON API that display each function's result (with its Python type) or the error it raised.
- `GET /health` returns the deployed Git commit SHA, which is also shown in the page footer.
- GitHub Actions pipeline: `test` (Python 3.10, 3.11, 3.12) -> `deploy` (Render deploy hook, main only) -> `smoke-test` (waits for the new SHA, then makes three live requests).

## Project structure

```text
functional-testing-2507204/
â”œâ”€â”€ .github/
â”‚   â”œâ”€â”€ workflows/ci.yml          # test -> deploy -> smoke-test
â”‚   â””â”€â”€ PULL_REQUEST_TEMPLATE.md
â”œâ”€â”€ docs/                         # deployment, CI, branch protection, demo notes
â”œâ”€â”€ templates/index.html          # frontend
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ test_target.py            # functional tests for target.py
â”‚   â””â”€â”€ test_app.py               # frontend / API tests
â”œâ”€â”€ app.py                        # Flask app: frontend, /api/run, /health
â”œâ”€â”€ target.py                     # supplied source; NOT modified
â”œâ”€â”€ pytest.ini
â”œâ”€â”€ render.yaml
â”œâ”€â”€ requirements.txt              # pinned dependencies
â””â”€â”€ README.md
```

## Local setup (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run lint and tests

```powershell
python -m ruff check .
python -m pytest --cov=target --cov-branch --cov-fail-under=100 --cov-report=term-missing
```

## Run the frontend locally

```powershell
python app.py
```

Open `http://127.0.0.1:5000`. Select any of the 16 functions, give its positional arguments as a JSON array (and optional keyword arguments as a JSON object), then click **Run function**.

The JSON API accepts `POST /api/run`, for example:

```json
{"function":"is_adult","args":[18],"kwargs":{}}
```

`GET /health` returns `{"status":"ok","commit_sha":"..."}`. Locally the SHA is `local`.

## CI/CD pipeline

See [docs/CI_WORKFLOW.md](docs/CI_WORKFLOW.md) and [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). The Render deploy-hook URL is stored only as the `RENDER_DEPLOY_HOOK_URL` GitHub Actions secret; the live URL is the `LIVE_APP_URL` Actions variable. Render's own auto-deploy is switched off, so GitHub Actions is the only way code reaches the live site.

## Suspected bugs / surprising behaviour in the supplied target.py

These are observations only; `target.py` is left unchanged as the assignment requires. Each one was reproduced by running the code.

| Function | Input | Actual behaviour | Why it is suspicious |
| --- | --- | --- | --- |
| `greet` | `greet(123)` | `AttributeError: 'int' object has no attribute 'strip'` | No type validation; the error is an accident of calling `.strip()`. Every other string function raises a deliberate `TypeError`. |
| `factorial` | `factorial(True)` | returns `1` | `bool` is accepted because it subclasses `int`, but `to_int` rejects bools, so the rules are inconsistent. |
| `power` | `power(-8, 0.5)` | returns a complex number `(1.7e-16+2.83j)` | A negative base with a fractional exponent silently changes the result type instead of raising an error. |
| `power` | `power(0, -1)` | raw `ZeroDivisionError: 0.0 cannot be raised to a negative power` | Unlike `divide`, there is no explicit check or clear message. |
| `common_items` | `common_items(5, 3)` | returns `1` | It only evaluates `a & b`, so any type supporting `&` (ints, bools) is accepted and returns a non-set. |
| `square_root` | `square_root(float("nan"))` | returns `nan` | NaN passes the `x < 0` check because every comparison with NaN is False. |
| `is_adult` | `is_adult(float("nan"))` | returns `False` | Same NaN comparison issue; NaN is not rejected as invalid. |
| `find_max` / `swap` | `find_max("abc")`, `swap("ab")` | return `"c"` and `("b", "a")` | Strings are accepted, although the docs say lists and tuples. |
| `is_leap_year` | `is_leap_year(2024.0)`, `is_leap_year(True)` | `True`, `False` | Floats and bools are accepted as years. |
| `to_int` | `to_int(float("inf"))` | `OverflowError` | Documented only for bools; infinity raises a different, undocumented exception. |

## Repository

https://github.com/jftithi64/functional-testing-2507204

## Submission checklist

- [ ] Add the instructor as a repository collaborator.
- [ ] At least 10 focused commits with clear messages.
- [ ] 3+ feature branches merged through pull requests (bonus).
- [ ] `main` protected, requiring the CI `test` checks (bonus).
- [ ] All three Python matrix jobs green; coverage artifact downloadable.
- [ ] One red CI run from a failing test, followed by a green fix.
- [ ] Render service created with auto-deploy off; secret and variable configured.
- [ ] `/health`, the live frontend and the three smoke tests verified.
- [ ] 3-5 minute demo video recorded.
- [ ] Submit: repository URL, live URL, demo video link, final commit SHA.
