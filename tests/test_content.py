import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = {"discovery", "engineering", "rag", "agents", "evaluation", "delivery"}

class ContentTests(unittest.TestCase):
    def test_six_unique_categories_have_five_assessment_questions_each(self):
        data = json.loads((ROOT / "data/curriculum.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data), 6)
        self.assertEqual({item["id"] for item in data}, IDS)
        for item in data:
            with self.subTest(category=item["id"]):
                self.assertEqual(len(item["quiz"]), 5)
                self.assertTrue(item["tasks"] and item["topics"] and item["project"])
                for question in item["quiz"]:
                    self.assertGreaterEqual(question["a"], 0)
                    self.assertLess(question["a"], len(question["o"]))
                    self.assertIn("why", question)
                    self.assertIn(question["source"], range(len(item["sources"])))
                for source in item["sources"]:
                    self.assertTrue(source["url"].startswith("https://"))

    def test_published_recordings_start_empty_and_have_a_documented_schema(self):
        self.assertEqual(json.loads((ROOT / "data/recordings.json").read_text(encoding="utf-8")), [])
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        for field in ("url", "title", "category", "minutes", "summary", "takeaways", "transcript", "created"):
            with self.subTest(field=field):
                self.assertIn(field, app)

    def test_no_external_runtime_libraries_or_credential_placeholders(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertNotRegex(app, re.compile(r"(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|gh[pousr]_[A-Za-z0-9]{20,})"))
        self.assertNotIn("document.write(", app)
        self.assertFalse((ROOT / ".env").exists())

    def test_website_and_publishing_workflow_are_present(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('src="assets/learning-loop.png"', html)
        self.assertIn('href="#assessments"', html)
        self.assertIn("Stevie's Second Brain", html)
        self.assertTrue((ROOT / ".github/workflows/pages.yml").exists())
        self.assertTrue((ROOT / ".github/workflows/publish-recording.yml").exists())

if __name__ == "__main__":
    unittest.main()