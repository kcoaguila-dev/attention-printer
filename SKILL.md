# Attention Printer AI Agent Skill

This document acts as the core instructions for the AI Agent when processing screencasts to automate the addition of B-roll stock footage.

When a video file is uploaded, you must strictly follow this sequence:

## Step 1: Transcribe the Video
Use your native multimodal audio capabilities to listen to the uploaded video file.
Generate a timestamped transcript of the audio content.

## Step 2: Chunk the Transcript
Analyze the generated timestamped transcript.
Break the transcript into roughly 15-second contextual chunks.

## Step 3: Keyword Extraction
For each 15-second contextual chunk, determine a highly visual search keyword that represents the content (e.g., "Hedge Fund", "Hacker", "Money").

## Step 4: Fetch B-Roll
Autonomously call the `fetch_broll` MCP tool for each keyword identified in Step 3.
This will download the relevant stock footage from Pexels for each chunk.

## Step 5: Generate FCPXML
Use your built-in file writing capabilities to generate a standard Adobe Premiere Pro FCPXML file (`.xml`).
The XML must structure the timeline as follows:
- **Video Track 1:** Place the original uploaded screencast.
- **Video Track 2:** Place the downloaded Pexels clips at the exact start timestamps of their corresponding chunks. Each Pexels clip must be trimmed to a maximum duration of 4 seconds.
