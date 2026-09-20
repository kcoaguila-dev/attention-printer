from typing import List, Dict, Any
from src.timeline.logic import build_premiere_fcpxml

def register_timeline_tools(mcp):
    """
    Registers timeline building tools with the provided MCPServer instance.
    """
    @mcp.tool()
    def build_timeline(
        screencast_path: str,
        broll_clips: List[Dict[str, Any]],
        music_path: str,
        output_xml_path: str,
        fps: int = 30,
        width: int = 1280,
        height: int = 720,
        total_frames: int = None,
        broll_duration_sec: float = 4.0,
        music_level: float = 0.022,
        graphic_cards: List[Dict[str, Any]] = None,
        sfx_path: str = None,
        punch_ins: List[Dict[str, Any]] = None
    ) -> str:
        """
        Builds a complete, 100% compliant 6-track Adobe Premiere Pro FCPXML timeline in one shot:
        - V1: Screencast with 100%/115% punch-in zoom segments.
        - V2: B-Roll video overlays (trimmed to 4s, scaled to frame).
        - V3: 2D graphic callout cards (transparent PNG overlays).
        - A1: Original screencast audio (voiceover).
        - A2: Curated background music (-18 dB ducked, auto-trimmed).
        - A3: Transition whoosh SFX on each cutaway (-14 dB ducked).

        Returns:
            The absolute path of the generated XML file.
        """
        return build_premiere_fcpxml(
            screencast_path=screencast_path,
            broll_clips=broll_clips,
            music_path=music_path,
            output_xml_path=output_xml_path,
            fps=fps,
            width=width,
            height=height,
            total_frames=total_frames,
            broll_duration_sec=broll_duration_sec,
            music_level=music_level,
            graphic_cards=graphic_cards,
            sfx_path=sfx_path,
            punch_ins=punch_ins
        )
