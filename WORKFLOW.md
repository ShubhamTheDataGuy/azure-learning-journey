# Daily Lab Processing Workflow Reference

Quick reference for processing a daily Azure lab video recording.

## 1-Command CLI Pipeline
Run from the repository root:
```bash
.venv\Scripts\python.exe scripts/process_day.py --video "C:\path\to\recording.mp4" --day 2 --title "Azure Storage Accounts & Blob Hosting"
```

## What the Script Does:
1. Creates folder structure: `day-XX-<slug>/screenshots/raw` and `curated`.
2. Extracts frames at 4-second intervals and generates `manifest.json`.
3. Adds the lab entry to `_sidebar.md` and `README.md`.

## Agent Execution Steps:
1. Run `scripts/process_day.py` with the provided video path and lab title.
2. Review extracted frames and curate the 8-16 essential milestone screenshots.
3. Crop any window that contains extraneous background apps using Pillow:
   ```python
   from PIL import Image
   im = Image.open("path/to/raw.png")
   im.crop((left, top, right, bottom)).save("day-XX/screenshots/curated/XX_name.png")
   ```
4. Draft `day-XX-<slug>/blog-article.md` following the structure in `AGENTS.md`.
5. Run emoji validation:
   ```python
   from scripts.process_day import validate_no_emojis
   from pathlib import Path
   assert validate_no_emojis(Path("day-XX-<slug>"))
   ```
6. Commit and push:
   ```bash
   git add -A; git commit -m "Add Day X: <Title> documentation and curated screenshots"; git push origin main
   ```
7. Send the user the live link: `https://shubhamthedataguy.github.io/azure-learning-journey/#/day-XX-<slug>/blog-article`\n