import os
from src.background_music.logic import download_archive_music

def register_bg_music_tools(mcp):
    """
    Registers the background_music tools with the provided MCPServer instance.
    """
    @mcp.tool()
    def fetch_background_music(tags: str, output_dir: str, target_duration_sec: float = None) -> str:
        """
        Fetches free, clean royalty-free background music from the Internet Archive based on tags.
        Optionally trims and adds a smooth 4s fade-out via ffmpeg to match target video duration.

        Args:
            tags: The search tags for the music (e.g., 'acoustic', 'ambient'). Space-separated.
            output_dir: The local directory where the downloaded MP3 will be saved.
            target_duration_sec: Optional duration in seconds to trim and fade out.

        Returns:
            The absolute local file path of the downloaded and processed audio track.
        """
        return download_archive_music(tags, output_dir, target_duration_sec)
