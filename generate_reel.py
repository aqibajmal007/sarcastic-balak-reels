

import subprocess

# Instagram Reel format: 1080 x 1920, 7 seconds
width = 1080
height = 1920
duration = 7

# Simple test Reel with 3 timed meme lines
filter_text = (
    "drawtext=text='Salary credited':"
    "fontcolor=white:fontsize=85:"
    "x=(w-text_w)/2:y=(h-text_h)/2:"
    "enable='between(t,0,2)',"
    "drawtext=text='EMI deducted':"
    "fontcolor=white:fontsize=85:"
    "x=(w-text_w)/2:y=(h-text_h)/2:"
    "enable='between(t,2,4)',"
    "drawtext=text='Bank balance gone':"
    "fontcolor=yellow:fontsize=80:"
    "x=(w-text_w)/2:y=(h-text_h)/2:"
    "enable='between(t,4,7)'"
)

command = [
    "ffmpeg", "-y",
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
