import os
import subprocess
import requests
import random

def download_archive_music(tags: str, output_dir: str, target_duration_sec: float = None) -> str:
    """
    Core business logic to fetch background music from the Internet Archive (Free Music Archive).
    Downloads a curated clean track matching the tags, and optionally trims/fades it using ffmpeg
    to exactly match the target video length.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Prefer clean acoustic / chillout collections to avoid abrasive glitch/experimental tracks
    search_url = "https://archive.org/advancedsearch.php"
    clean_query = f'collection:freemusicarchive AND mediatype:audio AND (creator:"Jason Shaw" OR creator:"Kevin MacLeod" OR subject:acoustic OR subject:ambient)'
    params = {
        "q": clean_query,
        "fl[]": "identifier",
        "output": "json",
        "rows": 10
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        docs = response.json().get("response", {}).get("docs", [])
    except Exception:
        docs = []

    # Fallback to direct query if specific search returned nothing
    if not docs:
        params["q"] = f'collection:freemusicarchive AND mediatype:audio AND subject:{tags}'
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        docs = response.json().get("response", {}).get("docs", [])

    if not docs:
        raise RuntimeError(f"Internet Archive returned zero results for tags: '{tags}'")

    item = random.choice(docs)
    identifier = item.get("identifier")

    meta_url = f"https://archive.org/metadata/{identifier}"
    meta_response = requests.get(meta_url)
    meta_response.raise_for_status()
    
    files = meta_response.json().get("files", [])
    mp3_files = [f for f in files if f.get("name", "").endswith(".mp3")]
    
    if not mp3_files:
        raise RuntimeError(f"No MP3 files found in the Archive item: '{identifier}'")
        
    mp3_file = mp3_files[0].get("name")
    download_link = f"https://archive.org/download/{identifier}/{mp3_file}"

    safe_tags = "".join([c if c.isalnum() else "_" for c in tags]).strip("_")
    raw_path = os.path.abspath(os.path.join(output_dir, f"bgmusic_{safe_tags}_raw.mp3"))

    download_response = requests.get(download_link, stream=True)
    download_response.raise_for_status()

    with open(raw_path, "wb") as f:
        for chunk in download_response.iter_content(chunk_size=8192):
            f.write(chunk)

    # If target duration is specified, trim and add smooth fade out via ffmpeg
    if target_duration_sec and target_duration_sec > 0:
        final_path = os.path.abspath(os.path.join(output_dir, f"bgmusic_{safe_tags}.mp3"))
        fade_start = max(0.0, target_duration_sec - 4.0)
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", raw_path,
            "-t", f"{target_duration_sec:.2f}",
            "-af", f"afade=t=out:st={fade_start:.2f}:d=4.0",
            "-b:a", "192k",
            final_path
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(raw_path) and raw_path != final_path:
                os.remove(raw_path)
            return final_path
        except Exception:
            return raw_path

    return raw_path

