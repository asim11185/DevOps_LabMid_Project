"""Local HTTP receiver. Saves each incoming CI report as test-report.json."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
from datetime import datetime, timezone

OUTPUT = Path(__file__).with_name("test-report.json")

class ReportHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/report":
            self.send_error(404, "Use POST /report")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 2_000_000:
                self.send_error(400, "Invalid report size")
                return
            report = json.loads(self.rfile.read(length).decode("utf-8"))
            required = ("repository", "branch", "commit_sha", "pipeline_run_id",
                        "execution_timestamp", "tests", "total", "passed", "failed",
                        "overall_status")
            missing = [key for key in required if key not in report]
            if missing:
                self.send_error(400, "Missing fields: " + ", ".join(missing))
                return
            OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
            body = b'{"message":"Report received and saved"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            print(f"[{datetime.now().isoformat(timespec='seconds')}] Saved {report['overall_status']} report to {OUTPUT}")
        except (ValueError, UnicodeDecodeError) as exc:
            self.send_error(400, f"Invalid JSON: {exc}")

    def log_message(self, fmt, *args):
        print("Receiver:", fmt % args)

if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 5001), ReportHandler)
    print("Report receiver running at http://127.0.0.1:5001/report")
    print("Keep this window open while GitHub Actions runs.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nReceiver stopped.")
        server.server_close()
