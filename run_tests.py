"""Run the tests and save a machine-readable report, even when tests fail."""
import json
import sys
import time
import unittest
from pathlib import Path

class JSONResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def startTest(self, test):
        self._current_test = test
        super().startTest(test)

    def addSuccess(self, test):
        self.records.append({"name": test.id(), "result": "passed", "failure_message": ""})
        super().addSuccess(test)

    def addFailure(self, test, err):
        self.records.append({"name": test.id(), "result": "failed",
                             "failure_message": self._exc_info_to_string(err, test)})
        super().addFailure(test, err)

    def addError(self, test, err):
        self.records.append({"name": test.id(), "result": "failed",
                             "failure_message": self._exc_info_to_string(err, test)})
        super().addError(test, err)

def main():
    suite = unittest.defaultTestLoader.discover(".", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2, resultclass=JSONResult)
    result = runner.run(suite)
    records = result.records
    report = {
        "execution_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tests": records,
        "total": len(records),
        "passed": sum(x["result"] == "passed" for x in records),
        "failed": sum(x["result"] == "failed" for x in records),
        "overall_status": "passed" if result.wasSuccessful() else "failed"
    }
    Path("test-results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\nTest report saved to test-results.json")
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(main())
