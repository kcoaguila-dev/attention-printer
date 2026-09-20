import os
import subprocess

def get_or_create_whoosh_sfx(output_dir: str) -> str:
    """
    Ensures a clean, organic transition whoosh SFX exists in the output directory.
    Synthesizes a 0.5s swept whoosh via ffmpeg if not present.
    """
    os.makedirs(output_dir, exist_ok=True)
    sfx_path = os.path.abspath(os.path.join(output_dir, "sfx_transition_whoosh.wav"))

    if os.path.exists(sfx_path):
        return sfx_path

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "anoisesrc=d=0.5:c=white:r=44100, afade=t=in:st=0:d=0.2, afade=t=out:st=0.2:d=0.3, lowpass=f=1800, volume=0.35",
        sfx_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sfx_path
