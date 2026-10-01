import json
from pathlib import Path

raw_dir = Path("day-02-azure-windows-vm-data-disks-snapshots-migration/screenshots/raw")
with open(raw_dir / "manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

print(f"Total frames: {len(manifest)}")
for m in manifest[::5]:
    idx = m["index"]
    ts = m["timestamp_str"]
    fn = m["filename"]
    print(f"{idx:03d} | {ts} | {fn}")
