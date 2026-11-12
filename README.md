# DevOps Lab Mid — Assignment Submission Portal

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Git
- A GitHub account
- For automatic delivery to your computer: ngrok (or another secure HTTPS tunnel)

## 1. Download and run the project on Windows

Open Command Prompt in this project folder, then run:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

Open http://127.0.0.1:5000 in your browser. Enter all four fields and submit.
Valid submissions are saved in `submissions.json`.

## 2. Run automated tests locally

Open a second Command Prompt in the same project folder:

```bat
.venv\Scripts\activate
py run_tests.py
```

The command creates `test-results.json`. A failed test makes the command return a failure exit code.

## 3. Start the local report receiver

Open a third Command Prompt:

```bat
py receiver.py
```

The receiver listens on port 5001 and saves received reports as `test-report.json` in this project folder. Keep this window open.

## 4. Connect GitHub Actions to your computer

A GitHub-hosted runner cannot reach your computer using its own `localhost`. You need a secure HTTPS tunnel.

1. Create an ngrok account and install ngrok from its official website: https://ngrok.com/
2. Configure your ngrok authentication token using the instructions in your ngrok dashboard.
3. With `receiver.py` still running, open another Command Prompt and run:

```bat
ngrok http 5001
```

4. Copy the HTTPS forwarding address displayed by ngrok, for example `https://example.ngrok-free.app`.
5. In your GitHub repository open **Settings → Secrets and variables → Actions → New repository secret**.
6. Name the secret `REPORT_RECEIVER_URL`.
7. Set its value to the forwarding address followed by `/report`, for example `https://example.ngrok-free.app/report`.
8. Save the secret. Keep both the receiver and ngrok windows running while you push and while the workflow executes.

The example address above is only a format example. Use the real HTTPS address shown in your ngrok window. Do not commit tunnel credentials or tokens to GitHub.

## 5. Upload the project to GitHub

Create an empty GitHub repository, for example `devops-lab-mid`. Do not add a README on GitHub if you already have this README locally.

In Command Prompt, inside the project folder:

```bat
git init
git add .
git commit -m "Complete DevOps lab mid project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/devops-lab-mid.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. If `origin` already exists, use `git remote set-url origin https://github.com/YOUR-USERNAME/devops-lab-mid.git` instead of `git remote add origin`.

Every later code change can be uploaded with:

```bat
git add .
git commit -m "Describe your change"
git push
```

Each push to `main` starts the GitHub Actions workflow.

## 6. Check the pipeline and local JSON report

1. On GitHub open your repository → **Actions**.
2. Open the latest **Assignment Portal CI** run.
3. Review the test output and the report-delivery step.
4. On your computer open `test-report.json`. It should contain repository, branch, commit SHA, pipeline run ID, timestamp, every test result, total/passed/failed counts and overall status.
5. The workflow also uploads `ci-report.json` as an artifact. Artifact download is extra evidence; it does not replace the automatic receiver.

If the delivery step fails, check that `receiver.py` and ngrok are running, the secret URL ends in `/report`, and the tunnel URL has not changed.

## 7. Demonstrate pass, fail, and correction

Keep the receiver and tunnel running throughout all three pushes.

**A. Passing run:** Push the original code. Show all three tests passing in Actions and `test-report.json` with `overall_status` set to `passed`.

**B. Failing run:** Temporarily introduce a defect in `app.py`. For example, in `validate_submission`, temporarily change the valid URL condition so that valid HTTPS links are rejected. Commit and push this change. Show the failed test in Actions and the newly received JSON report with `overall_status` set to `failed`.

**C. Corrected run:** Undo the temporary defect, commit and push again. Show all tests passing and the local JSON report updated to `passed`.

Do not submit the deliberately broken version as your final code. The final push must contain the corrected application.

## 8. Bonus: GitHub Pages

The workflow contains a `deploy-pages` job. It runs only after the test-and-report job succeeds on `main` and publishes the static demo in `docs/`.

In GitHub, open **Settings → Pages** and set the build/deployment source to **GitHub Actions**. Push a passing commit to `main`. After deployment, the URL normally has this format:

`https://YOUR-USERNAME.github.io/devops-lab-mid/`

Use the actual URL shown in the repository's Pages settings or deployment.

GitHub Pages hosts only the static demo; it does not run the Flask/Python backend.

## What to submit

- GitHub repository URL
- Setup/run instructions (this README)
- Evidence/screenshots of passing, failing, and corrected Actions runs
- Evidence that `test-report.json` was automatically updated for both passing and failing runs
- GitHub Pages URL if the bonus deployment succeeds

## Notes

- The local receiver overwrites `test-report.json` with the latest run, as requested.
- The workflow uses `if: always()` to build and send the report even if tests fail. The final step then makes the workflow fail when tests fail.
- If the computer sleeps, shuts down, or loses its internet connection, the tunnel cannot deliver the report. Keep the computer awake and both receiver and tunnel running during the demonstration.
