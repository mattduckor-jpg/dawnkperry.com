"""One-time: copy every image and PDF from the old Squarespace site into this repo.
Run by .github/workflows/fetch-assets.yml (GitHub Actions has open internet)."""
import json, pathlib, sys, urllib.parse, urllib.request
root = pathlib.Path(__file__).resolve().parent
cfg = json.loads((root / "assets.json").read_text())
jobs = [(root / "images" / n, cfg["base"] + urllib.parse.quote(p) + "?format=1500w") for n, p in cfg["images"].items()]
jobs += [(root / "files" / n, u) for n, u in cfg["files"].items()]
failed = []
for dest, url in jobs:
    dest.parent.mkdir(exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            dest.write_bytes(r.read())
        print("ok  ", dest.name)
    except Exception as e:
        failed.append(dest.name); print("FAIL", dest.name, url, e)
print(f"{len(jobs)-len(failed)}/{len(jobs)} assets in place")
if failed: sys.exit(1)
