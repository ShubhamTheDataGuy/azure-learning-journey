import os
import sys
import cv2

video_path = r"C:\Users\Shubham\Videos\Screen Recordings\Screen Recording 2026-09-30 201807.mp4"
output_dir = r"C:\Users\Shubham\Desktop\Azure-Learning-Journey\day-01-azure-linux-vm\screenshots\raw"

os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error opening video: {video_path}")
    sys.exit(1)

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration_sec = total_frames / fps if fps > 0 else 0
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("=== Video Metadata ===")
print(f"Resolution : {width}x{height}")
print(f"FPS        : {fps:.2f}")
print(f"TotalFrames: {total_frames}")
print(f"Duration   : {duration_sec:.1f}s ({duration_sec/60:.2f} mins)")
print("======================")

# Extract 1 frame every 4 seconds to get a comprehensive timeline of every screen and action
interval_sec = 4
frame_interval = int(fps * interval_sec) if fps > 0 else 120

count = 0
frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_idx % frame_interval == 0:
        sec = frame_idx / fps if fps > 0 else 0
        mm = int(sec // 60)
        ss = int(sec % 60)
        filename = f"step_{count:03d}_{mm:02d}m{ss:02d}s.png"
        cv2.imwrite(os.path.join(output_dir, filename), frame)
        count += 1
    frame_idx += 1

cap.release()
print(f"Done! Saved {count} frames to {output_dir}")
