from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import random

app = Flask(__name__)

# Define paths
VIDEO_PATH = "input_video.mp4"
OUTPUT_PATH = "output_highlight.mp4"

# List of trending background music files (replace with actual music file paths)
MUSIC_TRACKS = [
    "music/tiktok_song_1.mp3",
    "music/youtube_short_1.mp3",
    "music/instagram_reel_1.mp3"
]

def detect_key_moments():
    """Simulates AI detecting key soccer events (goals, shots, tackles)"""
    return [10, 30, 50]  # Placeholder timestamps

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Upload a video and generate an AI-powered highlight reel with trending music!"})

@app.route('/upload', methods=['POST'])
def upload_video():
    """Upload a soccer match video"""
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    file.save(VIDEO_PATH)
    return jsonify({"message": "Video uploaded successfully. Now call /generate to create highlights!"}), 200

@app.route('/generate', methods=['GET'])
def generate_highlight():
    """Generates AI-powered highlight reel with random trending music"""
    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = frame_count / fps if fps > 0 else 0

    if video_duration == 0:
        return jsonify({"error": "Invalid video file"}), 400

    key_timestamps = detect_key_moments()
    clip_duration = 5
    clips = []
    def generate_highlight():
    video = VideoFileClip(VIDEO_PATH)  # Ensure this is properly indented
    # Your other processing code here

    for timestamp in key_timestamps:
        start = max(0, timestamp - clip_duration)
        end = min(video_duration, timestamp + clip_duration)
        clips.append(video.subclip(start, end))

    if clips:
        highlight_reel = mp.concatenate_videoclips(clips)

        # Select a random background music track
        music_track = random.choice(MUSIC_TRACKS)
        if os.path.exists(music_track):
            audio = mp.AudioFileClip(music_track)
            highlight_reel = highlight_reel.set_audio(audio)

        highlight_reel.write_videofile(OUTPUT_PATH, codec="libx264", fps=fps)
        return jsonify({"message": "Highlight reel generated with trending music!", "download_url": "/download"}), 200
    else:
        return jsonify({"error": "No key moments detected"}), 400

@app.route('/download', methods=['GET'])
def download_video():
    """Download the generated highlight reel"""
    return send_file(OUTPUT_PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
