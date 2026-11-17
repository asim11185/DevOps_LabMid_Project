import json
from pathlib import Path
from flask import Flask, request, redirect, url_for, render_template_string

DATA_FILE = Path(__file__).with_name("submissions.json")

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Assignment Submission Portal</title>
  <style>
    body{font-family:Arial,sans-serif;background:#f3f6fb;margin:0;color:#182235}
    main{max-width:850px;margin:35px auto;padding:24px}
    .panel{background:white;padding:24px;border-radius:12px;box-shadow:0 3px 14px #0001;margin-bottom:20px}
    h1{color:#174a8b} label{display:block;margin-top:13px;font-weight:bold}
    input{box-sizing:border-box;width:100%;padding:11px;margin-top:6px;border:1px solid #bbc6d5;border-radius:6px}
    button{margin-top:18px;padding:11px 18px;background:#1769aa;color:white;border:0;border-radius:6px;cursor:pointer}
    .error{color:#b42318;background:#fff0ee;padding:10px;border-radius:6px}
    .success{color:#087443;background:#eaf8f0;padding:10px;border-radius:6px}
    li{padding:10px;border-bottom:1px solid #e5e9f0} a{overflow-wrap:anywhere}
  </style>
</head>
<body><main>
  <h1>Assignment Submission Portal</h1>
  <section class="panel">
    <h2>Submit an assignment</h2>
    {% if message %}<p class="{{ 'error' if error else 'success' }}">{{ message }}</p>{% endif %}
    <form method="post" action="/submit">
      <label>Student name</label><input name="student_name" required value="{{ values.get('student_name','') }}">
      <label>Registration number</label><input name="registration_number" required value="{{ values.get('registration_number','') }}">
      <label>Assignment title</label><input name="assignment_title" required value="{{ values.get('assignment_title','') }}">
      <label>Submission URL</label><input name="submission_url" type="url" required placeholder="https://example.com/my-assignment" value="{{ values.get('submission_url','') }}">
      <button type="submit">Submit assignment</button>
    </form>
  </section>
  <section class="panel"><h2>Saved submissions ({{ submissions|length }})</h2>
    {% if submissions %}<ul>{% for item in submissions %}
      <li><b>{{ item.student_name }}</b> — {{ item.registration_number }}<br>
      {{ item.assignment_title }}<br><a href="{{ item.submission_url }}" target="_blank" rel="noopener">{{ item.submission_url }}</a></li>
    {% endfor %}</ul>{% else %}<p>No submissions yet.</p>{% endif %}
  </section>
</main></body></html>
"""

def load_submissions():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def validate_submission(data):
    required = ("student_name",  "registration_number", "assignment_title", "submission_url")
    for field in required:
        if not str(data.get(field, "")).strip():
            return False, f"{field.replace('_', ' ').title()} is required."
    from urllib.parse import urlparse
    parsed = urlparse(str(data["submission_url"]).strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc or "." not in parsed.netloc:
        return False, "Please enter a valid HTTP or HTTPS submission URL."
    return True, ""

def create_app(data_file=None):
    global DATA_FILE
    if data_file is not None:
        DATA_FILE = Path(data_file)
    app = Flask(__name__)

    @app.get("/")
    def home():
        return render_template_string(PAGE, submissions=load_submissions(),
                                      message=request.args.get("message", ""),
                                      error=request.args.get("error") == "1", values={})

    @app.post("/submit")
    def submit():
        data = {key: request.form.get(key, "").strip() for key in
                ("student_name", "registration_number", "assignment_title", "submission_url")}
        valid, message = validate_submission(data)
        if not valid:
            return render_template_string(PAGE, submissions=load_submissions(),
                                          message=message, error=True, values=data), 400
        submissions = load_submissions()
        submissions.append(data)
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(json.dumps(submissions, indent=2), encoding="utf-8")
        return redirect(url_for("home", message="Submission saved successfully."))

    return app

if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=True)
