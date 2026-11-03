# Render deployment setup

The app runs as a Render web service with **automatic deploys turned off**. The only thing that can deploy it is the `deploy` job in `.github/workflows/ci.yml`, which runs after the `test` job passes on a push to `main`.

## 1. Create the Render service

1. Sign in to Render and choose **New -> Blueprint**, then select this GitHub repository (it reads `render.yaml`). Alternatively create a **Web Service** manually: runtime Python, build command `pip install -r requirements.txt`, start command `gunicorn app:app`.
2. Confirm the health-check path is `/health`.
3. In the service **Settings -> Build & Deploy**, make sure **Auto-Deploy** is **Off** (the Blueprint also sets `autoDeployTrigger: off`).
4. Wait for the first manual deploy to finish and open the service URL. You should see the playground, and `/health` should show a commit SHA.
5. In **Settings**, copy the **Deploy Hook** URL. Treat it like a password.

## 2. Configure GitHub

Repository **Settings -> Secrets and variables -> Actions**:

| Kind | Name | Value |
| --- | --- | --- |
| Secret | `RENDER_DEPLOY_HOOK_URL` | the private deploy-hook URL from Render |
| Variable | `LIVE_APP_URL` | the public service URL, e.g. `https://my-service.onrender.com` |

## 3. How a deploy happens

1. `deploy` calls the hook with `&ref=<commit SHA>`, so Render builds exactly the commit that passed the tests.
2. `smoke-test` polls `/health` until `commit_sha` equals that SHA (up to 20 minutes, to allow for free-tier cold starts), then makes three live requests: `GET /health`, `GET /`, `POST /api/run`.

Never paste the deploy-hook URL into code, the README, screenshots or the demo video.
