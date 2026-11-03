# Demo checklist (3-5 minutes)

Record real actions only. Never show the deploy-hook URL or any secret.

1. **Repo + badge** (20 s): show the README, the green CI badge and the live URL.
2. **Green matrix** (30 s): open the latest Actions run: `test` on 3.10 / 3.11 / 3.12, then `deploy` and `smoke-test`. Download or point at a coverage artifact.
3. **A change goes live** (90 s): edit something visible (e.g. the header text in `templates/index.html`), commit and push to `main`. Show `test` -> `deploy` -> `smoke-test` going green. Reload the live site and show that the footer SHA equals the new commit SHA (`git rev-parse HEAD`).
4. **A failing push is blocked** (60 s): break one assertion in `tests/test_target.py`, push to `main`. Show `test` turning red and `deploy` / `smoke-test` being **skipped**. Reload the live site: the SHA is still the previous one. Then revert and push to get green again.
5. **Branch protection** (20 s, bonus): show the ruleset and a PR whose merge is blocked while checks fail.

Step 4 needs a direct push to `main`, so record it before enabling branch protection (or temporarily allow admin bypass).
