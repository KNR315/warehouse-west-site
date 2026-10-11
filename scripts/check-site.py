"""Validate the buildless site with Python and Node standard libraries."""
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def asset(value):
    value = value.strip().strip("\"'")
    if not value or value.startswith("#") or urlparse(value).scheme:
        return
    assert not value.startswith("/"), f"Root-relative asset breaks project hosting: {value}"
    path = ROOT / value.split("?")[0].split("#")[0]
    assert path.is_file(), f"Missing asset: {value}"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.references, self.labels = set(), [], []
        self.mode, self.buffer, self.script_type = None, "", None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"Duplicate ID: {attrs['id']}"
            self.ids.add(attrs["id"])
        if tag == "label" and "for" in attrs:
            self.labels.append(attrs["for"])
        self.references.extend(attrs.get("aria-describedby", "").split())
        if "src" in attrs:
            asset(attrs["src"])
        if tag == "link" and "href" in attrs:
            asset(attrs["href"])
        if tag in {"script", "style"}:
            self.mode, self.buffer, self.script_type = tag, "", attrs.get("type")

    def handle_data(self, data):
        if self.mode:
            self.buffer += data

    def handle_endtag(self, tag):
        if tag != self.mode:
            return
        if tag == "script":
            if self.script_type == "application/ld+json":
                assert json.loads(self.buffer)["@type"] == "EventVenue"
            else:
                subprocess.run(["node", "--check"], input=self.buffer, text=True, check=True)
        else:
            for value in re.findall(r"url\(([^)]+)\)", self.buffer):
                asset(value)
        self.mode = None


for name in ("index.html", "404.html"):
    page = Page()
    source = (ROOT / name).read_text()
    page.feed(source)
    assert set(page.references + page.labels) <= page.ids, f"Broken field reference in {name}"
    assert '<html lang="en"' in source
index = (ROOT / "index.html").read_text()
for value in re.findall(r'img:\s*"([^"]+)"', index):
    asset(value)
for value in re.findall(r'<meta[^>]+(?:property="og:image"|name="twitter:image")[^>]+content="([^"]+)"', index):
    assert value.startswith("https://"), "Social previews need absolute HTTPS image URLs"
manifest = json.loads((ROOT / "site.webmanifest").read_text())
assert manifest["start_url"] == "./"
for icon in manifest["icons"]:
    asset(icon["src"])
assert (ROOT / ".nojekyll").exists()
print("PASS: HTML references, assets, metadata, manifest and JavaScript syntax")
