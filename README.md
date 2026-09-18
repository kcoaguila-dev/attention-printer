# Attention Printer

Attention Printer is a project designed to automate the process of adding B-roll stock footage to educational screencasts to maximize viewer retention.

Instead of relying on a rigid, expensive Python script with LLM APIs and Whisper, this project utilizes an Interactive Agent Workflow via the Model Context Protocol (MCP). A multimodal AI assistant native to the IDE listens to the video, deduces keywords, uses the provided MCP tool to fetch Pexels videos, and writes a Premiere Pro XML file directly to the local hard drive.

## Files included

- `pexels_mcp.py`: The FastMCP Server exposing a single tool `fetch_broll(keyword, output_dir)` to fetch stock footage securely using the Pexels Video API.
- `SKILL.md`: The brain/instructions for the IDE agent describing the exact steps the AI should take to process the video and use the MCP tool.

## Setup and Configuration

To use the MCP server in your AI environment, follow these steps:

1. **Get a Pexels API Key:**
   You will need a free API key from Pexels to access the video search functionality.

2. **Set Environment Variable:**
   Set the `PEXELS_API_KEY` environment variable in your AI environment or system where the MCP server will be running.
   ```bash
   export PEXELS_API_KEY="your_api_key_here"
   ```

3. **Install Dependencies:**
   Make sure you have `mcp` and `requests` installed in the Python environment where `pexels_mcp.py` will execute.
   ```bash
   pip install mcp requests
   ```

4. **Configure the AI Environment:**
   Configure your MCP-compatible AI environment (e.g., Claude Desktop or your preferred IDE agent) to launch the `pexels_mcp.py` script as an MCP server.

   Typically, this involves pointing the MCP client configuration to run the Python script. For example:
   ```json
   {
     "mcpServers": {
       "pexels_broll": {
         "command": "python",
         "args": ["/absolute/path/to/pexels_mcp.py"],
         "env": {
           "PEXELS_API_KEY": "your_api_key_here"
         }
       }
     }
   }
   ```
   *Note: Adjust the configuration block format according to your specific AI tool's requirements.*

Once configured, your AI assistant will be able to autonomously call the `fetch_broll` tool as described in `SKILL.md` to download B-roll footage to your specified output directory.
