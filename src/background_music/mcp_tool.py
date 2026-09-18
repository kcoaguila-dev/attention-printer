import os
from src.background_music.logic import download_archive_music

def register_bg_music_tools(mcp):
    """
    Registers the background_music tools with the provided MCPServer instance.
    """
    @mcp.tool()
    def fetch_background_music(tags: str, output_dir: str) -> str:
        """
        Fetches free background music from the Internet Archive based on tags.
        Downloads an MP3 track to the specified output directory.

        Args:
            tags: The search tags for the music (e.g., 'ambient', 'electronic'). Space-separated.
            output_dir: The local directory where the downloaded MP3 will be saved.

        Returns:
            The absolute local file path of the downloaded audio track.
        """
        # We delegate the actual logic to our data/logic layer.
        return download_archive_music(tags, output_dir)
