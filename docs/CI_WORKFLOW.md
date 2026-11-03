# Continuous integration workflow

`.github/workflows/ci.yml` runs on every push to `main` and on every pull request targeting `main`.

| Job | Runs when | What it does |
| --- | --- | --- |
| `test` | always | On Python 3.10, 3.11 and 3.12 (pip cached): Ruff lint, all tests, fails below 100% statement + branch coverage of `target.py`, uploads the coverage report as an artifact. |
| `deploy` | push to `main` only, `needs: test` | Calls the Render deploy hook (GitHub secret `RENDER_DEPLOY_HOOK_URL`) for the exact commit SHA. |
| `smoke-test` | after `deploy` | Waits until the live `/health` reports the new SHA, then checks `GET /health`, `GET /` and `POST /api/run`. |

If any `test` matrix entry fails, `deploy` and `smoke-test` are skipped and the live site is unchanged. Pull requests only ever run `test`, because the deploy job is limited to pushes on `main`.

Each matrix entry uploads its own artifact (`coverage-python-3.10`, `-3.11`, `-3.12`); download them from the run's summary page.
