"""Stage only public website files for deployment."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "_site"
if DEST.exists():
    shutil.rmtree(DEST)
DEST.mkdir()
for name in (
    "index.html", "404.html", ".nojekyll", "_headers", "robots.txt",
    "site.webmanifest", "favicon.ico", "favicon.svg", "apple-touch-icon.png",
    "icon-192.png", "icon-512.png", "og-image.jpg",
):
    shutil.copy2(ROOT / name, DEST / name)
for name in ("img", "fonts"):
    shutil.copytree(ROOT / name, DEST / name)
if (ROOT / "CNAME").exists():
    shutil.copy2(ROOT / "CNAME", DEST / "CNAME")
print(f"Staged {sum(p.is_file() for p in DEST.rglob('*'))} public files in _site/")
