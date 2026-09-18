import os
import requests
import random

def download_archive_music(tags: str, output_dir: str) -> str:
    """
    Core business logic to fetch background music from the Internet Archive (Free Music Archive).
    Downloads a random MP3 track matching the tags to the specified output directory.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    search_url = "https://archive.org/advancedsearch.php"
    # We search the freemusicarchive collection for audio matching the tags
    query = f'collection:freemusicarchive AND mediatype:audio AND subject:{tags}'
    params = {
        "q": query,
        "fl[]": "identifier",
        "output": "json",
        "rows": 10  # fetch a few to pick a random one
    }

    response = requests.get(search_url, params=params)
    response.raise_for_status()

    data = response.json()
    docs = data.get("response", {}).get("docs", [])

    if not docs:
        raise RuntimeError(f"Internet Archive returned zero results for tags: '{tags}'")

    # Pick a random track from the results
    item = random.choice(docs)
    identifier = item.get("identifier")

    if not identifier:
        raise RuntimeError(f"Missing identifier for the track matching tags: '{tags}'")

    # Now get the metadata to find the mp3 file
    meta_url = f"https://archive.org/metadata/{identifier}"
    meta_response = requests.get(meta_url)
    meta_response.raise_for_status()
    
    files = meta_response.json().get("files", [])
    mp3_files = [f for f in files if f.get("name", "").endswith(".mp3")]
    
    if not mp3_files:
        raise RuntimeError(f"No MP3 files found in the Archive item: '{identifier}'")
        
    mp3_file = mp3_files[0].get("name")
    download_link = f"https://archive.org/download/{identifier}/{mp3_file}"

    # Download the audio file
    download_response = requests.get(download_link, stream=True)
    download_response.raise_for_status()

    # Clean up the tags to make a safe filename
    safe_tags = "".join([c if c.isalnum() else "_" for c in tags]).strip("_")
    filename = f"bgmusic_{safe_tags}.mp3"
    file_path = os.path.join(output_dir, filename)
    absolute_path = os.path.abspath(file_path)

    with open(absolute_path, "wb") as f:
        for chunk in download_response.iter_content(chunk_size=8192):
            f.write(chunk)

    return absolute_path
