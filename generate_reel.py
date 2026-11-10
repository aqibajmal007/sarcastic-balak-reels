

import subprocess
import imageio_ffmpeg

import json

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
duration = 7

# Simple test Reel with 3 timed meme lines

lines = [
    line.strip()
    for line in reel_text.replace("|", "\n").splitlines()
    if line.strip()
]

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
        
        
        
        f"fontcolor=white:fontsize=75:"
 



        "x=(w-text_w)/2:y=(h-text_h)/2:"
        f"enable='between(t,{start:.2f},{end:.2f})'"
    )

filter_text = ",".join(filter_parts)


command = [
    imageio_ffmpeg.get_ffmpeg_exe(), "-y",
    "-f", "lavfi",
    "-i", f"color=c=0x161622:s={width}x{height}:r=24",
    "-f", "lavfi",
    "-i", "anullsrc=r=44100:cl=stereo",
    "-vf", filter_text,
    "-t", str(duration),
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
