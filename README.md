🎥 Video Forgery Detection (Forensics Tool)

📌 Overview

This project is a lightweight video forensics tool that detects possible tampering in videos.
It analyzes a video file and checks for:
🔁 Loop detection (repeated segments)
✂️ Cut & Paste edits
🧊 Freeze or frame drops
📊 Saves suspicious frames for manual review


🚀 Features

Supports multiple videos at once
Generates reports in JSON + CSV format
Saves suspicious frames as proof in video_analysis_proofs/
Works on macOS, Linux, Windows

🛠️ Requirements

Python 3.8+
Install dependencies:
pip install opencv-python numpy tqdm

📂 How to Run

Clone the repo:
git clone https://github.com/your-username/video-forensics.git
cd video-forensics

Place your .mp4 videos inside the same folder.

Run the script:
python3 video_forensics.py

The tool will automatically scan all .mp4 files and generate:

Reports: video_analysis.json, video_analysis.csv
Proof frames: inside video_analysis_proofs/

📝 Example Output
===== VIDEO FORENSICS REPORT =====
video_file: test_video.mp4
loop_detected: False
cut_paste_detected: False
freeze_or_frame_drop_detected: False
final_status: Authentic
Suspicious Frames Saved: 0 (check video_analysis_proofs/)
===================================

📊 Folder Structure
📂 video-forensics
 ┣ 📜 video_forensics.py
 ┣ 📜 video_analysis.json
 ┣ 📜 video_analysis.csv
 ┣ 📂 video_analysis_proofs/
 ┗ 📹 your_video.mp4

📌 Future Improvements

Add deep learning–based forgery detection
Build a web dashboard for uploading & analyzing videos
Support for more formats (.avi, .mov, .mkv)

👨‍💻 Author

Developed by [Anirudh Singh]
For Smart India Hackathon (SIH 2025) submission
