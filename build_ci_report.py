"""Add GitHub Actions metadata to the test results for the local receiver."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

source = Path("test-results.json")
if source.exists():
    report = json.loads(source.read_text(encoding="utf-8"))
else:
    report = {"tests": [], "total": 0, "passed": 0, "failed": 0,
              "overall_status": "failed"}

report.update({
    "repository": os.getenv("GITHUB_REPOSITORY", "local-run"),
    "branch": os.getenv("GITHUB_REF_NAME", "local"),
    "commit_sha": os.getenv("GITHUB_SHA", "local"),
    "pipeline_run_id": os.getenv("GITHUB_RUN_ID", "local"),
    "execution_timestamp": datetime.now(timezone.utc).isoformat()
})
Path("ci-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("Complete CI report created: ci-report.json")
