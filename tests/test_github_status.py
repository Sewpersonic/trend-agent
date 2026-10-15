import json
import unittest
from unittest import mock

from trendagent import github_status as gs

RUNS = [
    {"databaseId": 1, "workflowName": "practice", "status": "completed", "conclusion": "failure",
     "createdAt": "2026-10-14T22:17:00Z", "updatedAt": "2026-10-14T22:21:30Z", "event": "schedule", "url": "u1"},
    {"databaseId": 2, "workflowName": "tests", "status": "completed", "conclusion": "success",
     "createdAt": "2026-10-14T10:00:00Z", "updatedAt": "2026-10-14T10:01:00Z", "event": "push", "url": "u2"},
    {"databaseId": 3, "workflowName": "status", "status": "completed", "conclusion": "success",
     "createdAt": "2026-10-14T10:00:00Z", "updatedAt": "2026-10-14T10:01:00Z", "event": "workflow_run", "url": "u3"},
]
JOBS = {"jobs": [{"steps": [{"name": "Trend-agent", "conclusion": "success"},
                            {"name": "Gezondheidscontrole", "conclusion": "failure"}]}]}


def fake(args):
    return json.dumps(RUNS if args[1] == "list" else JOBS)


class GithubStatusTest(unittest.TestCase):
    def test_collect(self):
        with mock.patch.object(gs, "_gh", side_effect=fake):
            rows = gs.collect()
        self.assertEqual(len(rows), 2)
        fout, goed = rows
        self.assertEqual(fout["uitkomst"], "fout")
        self.assertEqual(fout["fout_stap"], "Gezondheidscontrole")
        self.assertIn("niet betrouwbaar", fout["uitleg"])
        self.assertEqual(fout["duur_min"], 4.5)
        self.assertEqual(fout["wat"], "Dagelijkse ronde van de bots")
        self.assertEqual(goed["uitkomst"], "goed")
        self.assertEqual(goed["uitleg"], "")
        self.assertFalse(fout["opgelost"])
