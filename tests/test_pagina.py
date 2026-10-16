import re
import unittest
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "dashboard" / "index.html"


class PaginaTest(unittest.TestCase):
    """Het dashboard haalt bepaalde onderdelen weg; dan werkt de pagina niet meer goed."""

    def test_geen_weggehaalde_onderdelen(self):
        html = PAGE.read_text(encoding="utf-8")
        for tag in ("form", "iframe", "meta", "base"):
            self.assertIsNone(re.search(rf"<{tag}\b", html), f"<{tag}> wordt door het dashboard weggehaald")
        self.assertIsNone(re.search(r"<[a-z][^>]*\son[a-z]+=", html), "on...= attributen werken niet in het dashboard")

    def test_elk_id_waar_het_script_om_vraagt_bestaat(self):
        html = PAGE.read_text(encoding="utf-8")
        ids = set(re.findall(r'\sid="([^"]+)"', html))
        gevraagd = set(re.findall(r"getElementById\('([^']+)'\)", html))
        # id's die het script zelf aanmaakt
        gemaakt = set(re.findall(r"id: '([^']+)'", html))
        self.assertEqual(sorted(gevraagd - ids - gemaakt), [])


if __name__ == "__main__":
    unittest.main()
