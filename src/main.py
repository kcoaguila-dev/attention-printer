import sys
import os

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp.server.mcpserver import MCPServer
from src.pexels_broll.mcp_tool import register_tools
from src.background_music.mcp_tool import register_bg_music_tools
from src.timeline.mcp_tool import register_timeline_tools
from src.sound_design.mcp_tool import register_sound_design_tools
from src.graphics.mcp_tool import register_graphics_tools

# 1. Create an MCPServer instance (Transport/Entry Layer)
mcp = MCPServer("PexelsBrollServer")

# 2. Register tools from the Protocol Layers
register_tools(mcp)
register_bg_music_tools(mcp)
register_timeline_tools(mcp)
register_sound_design_tools(mcp)
register_graphics_tools(mcp)

if __name__ == "__main__":
    # Start the server
    mcp.run()
