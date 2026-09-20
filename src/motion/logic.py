from typing import List, Dict, Any

def plan_screencast_punch_ins(
    total_seconds: float,
    punch_intervals: List[Dict[str, float]] = None
) -> List[Dict[str, Any]]:
    """
    Plans punch-in zoom segments (alternating 100% wide and 115% zoom) on the screencast track.
    If specific punch_intervals are not supplied, creates balanced 10-15s alternating rhythm.
    """
    if punch_intervals:
        return punch_intervals

    # Default balanced rhythm: punch in on key emphasis segments
    # Each item has: 'start_sec', 'end_sec', 'scale' (100 or 115)
    segments = []
    current_time = 0.0
    is_zoomed = False

    while current_time < total_seconds:
        seg_duration = 14.0 if not is_zoomed else 10.0
        end_time = min(total_seconds, current_time + seg_duration)
        segments.append({
            "start_sec": current_time,
            "end_sec": end_time,
            "scale": 115 if is_zoomed else 100
        })
        current_time = end_time
        is_zoomed = not is_zoomed

    return segments
