## What does this change?

<!-- One or two sentences. -->

## Checklist

- [ ] `python -m ruff check .` passes locally
- [ ] `python -m pytest --cov=target --cov-branch --cov-fail-under=100` passes locally
- [ ] `target.py` is unchanged
- [ ] No secrets, deploy-hook URLs or `.env` files are included
- [ ] The CI `test` job is green on Python 3.10, 3.11 and 3.12
