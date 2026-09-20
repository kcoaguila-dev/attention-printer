from typing import List, Dict, Any
from src.graphics.logic import generate_callouts_batch

def register_graphics_tools(mcp):
    """
    Registers 2D graphic callout tools with the provided MCPServer instance.
    """
    @mcp.tool()
    def create_graphic_callouts(callouts: List[Dict[str, Any]], output_dir: str) -> List[Dict[str, Any]]:
        """
        Generates sleek transparent 2D callout cards (PNGs) for important educational stats/rules.

        Args:
            callouts: List of dicts with 'title', 'subtitle', 'start_sec', optional 'badge', 'accent'.
            output_dir: Directory where the generated PNG cards will be saved.

        Returns:
            List of callout dicts updated with absolute 'path' references.
        """
        return generate_callouts_batch(callouts, output_dir)
