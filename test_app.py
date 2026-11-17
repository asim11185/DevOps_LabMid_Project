import tempfile
import unittest
from pathlib import Path
from app import create_app

class SubmissionPortalTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app(Path(self.temp_dir.name) / "submissions.json")
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_complete_details_and_valid_url_are_saved(self):
        response = self.client.post("/submit", data={
            "student_name": "Ali",
            "registration_number": "FA24-BSE-001",
            "assignment_title": "DevOps Lab",
            "submission_url": "https://github.com/ali/assignment"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Submission saved successfully", response.data)
        self.assertIn(b"FA24-BSE-001", response.data)

    def test_missing_registration_number_is_rejected(self):
        response = self.client.post("/submit", data={
            "student_name": "Ali",
            "registration_number": "",
            "assignment_title": "DevOps Lab",
            "submission_url": "https://github.com/ali/assignment"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Registration Number is required", response.data)

    # def test_invalid_submission_url_is_rejected_and_not_saved(self):
    #     response = self.client.post("/submit", data={
    #         "student_name": "Ali",
    #         "registration_number": "FA24-BSE-001",
    #         "assignment_title": "DevOps Lab",
    #         "submission_url": "not-a-valid-url"
    #     })
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn(b"valid HTTP or HTTPS", response.data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn(b"Please enter a valid HTTP or HTTPS submission URL.", response.data)

if __name__ == "__main__":
    unittest.main()
