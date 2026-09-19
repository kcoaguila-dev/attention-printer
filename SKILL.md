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

## Step 5: Fetch Background Music
Autonomously call the `fetch_background_music` MCP tool to download a clean acoustic or lo-fi music track suitable for the video's theme.
Always pass `target_duration_sec` matching the screencast length so the audio is automatically trimmed with a smooth 4-second fade-out.

## Step 6: Generate FCPXML
Autonomously call the `build_timeline` MCP tool (or use `src.timeline.logic.build_premiere_fcpxml`) to generate a 100% Premiere Pro compliant FCPXML (`xmeml v5`) in one shot.
The XML timeline structures:
- **Video Track 1:** The original uploaded screencast.
- **Video Track 2:** Downloaded Pexels clips at the exact start timestamps of their corresponding chunks, trimmed to 4 seconds, pre-scaled to sequence resolution.
- **Audio Track 1:** Original voiceover audio.
- **Audio Track 2:** Ducked background music track (volume set to ~ -18 dB / 0.022 level), trimmed to exact video duration.

## Step 7: Automated QA Verification
Verify the generated project meets professional standards:
1. **Duration Check:** Confirm audio does not exceed screencast video duration.
2. **Audio Levels:** Confirm background music is ducked so voiceover is intelligible.
3. **Visual Scaling:** Confirm B-roll clips fill frame dimensions without letterboxing or extreme cropping.
4. **Visual Mix:** Ensure dense conceptual sections feature graphic/diagram cards rather than generic B-roll.
