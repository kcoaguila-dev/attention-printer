import os
import requests

def download_pexels_broll(keyword: str, output_dir: str, api_key: str) -> str:
    """
    Core business logic to fetch B-roll footage from Pexels Video API.
    Downloads the highest quality MP4 (landscape, HD) to the specified output directory.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    search_url = "https://api.pexels.com/videos/search"
    headers = {
        "Authorization": api_key
    }
    params = {
        "query": keyword,
        "orientation": "landscape",
        "size": "hd",
        "per_page": 1  # We only need the first result
    }

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    videos = data.get("videos", [])

    if not videos:
        raise RuntimeError(f"Pexels returned zero results for keyword: '{keyword}'")

    first_video = videos[0]
    video_files = first_video.get("video_files", [])

    # Filter for mp4 files
    mp4_files = [f for f in video_files if f.get("file_type") == "video/mp4"]
    if not mp4_files:
        raise RuntimeError(f"No MP4 files found for the video matching keyword: '{keyword}'")

    # Sort by highest resolution (width * height)
    mp4_files.sort(key=lambda x: x.get("width", 0) * x.get("height", 0), reverse=True)
    best_file = mp4_files[0]
    download_link = best_file.get("link")

    if not download_link:
        raise RuntimeError(f"Missing download link for the best quality video matching keyword: '{keyword}'")

    # Download the video
    download_response = requests.get(download_link, stream=True)
    download_response.raise_for_status()

    # Clean up the keyword to make a safe filename
    safe_keyword = "".join([c if c.isalnum() else "_" for c in keyword]).strip("_")
    filename = f"broll_{safe_keyword}.mp4"
    file_path = os.path.join(output_dir, filename)
    absolute_path = os.path.abspath(file_path)

    with open(absolute_path, "wb") as f:
        for chunk in download_response.iter_content(chunk_size=8192):
            f.write(chunk)

    return absolute_path
