

import subprocess
import imageio_ffmpeg

import json

import os

clips_file = os.environ.get("CLIPS_DATA_FILE", "clips_data.json")

with open(clips_file, "r", encoding="utf-8") as file:
    clips = json.load(file)

print("Reel Generator received clips:", len(clips))

import textwrap

with open("meme_data.json", "r", encoding="utf-8") as file:
    meme = json.load(file)

reel_text = str(meme["reelText"])

reel_text = "".join(
    char for char in reel_text
    if ord(char) < 0x2600
)

print("Google Sheet Reel Text loaded successfully!")

# Instagram Reel format: 1080 x 1920, 7 seconds
width = 1080
height = 1920
from pathlib import Path

video_files = sorted(Path("funny_clips").glob("clip_*.mp4"))
if not video_files:
    raise RuntimeError("Funny clips download nahi hui")

selected_video = str(video_files[0])
print("Selected funny video:", selected_video)

video_duration = subprocess.check_output(
    [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        selected_video
    ],
    text=True
).strip()

duration = float(video_duration)
print("Original video duration:", duration)




# Simple test Reel with 3 timed meme lines


lines = []
for part in reel_text.replace("|", "\n").splitlines():
    part = part.strip()
    if part:
        lines.extend(
            textwrap.wrap(
                part,
                
                
                width=22,
                break_long_words=False
            )
        )


if not lines:
    raise ValueError("Google Sheet Reel Text is empty")

# Each line appears for an equal part of the video
filter_parts = []
for i, line in enumerate(lines):
    start = i * duration / len(lines)
    end = (i + 1) * duration / len(lines)

    # Escape special characters for FFmpeg drawtext
    safe_line = (
        line.replace("\\", "\\\\")
            .replace(":", "\\:")
            .replace("'", "\\'")
            .replace("%", "\\%")
            .replace(",", "\\,")
    )

    filter_parts.append(
        f"drawtext=text='{safe_line}':"
        
        
        
        
        "fontcolor=white:fontsize=100:"

 



        "x=(w-text_w)/2:y=(h-text_h)/2:"
        f"enable='between(t,{start:.2f},{end:.2f})'"
    )

filter_text = ",".join(filter_parts)




command = [
    imageio_ffmpeg.get_ffmpeg_exe(), "-y",
    
    
    "-i", selected_video,

    "-f", "lavfi",
    "-i", "anullsrc=r=44100:cl=stereo",
    
    "-vf", f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},{filter_text}",

    
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    "sarcastic_balak_reel.mp4"
]

subprocess.run(command, check=True)
print("MP4 Reel generated successfully!")
("Sarcastic Balak Reel Generator Ready!")
