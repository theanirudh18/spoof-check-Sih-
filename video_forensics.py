import cv2
import numpy as np
import os
import json
import csv
from skimage.metrics import structural_similarity as ssim

def detect_video_editing(video_path, output_prefix="report", save_proofs=True):
    cap = cv2.VideoCapture(video_path)
    ret, prev = cap.read()
    if not ret:
        print("❌ Could not read video")
        return
    
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    frame_no = 0
    
    loop_detected = False
    cut_detected = False
    freeze_detected = False

    prev_noise = None

    # Proof folder
    proof_folder = f"{output_prefix}_proofs"
    if save_proofs and not os.path.exists(proof_folder):
        os.makedirs(proof_folder)
    
    suspicious_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_no += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ---------- (1) Loop Detection ----------
        score, _ = ssim(prev_gray, gray, full=True)
        if score > 0.98:  # very high similarity = repeated frame
            loop_detected = True
            if save_proofs:
                fname = os.path.join(proof_folder, f"loop_frame_{frame_no}.jpg")
                cv2.imwrite(fname, frame)
                suspicious_frames.append({"type": "loop", "frame": frame_no, "file": fname})

        # ---------- (2) Cut-Paste Detection (Noise Level) ----------
        noise = np.std(gray)  # rough noise measure
        if prev_noise is not None:
            if abs(noise - prev_noise) > 15:  # sudden spike in noise
                cut_detected = True
                if save_proofs:
                    fname = os.path.join(proof_folder, f"cut_frame_{frame_no}.jpg")
                    cv2.imwrite(fname, frame)
                    suspicious_frames.append({"type": "cut-paste", "frame": frame_no, "file": fname})
        prev_noise = noise

        # ---------- (3) Frame Freeze / Drop (Optical Flow) ----------
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 
                                            0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        avg_motion = mag.mean()

        if avg_motion < 0.01 and noise > 5:  # no motion but not static scene
            freeze_detected = True
            if save_proofs:
                fname = os.path.join(proof_folder, f"freeze_frame_{frame_no}.jpg")
                cv2.imwrite(fname, frame)
                suspicious_frames.append({"type": "freeze", "frame": frame_no, "file": fname})

        prev_gray = gray

    cap.release()

    # ---------- Final Report Dictionary ----------
    report = {
        "video_file": video_path,
        "loop_detected": loop_detected,
        "cut_paste_detected": cut_detected,
        "freeze_or_frame_drop_detected": freeze_detected,
        "suspicious_frames": suspicious_frames,
        "final_status": "Edited" if (loop_detected or cut_detected or freeze_detected) else "Authentic"
    }

    # ---------- Save as JSON ----------
    json_file = f"{output_prefix}.json"
    with open(json_file, "w") as jf:
        json.dump(report, jf, indent=4)

    # ---------- Save as CSV ----------
    csv_file = f"{output_prefix}.csv"
    with open(csv_file, "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=report.keys())
        writer.writeheader()
        writer.writerow(report)

    # ---------- Print Report ----------
    print("\n===== VIDEO FORENSICS REPORT =====")
    for key, value in report.items():
        if key != "suspicious_frames":
            print(f"{key}: {value}")
    print(f"Suspicious Frames Saved: {len(suspicious_frames)} (check {proof_folder}/)")
    print("===================================")
    print(f"\n✅ Report saved as: {json_file}, {csv_file}")

# ---------- Pick video interactively ----------
videos = [f for f in os.listdir('.') if f.lower().endswith('.mp4')]

if not videos:
    print("❌ No .mp4 files found in this folder.")
else:
    print("\nAvailable videos:")
    for i, v in enumerate(videos, 1):
        print(f"{i}. {v}")

    choice = int(input("Enter the number of the video you want to check: "))
    video_file = videos[choice - 1].strip()

    print(f"\n🔎 Checking video: {video_file}")
    detect_video_editing(video_file, output_prefix=f"{os.path.splitext(video_file)[0]}_analysis")

