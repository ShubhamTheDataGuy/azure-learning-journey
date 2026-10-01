import os
import json
from pathlib import Path
from PIL import Image

DAY2_DIR = Path("day-02-azure-windows-vm-data-disks-snapshots-migration")
RAW_DIR = DAY2_DIR / "screenshots" / "raw"
CURATED_DIR = DAY2_DIR / "screenshots" / "curated"

CURATED_DIR.mkdir(parents=True, exist_ok=True)

def crop_portal_image(src_path: Path, dst_path: Path):
    im = Image.open(src_path)
    w, h = im.size
    px = im.load()

    # Find portal blue on left
    left = 0
    for x in range(60):
        r, g, b = px[x, 20][:3]
        if 0 <= r <= 25 and 110 <= g <= 140 and 190 <= b <= 220:
            left = x
            break

    # Find portal blue on right
    right = w
    for x in range(w - 1, w - 60, -1):
        r, g, b = px[x, 20][:3]
        if 0 <= r <= 25 and 110 <= g <= 140 and 190 <= b <= 220:
            right = x + 1
            break

    # Bottom edge: search for dark desktop/taskbar boundary
    bottom = h
    for y in range(h - 1, h - 30, -1):
        r, g, b = px[left + 50, y][:3]
        if r > 150 and g > 150 and b > 150:
            bottom = y + 1
            break

    cropped = im.crop((left, 0, right, bottom))
    cropped.save(dst_path, optimize=True)
    print(f"Portal Crop: {src_path.name} -> {dst_path.name} ({cropped.size})")

def crop_rdp_image(src_path: Path, dst_path: Path, box=None):
    im = Image.open(src_path)
    if box:
        cropped = im.crop(box)
    else:
        cropped = im
    cropped.save(dst_path, optimize=True)
    print(f"RDP Crop: {src_path.name} -> {dst_path.name} ({cropped.size})")

curated_map = [
    ("step_006_00m24s.png", "01_vm_basics_sku_gotcha.png", "portal"),
    ("step_010_00m40s.png", "02_vm_size_selection_b_series.png", "portal"),
    ("step_030_02m00s.png", "03_vm_created_connect_rdp.png", "portal"),
    ("step_054_03m36s.png", "04_create_and_attach_data_disk.png", "portal"),
    ("step_060_04m00s.png", "05_server_manager_disks_initialization.png", "rdp"),
    ("step_072_04m48s.png", "06_new_volume_wizard_confirmation.png", "rdp"),
    ("step_074_04m56s.png", "07_new_volume_wizard_completed.png", "rdp"),
    ("step_076_05m04s.png", "08_data_disk_online_formatted.png", "rdp"),
    ("step_085_05m40s.png", "09_test_file_created_in_e_drive.png", "rdp"),
    ("step_098_06m32s.png", "10_create_disk_snapshot.png", "portal"),
    ("step_132_08m48s.png", "11_create_managed_disk_from_snapshot.png", "portal"),
    ("step_147_09m48s.png", "12_create_vm2_attach_existing_disk.png", "portal"),
    ("step_152_10m08s.png", "13_vm2_review_create.png", "portal"),
    ("step_174_11m36s.png", "14_vm2_volume_mounted.png", "rdp"),
    ("step_175_11m40s.png", "15_vm2_data_persistence_verified.png", "rdp"),
]

for src_name, dst_name, kind in curated_map:
    src = RAW_DIR / src_name
    dst = CURATED_DIR / dst_name
    if kind == "portal":
        crop_portal_image(src, dst)
    else:
        crop_rdp_image(src, dst)

print("\nAll 15 screenshots curated successfully!")
