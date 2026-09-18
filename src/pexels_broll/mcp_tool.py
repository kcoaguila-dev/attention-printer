import os
from src.pexels_broll.logic import download_pexels_broll

def register_tools(mcp):
    """
    Registers the pexels_broll tools with the provided FastMCP server instance.
    """
    @mcp.tool()
    def fetch_broll(keyword: str, output_dir: str) -> str:
        """
        Fetches B-roll footage from Pexels Video API based on a keyword.
        Downloads the highest quality MP4 (landscape, HD) to the specified output directory.

        Args:
            keyword: The search keyword for the video (e.g., 'Hedge Fund', 'Hacker', 'Money').
            output_dir: The local directory where the downloaded video will be saved.

        Returns:
            The absolute local file path of the downloaded video.
        """
        api_key = os.environ.get("PEXELS_API_KEY")
        if not api_key:
            raise ValueError("PEXELS_API_KEY environment variable is not set.")
        
        # We delegate the actual logic to our data/logic layer.
        return download_pexels_broll(keyword, output_dir, api_key)
