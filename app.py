from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
VIDEO_PATH = "input_video.mp4"  # Change this to your actual video file path
HIGHLIGHT_OUTPUT_PATH = "output_highlight.mp4"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Soccer Highlight Reel API!"})

@app.route('/generate_highlight', methods=['POST'])
def generate_highlight():
    try:
        # Check if video exists
        if not os.path.exists(VIDEO_PATH):
            return jsonify({"error": "Video file not found."}), 404

        logger.info("Processing video for highlights...")
        
        video = VideoFileClip(VIDEO_PATH)
        
        # Example: Extract a 10-second highlight from 30 to 40 seconds
        highlight = video.subclip(30, 40)
        highlight.write_videofile(HIGHLIGHT_OUTPUT_PATH, codec="libx264")
        
        return jsonify({"message": "Highlight generated successfully.", "output": HIGHLIGHT_OUTPUT_PATH})
    
    except Exception as e:
        logger.error(f"Error generating highlight: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
