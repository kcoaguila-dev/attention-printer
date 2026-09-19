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
        music_level: float = 0.022
    ) -> str:
        """
        Builds a complete, 100% compliant Adobe Premiere Pro FCPXML timeline in one shot.
        Automatically scales B-roll to frame dimensions, trims B-roll to 4s overlays,
        and ducked background music to exact video length.

        Args:
            screencast_path: Path to the original video file.
            broll_clips: List of dicts with 'path' and 'start_sec'.
            music_path: Path to the background music file.
            output_xml_path: Destination path for the .xml file.
            fps: Frame rate (default 30).
            width: Frame width (default 1280).
            height: Frame height (default 720).
            total_frames: Total duration in frames.
            broll_duration_sec: Duration per B-roll overlay (default 4.0s).
            music_level: Music volume multiplier (default 0.022 ~ -18 dB).

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
            music_level=music_level
        )
