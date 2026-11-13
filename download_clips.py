
import os
import io
import json
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Read private credentials from GitHub Secret
credentials_info = json.loads(
    os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)

drive = build("drive", "v3", credentials=credentials)

# Read the funny clips list
with open("clips_data.json", "r", encoding="utf-8") as file:
    clips = json.load(file)

if not clips:
    raise RuntimeError("No funny clips found")

output_folder = Path("funny_clips")
output_folder.mkdir(exist_ok=True)

for index, clip in enumerate(clips, start=1):
    file_id = clip["id"]
    filename = f"clip_{index}.mp4"
    destination = output_folder / filename

    request = drive.files().get_media(fileId=file_id)

    with open(destination, "wb") as output:
        downloader = MediaIoBaseDownload(output, request)
        done = False

        while not done:
            _, done = downloader.next_chunk()

    print(f"Downloaded clip {index}: {filename}")

print("All funny clips downloaded successfully!")
