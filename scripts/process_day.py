#!/usr/bin/env python3
"""
Daily Azure Learning Journey Automation Pipeline
Usage:
    python scripts/process_day.py --video "path/to/recording.mp4" --day 2 --title "Azure Storage Accounts"
"""

import os
import sys
import re
import argparse
import json
from pathlib import Path
import cv2
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

def setup_day_directory(day_num: int, title: str):
    slug = slugify(title)
    day_dir_name = f"day-{day_num:02d}-{slug}"
    day_dir = REPO_ROOT / day_dir_name
    raw_dir = day_dir / "screenshots" / "raw"
    curated_dir = day_dir / "screenshots" / "curated"

    raw_dir.mkdir(parents=True, exist_ok=True)
    curated_dir.mkdir(parents=True, exist_ok=True)

    print(f"Directory ready: {day_dir}")
    return day_dir, raw_dir, curated_dir

def extract_frames(video_path: str, raw_dir: Path, interval_sec: float = 4.0):
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps if fps > 0 else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("=== Video Information ===")
    print(f"Source     : {video_path}")
    print(f"Resolution : {width}x{height}")
    print(f"Duration   : {duration_sec:.1f}s ({duration_sec/60:.2f} mins)")
    print(f"FPS        : {fps:.2f}")
    print("=========================")

    frame_interval = int(fps * interval_sec) if fps > 0 else 120
    count = 0
    frame_idx = 0
    manifest = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            sec = frame_idx / fps if fps > 0 else 0
            mm = int(sec // 60)
            ss = int(sec % 60)
            filename = f"step_{count:03d}_{mm:02d}m{ss:02d}s.png"
            target_path = raw_dir / filename
            cv2.imwrite(str(target_path), frame)
            manifest.append({
                "index": count,
                "timestamp_sec": round(sec, 2),
                "timestamp_str": f"{mm:02d}m{ss:02d}s",
                "filename": filename
            })
            count += 1
        frame_idx += 1

    cap.release()
    manifest_path = raw_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Successfully extracted {count} frames to {raw_dir}")
    print(f"Manifest written to {manifest_path}")

def update_navigation(day_num: int, title: str, day_dir_name: str):
    sidebar_path = REPO_ROOT / "_sidebar.md"
    readme_path = REPO_ROOT / "README.md"
    link_line = f"  * [Day {day_num}: {title}]({day_dir_name}/blog-article.md)"

    # Update _sidebar.md
    if sidebar_path.exists():
        content = sidebar_path.read_text(encoding="utf-8")
        if f"{day_dir_name}/blog-article.md" not in content:
            content = content.rstrip() + f"\n{link_line}\n"
            sidebar_path.write_text(content, encoding="utf-8")
            print(f"Updated {sidebar_path}")

    # Update README.md
    readme_line = f"- **[Day {day_num}: {title}](./{day_dir_name}/blog-article.md)**\n"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        if f"{day_dir_name}/blog-article.md" not in content:
            if "## Articles & Labs" in content:
                parts = content.split("## Articles & Labs\n")
                content = parts[0] + "## Articles & Labs\n" + readme_line + parts[1]
            else:
                content = content.rstrip() + f"\n\n## Articles & Labs\n{readme_line}\n"
            readme_path.write_text(content, encoding="utf-8")
            print(f"Updated {readme_path}")

def validate_no_emojis(day_dir: Path):
    emoji_pattern = re.compile(
        r'[\U00010000-\U0010ffff]'
        r'|[\u2600-\u27bf]'
        r'|[\u2300-\u23ff]'
        r'|[\u2b50-\u2b55]'
        r'|[\u203c\u2049\u2122\u2139\u2194-\u2199\u21a9-\u21aa]'
    )
    for ext in ("*.md", "*.html"):
        for file_path in day_dir.glob(ext):
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            emojis = emoji_pattern.findall(text)
            if emojis:
                print(f"WARNING: Emoji detected in {file_path}: {emojis}")
                return False
    return True

def crop_active_window(image_path: Path, output_path: Path, box: tuple):
    im = Image.open(image_path)
    cropped = im.crop(box)
    cropped.save(output_path)
    print(f"Cropped {image_path.name} -> {output_path.name} ({cropped.size})")

def main():
    parser = argparse.ArgumentParser(description="Azure Daily Lab Automation Pipeline")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--day", type=int, required=True, help="Day number")
    parser.add_argument("--title", required=True, help="Lab title")
    parser.add_argument("--interval", type=float, default=4.0, help="Extraction interval in seconds")
    args = parser.parse_args()

    day_dir, raw_dir, curated_dir = setup_day_directory(args.day, args.title)
    extract_frames(args.video, raw_dir, args.interval)
    update_navigation(args.day, args.title, day_dir.name)
    print("\nScaffolding and frame extraction complete!")

if __name__ == "__main__":
    main()