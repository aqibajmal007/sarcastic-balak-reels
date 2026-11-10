
import os
import json
import urllib.parse
import urllib.request

url = os.environ["MEME_API_URL"]
key = os.environ["MEME_API_KEY"]

request_url = url + "?" + urllib.parse.urlencode({
    "key": key
})

with urllib.request.urlopen(request_url, timeout=30) as response:
    data = json.load(response)

if "error" in data:
    raise RuntimeError("API authorization failed")

if not data.get("success") or not data.get("meme"):
    raise RuntimeError("No approved meme found")

meme = data["meme"]

print("Google Sheet connection successful!")
print("Meme row:", meme["row"])
print("Meme idea:", meme["idea"])
