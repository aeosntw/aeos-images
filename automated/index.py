import json
import os
import requests
from duckduckgo_search import DDGS

JSON_FILE = "games.json"
OUTPUT_DIR = "images"
LOG_FILE = "log.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_image(url, filename):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "jpeg" in content_type:
            ext = ".jpg"
        elif "png" in content_type:
            ext = ".png"
        elif "gif" in content_type:
            ext = ".gif"
        else:
            ext = ".jpg"
        
        filepath = os.path.join(OUTPUT_DIR, filename + ext)
        with open(filepath, "wb") as f:
            f.write(response.content)
        return filepath
    except Exception as e:
        print(f"🔴 failed to download {url}: {e}")
        return None

def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    titles = [game["title"] for game in data.get("games", [])]

    with open(LOG_FILE, "w", encoding="utf-8") as log:
        with DDGS() as ddgs:
            for title in titles:
                print(f"🟡 searching for: {title}")
                try:
                    results = list(ddgs.images(title, max_results=1))
                    if not results:
                        continue

                    img_url = results[0]["image"]
                    filename = title.replace(" ", "_").replace("/", "_")
                    saved_path = download_image(img_url, filename)
                    
                    if saved_path:
                        log.write(f"{title}: {os.path.basename(saved_path)}\n")
                        print(f"🟢 saved {title} → {saved_path}")
                except Exception as e:
                    print(f"🔴 error searching {title}: {e}")

if __name__ == "__main__":
    main()