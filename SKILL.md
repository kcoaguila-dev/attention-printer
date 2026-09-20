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

## Step 4: Screencast Punch-In Zoom Planning
Autonomously plan 115% push-in cuts on the screencast (using `src.motion.logic.plan_screencast_punch_ins`) to eliminate static screen fatigue and emphasize key verbal points.

## Step 5: Fetch B-Roll (Parallel)
Autonomously call the `fetch_broll_batch` MCP tool for all keywords in parallel to download sequence-matched HD MP4 clips.

## Step 6: Generate 2D Graphic Callouts
Autonomously call `create_graphic_callouts` (or `src.graphics.logic.generate_callouts_batch`) for abstract rules, dates, or financial thresholds to create sleek transparent PNG cards.

## Step 7: Fetch Background Music & Sound Design
1. Call `fetch_background_music` with `target_duration_sec` to download and auto-fade a clean acoustic track.
2. Call `get_transition_sfx` to acquire/synthesize the transition whoosh SFX.

## Step 8: Build Complete 6-Track Premiere Pro Timeline
Call `build_timeline` to generate a 100% compliant Premiere Pro FCPXML (`xmeml v5`):
- **Video Track 1:** Screencast with alternating 100%/115% punch-in cuts.
- **Video Track 2:** Downloaded B-roll clips (trimmed to 4s, scaled to sequence frame).
- **Video Track 3:** 2D graphic callout cards.
- **Audio Track 1:** Original voiceover audio.
- **Audio Track 2:** Ducked background music (-18 dB, exact duration with 4s fade).
- **Audio Track 3:** Synchronized transition whoosh SFX (-14 dB).

## Step 9: Automated QA Verification
Verify the project meets professional broadcast standards:
1. **Duration Check:** Audio tracks do not exceed screencast video duration.
2. **Audio Balance:** Music is ducked at -18 dB and SFX at -14 dB so speech is crystal clear.
3. **Visual Scaling:** All stock clips and graphic cards match the 720p/1080p sequence bounds.
4. **Information Polish:** Complex regulatory or numeric claims have visual callout cards.
