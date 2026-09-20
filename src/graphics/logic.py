import os
from typing import List, Dict, Any
from PIL import Image, ImageDraw, ImageFont

ACCENT_COLORS = {
    "cyan": {"border": (56, 189, 248, 255), "badge": (14, 165, 233, 255)},
    "amber": {"border": (251, 191, 36, 255), "badge": (245, 158, 11, 255)},
    "emerald": {"border": (52, 211, 153, 255), "badge": (16, 185, 129, 255)},
    "rose": {"border": (251, 113, 133, 255), "badge": (244, 63, 94, 255)},
}

def generate_callout_card(
    title: str,
    subtitle: str,
    output_path: str,
    badge: str = "KEY FACT",
    accent: str = "cyan",
    canvas_w: int = 1280,
    canvas_h: int = 720
) -> str:
    """
    Renders a sleek, modern transparent 2D callout lower-third card for educational videos.
    Outputs a transparent RGBA PNG matching the sequence resolution.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    colors = ACCENT_COLORS.get(accent.lower(), ACCENT_COLORS["cyan"])

    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Card positioning (bottom-left quadrant)
    x0, y0 = 64, canvas_h - 180
    x1, y1 = 540, canvas_h - 60

    # Draw rounded dark background card
    draw.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=14,
        fill=(15, 23, 42, 235),
        outline=colors["border"],
        width=2
    )

    # Draw small pill badge
    badge_text = badge.upper()
    draw.rounded_rectangle(
        [x0 + 20, y0 + 16, x0 + 120, y0 + 38],
        radius=6,
        fill=colors["badge"]
    )
    draw.text((x0 + 30, y0 + 20), badge_text, fill=(255, 255, 255, 255))

    # Draw Title and Subtitle
    draw.text((x0 + 20, y0 + 48), title, fill=(255, 255, 255, 255))
    draw.text((x0 + 20, y0 + 78), subtitle, fill=(148, 163, 184, 255))

    img.save(output_path, "PNG")
    return os.path.abspath(output_path)

def generate_callouts_batch(callouts: List[Dict[str, Any]], output_dir: str) -> List[Dict[str, Any]]:
    """
    Batch-generates multiple transparent callout cards.
    Each item in callouts should have 'title', 'subtitle', 'start_sec', and optional 'badge', 'accent'.
    """
    results = []
    for idx, c in enumerate(callouts):
        filename = f"card_{idx+1}_{c.get('badge', 'fact').lower()}.png"
        out_path = os.path.join(output_dir, filename)
        generate_callout_card(
            title=c.get("title", ""),
            subtitle=c.get("subtitle", ""),
            output_path=out_path,
            badge=c.get("badge", "KEY FACT"),
            accent=c.get("accent", "cyan")
        )
        c_copy = dict(c)
        c_copy["path"] = out_path
        results.append(c_copy)
    return results
