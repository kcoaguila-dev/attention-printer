import os
import urllib.parse
from typing import List, Dict, Any

def to_pathurl(filepath: str) -> str:
    """Converts a local Windows or POSIX file path to a valid file://localhost/ URL for FCPXML."""
    normalized = filepath.replace("\\", "/")
    parts = normalized.split("/")
    encoded_parts = [urllib.parse.quote(p) if ":" not in p else p for p in parts]
    return "file://localhost/" + "/".join(encoded_parts)

def build_premiere_fcpxml(
    screencast_path: str,
    broll_clips: List[Dict[str, Any]],
    music_path: str,
    output_xml_path: str,
    fps: int = 30,
    width: int = 1280,
    height: int = 720,
    total_frames: int = None,
    broll_duration_sec: float = 4.0,
    music_level: float = 0.022,  # ~ -18 dB
    graphic_cards: List[Dict[str, Any]] = None,
    sfx_path: str = None,
    punch_ins: List[Dict[str, Any]] = None
) -> str:
    """
    Builds a 6-track Premiere Pro FCPXML (xmeml v5) timeline:
    - V1: Screencast with 100%/115% punch-in zoom segments.
    - V2: B-Roll video overlays (trimmed to 4s, scaled to frame).
    - V3: 2D graphic callout cards (PNG overlays).
    - A1: Original screencast audio (voiceover).
    - A2: Curated background music (-18 dB ducked, auto-trimmed).
    - A3: Transition whoosh SFX on each cutaway (-14 dB ducked).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_xml_path)), exist_ok=True)

    clip_duration_frames = int(broll_duration_sec * fps)
    screencast_url = to_pathurl(screencast_path)
    music_url = to_pathurl(music_path)
    screencast_name = os.path.basename(screencast_path)
    music_name = os.path.basename(music_path)
    sfx_url = to_pathurl(sfx_path) if sfx_path else ""

    if total_frames is None or total_frames <= 0:
        total_frames = int(180 * fps)

    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append('<!DOCTYPE xmeml>')
    xml.append('<xmeml version="5">')
    xml.append('  <project>')
    xml.append('    <name>Attention Printer</name>')
    xml.append('    <children>')
    xml.append('      <sequence id="sequence-1">')
    xml.append('        <name>Attention Printer Sequence</name>')
    xml.append(f'        <duration>{total_frames}</duration>')
    xml.append('        <rate>')
    xml.append(f'          <timebase>{fps}</timebase>')
    xml.append('          <ntsc>FALSE</ntsc>')
    xml.append('        </rate>')
    xml.append('        <media>')
    xml.append('          <video>')
    xml.append('            <format>')
    xml.append('              <samplecharacteristics>')
    xml.append('                <rate>')
    xml.append(f'                  <timebase>{fps}</timebase>')
    xml.append('                  <ntsc>FALSE</ntsc>')
    xml.append('                </rate>')
    xml.append(f'                <width>{width}</width>')
    xml.append(f'                <height>{height}</height>')
    xml.append('                <pixelaspectratio>square</pixelaspectratio>')
    xml.append('              </samplecharacteristics>')
    xml.append('            </format>')

    # ------------------ Video Track 1: Screencast (with punch-ins) ------------------
    xml.append('            <track>')
    if punch_ins:
        for idx, p in enumerate(punch_ins):
            s_frame = int(p["start_sec"] * fps)
            e_frame = min(total_frames, int(p["end_sec"] * fps))
            dur = e_frame - s_frame
            scale_val = p.get("scale", 100)
            cid = f"clipitem-screencast-v-{idx+1}"
            xml.append(f'              <clipitem id="{cid}">')
            xml.append(f'                <name>{screencast_name}</name>')
            xml.append('                <enabled>TRUE</enabled>')
            xml.append(f'                <duration>{dur}</duration>')
            xml.append('                <rate>')
            xml.append(f'                  <timebase>{fps}</timebase>')
            xml.append('                  <ntsc>FALSE</ntsc>')
            xml.append('                </rate>')
            xml.append(f'                <start>{s_frame}</start>')
            xml.append(f'                <end>{e_frame}</end>')
            xml.append(f'                <in>{s_frame}</in>')
            xml.append(f'                <out>{e_frame}</out>')
            xml.append('                <file id="file-screencast">')
            xml.append(f'                  <name>{screencast_name}</name>')
            xml.append(f'                  <pathurl>{screencast_url}</pathurl>')
            xml.append('                  <rate>')
            xml.append(f'                    <timebase>{fps}</timebase>')
            xml.append('                    <ntsc>FALSE</ntsc>')
            xml.append('                  </rate>')
            xml.append(f'                  <duration>{total_frames}</duration>')
            xml.append('                  <media>')
            xml.append('                    <video>')
            xml.append('                      <samplecharacteristics>')
            xml.append(f'                        <width>{width}</width>')
            xml.append(f'                        <height>{height}</height>')
            xml.append('                      </samplecharacteristics>')
            xml.append('                    </video>')
            xml.append('                  </media>')
            xml.append('                </file>')
            if scale_val != 100:
                xml.append('                <filter>')
                xml.append('                  <effect>')
                xml.append('                    <name>Basic Motion</name>')
                xml.append('                    <effectid>basic</effectid>')
                xml.append('                    <effectcategory>motion</effectcategory>')
                xml.append('                    <effecttype>motion</effecttype>')
                xml.append('                    <mediatype>video</mediatype>')
                xml.append('                    <parameter>')
                xml.append('                      <name>Scale</name>')
                xml.append('                      <parameterid>scale</parameterid>')
                xml.append(f'                      <value>{scale_val}</value>')
                xml.append('                    </parameter>')
                xml.append('                  </effect>')
                xml.append('                </filter>')
            xml.append('              </clipitem>')
    else:
        xml.append('              <clipitem id="clipitem-screencast-v">')
        xml.append(f'                <name>{screencast_name}</name>')
        xml.append('                <enabled>TRUE</enabled>')
        xml.append(f'                <duration>{total_frames}</duration>')
        xml.append('                <rate>')
        xml.append(f'                  <timebase>{fps}</timebase>')
        xml.append('                  <ntsc>FALSE</ntsc>')
        xml.append('                </rate>')
        xml.append('                <start>0</start>')
        xml.append(f'                <end>{total_frames}</end>')
        xml.append('                <in>0</in>')
        xml.append(f'                <out>{total_frames}</out>')
        xml.append('                <file id="file-screencast">')
        xml.append(f'                  <name>{screencast_name}</name>')
        xml.append(f'                  <pathurl>{screencast_url}</pathurl>')
        xml.append('                  <rate>')
        xml.append(f'                    <timebase>{fps}</timebase>')
        xml.append('                    <ntsc>FALSE</ntsc>')
        xml.append('                  </rate>')
        xml.append(f'                  <duration>{total_frames}</duration>')
        xml.append('                  <media>')
        xml.append('                    <video>')
        xml.append('                      <samplecharacteristics>')
        xml.append(f'                        <width>{width}</width>')
        xml.append(f'                        <height>{height}</height>')
        xml.append('                      </samplecharacteristics>')
        xml.append('                    </video>')
        xml.append('                  </media>')
        xml.append('                </file>')
        xml.append('              </clipitem>')
    xml.append('            </track>')

    # ------------------ Video Track 2: B-Roll Overlays ------------------
    xml.append('            <track>')
    for idx, clip in enumerate(broll_clips):
        start_sec = clip.get("start_sec", 0)
        start_frame = int(start_sec * fps)
        end_frame = start_frame + clip_duration_frames
        clip_path = clip.get("path", "")
        clip_name = os.path.basename(clip_path) or f"B-Roll {idx+1}"
        clip_url = to_pathurl(clip_path)
        cid = f"clipitem-broll-{idx+1}"
        fid = f"file-broll-{idx+1}"

        xml.append(f'              <clipitem id="{cid}">')
        xml.append(f'                <name>{clip_name}</name>')
        xml.append('                <enabled>TRUE</enabled>')
        xml.append(f'                <duration>{clip_duration_frames}</duration>')
        xml.append('                <rate>')
        xml.append(f'                  <timebase>{fps}</timebase>')
        xml.append('                  <ntsc>FALSE</ntsc>')
        xml.append('                </rate>')
        xml.append(f'                <start>{start_frame}</start>')
        xml.append(f'                <end>{end_frame}</end>')
        xml.append('                <in>0</in>')
        xml.append(f'                <out>{clip_duration_frames}</out>')
        xml.append(f'                <file id="{fid}">')
        xml.append(f'                  <name>{clip_name}</name>')
        xml.append(f'                  <pathurl>{clip_url}</pathurl>')
        xml.append('                  <rate>')
        xml.append(f'                    <timebase>{fps}</timebase>')
        xml.append('                    <ntsc>FALSE</ntsc>')
        xml.append('                  </rate>')
        xml.append(f'                  <duration>{clip_duration_frames + 60}</duration>')
        xml.append('                  <media>')
        xml.append('                    <video>')
        xml.append('                      <samplecharacteristics>')
        xml.append(f'                        <width>{width}</width>')
        xml.append(f'                        <height>{height}</height>')
        xml.append('                      </samplecharacteristics>')
        xml.append('                    </video>')
        xml.append('                  </media>')
        xml.append('                </file>')
        xml.append('              </clipitem>')
    xml.append('            </track>')

    # ------------------ Video Track 3: 2D Graphic Callouts ------------------
    xml.append('            <track>')
    if graphic_cards:
        card_duration_frames = int(4.5 * fps)
        for idx, card in enumerate(graphic_cards):
            start_sec = card.get("start_sec", 0)
            start_frame = int(start_sec * fps)
            end_frame = start_frame + card_duration_frames
            card_path = card.get("path", "")
            card_name = os.path.basename(card_path) or f"Card {idx+1}"
            card_url = to_pathurl(card_path)
            cid = f"clipitem-card-{idx+1}"
            fid = f"file-card-{idx+1}"

            xml.append(f'              <clipitem id="{cid}">')
            xml.append(f'                <name>{card_name}</name>')
            xml.append('                <enabled>TRUE</enabled>')
            xml.append(f'                <duration>{card_duration_frames}</duration>')
            xml.append('                <rate>')
            xml.append(f'                  <timebase>{fps}</timebase>')
            xml.append('                  <ntsc>FALSE</ntsc>')
            xml.append('                </rate>')
            xml.append(f'                <start>{start_frame}</start>')
            xml.append(f'                <end>{end_frame}</end>')
            xml.append('                <in>0</in>')
            xml.append(f'                <out>{card_duration_frames}</out>')
            xml.append(f'                <file id="{fid}">')
            xml.append(f'                  <name>{card_name}</name>')
            xml.append(f'                  <pathurl>{card_url}</pathurl>')
            xml.append('                  <rate>')
            xml.append(f'                    <timebase>{fps}</timebase>')
            xml.append('                    <ntsc>FALSE</ntsc>')
            xml.append('                  </rate>')
            xml.append(f'                  <duration>{card_duration_frames + 60}</duration>')
            xml.append('                  <media>')
            xml.append('                    <video>')
            xml.append('                      <samplecharacteristics>')
            xml.append(f'                        <width>{width}</width>')
            xml.append(f'                        <height>{height}</height>')
            xml.append('                      </samplecharacteristics>')
            xml.append('                    </video>')
            xml.append('                  </media>')
            xml.append('                </file>')
            xml.append('              </clipitem>')
    xml.append('            </track>')
    xml.append('          </video>')

    # ------------------ Audio Section ------------------
    xml.append('          <audio>')
    # Audio Track 1: Voiceover
    xml.append('            <track>')
    xml.append('              <clipitem id="clipitem-screencast-a1">')
    xml.append(f'                <name>{screencast_name} - Audio</name>')
    xml.append('                <enabled>TRUE</enabled>')
    xml.append(f'                <duration>{total_frames}</duration>')
    xml.append('                <rate>')
    xml.append(f'                  <timebase>{fps}</timebase>')
    xml.append('                  <ntsc>FALSE</ntsc>')
    xml.append('                </rate>')
    xml.append('                <start>0</start>')
    xml.append(f'                <end>{total_frames}</end>')
    xml.append('                <in>0</in>')
    xml.append(f'                <out>{total_frames}</out>')
    xml.append('                <file id="file-screencast"/>')
    xml.append('                <sourcetrack>')
    xml.append('                  <mediatype>audio</mediatype>')
    xml.append('                  <trackindex>1</trackindex>')
    xml.append('                </sourcetrack>')
    xml.append('              </clipitem>')
    xml.append('            </track>')

    # Audio Track 2: Background Music (-18 dB)
    xml.append('            <track>')
    xml.append('              <clipitem id="clipitem-bgmusic-a">')
    xml.append(f'                <name>{music_name}</name>')
    xml.append('                <enabled>TRUE</enabled>')
    xml.append(f'                <duration>{total_frames}</duration>')
    xml.append('                <rate>')
    xml.append(f'                  <timebase>{fps}</timebase>')
    xml.append('                  <ntsc>FALSE</ntsc>')
    xml.append('                </rate>')
    xml.append('                <start>0</start>')
    xml.append(f'                <end>{total_frames}</end>')
    xml.append('                <in>0</in>')
    xml.append(f'                <out>{total_frames}</out>')
    xml.append('                <file id="file-bgmusic">')
    xml.append(f'                  <name>{music_name}</name>')
    xml.append(f'                  <pathurl>{music_url}</pathurl>')
    xml.append('                  <rate>')
    xml.append(f'                    <timebase>{fps}</timebase>')
    xml.append('                    <ntsc>FALSE</ntsc>')
    xml.append('                  </rate>')
    xml.append(f'                  <duration>{total_frames}</duration>')
    xml.append('                  <media>')
    xml.append('                    <audio>')
    xml.append('                      <samplecharacteristics>')
    xml.append('                        <samplerate>44100</samplerate>')
    xml.append('                        <depth>16</depth>')
    xml.append('                      </samplecharacteristics>')
    xml.append('                      <channelcount>2</channelcount>')
    xml.append('                    </audio>')
    xml.append('                  </media>')
    xml.append('                </file>')
    xml.append('                <filter>')
    xml.append('                  <effect>')
    xml.append('                    <name>Audio Levels</name>')
    xml.append('                    <effectid>audiolevels</effectid>')
    xml.append('                    <effectcategory>audiolevels</effectcategory>')
    xml.append('                    <effecttype>audiolevels</effecttype>')
    xml.append('                    <mediatype>audio</mediatype>')
    xml.append('                    <parameter>')
    xml.append('                      <name>Level</name>')
    xml.append('                      <parameterid>level</parameterid>')
    xml.append(f'                      <value>{music_level:.4f}</value>')
    xml.append('                    </parameter>')
    xml.append('                  </effect>')
    xml.append('                </filter>')
    xml.append('              </clipitem>')
    xml.append('            </track>')

    # Audio Track 3: Sound Design / Transition Whoosh SFX (-14 dB)
    xml.append('            <track>')
    if sfx_path and os.path.exists(sfx_path):
        sfx_dur_frames = int(0.5 * fps)  # 0.5s duration = 15 frames
        sfx_triggers = [c.get("start_sec", 0) for c in broll_clips]
        if graphic_cards:
            sfx_triggers.extend([gc.get("start_sec", 0) for gc in graphic_cards])
        sfx_triggers = sorted(list(set(sfx_triggers)))

        for idx, t_sec in enumerate(sfx_triggers):
            s_frame = int(t_sec * fps)
            e_frame = s_frame + sfx_dur_frames
            cid = f"clipitem-sfx-{idx+1}"
            xml.append(f'              <clipitem id="{cid}">')
            xml.append('                <name>sfx_whoosh.wav</name>')
            xml.append('                <enabled>TRUE</enabled>')
            xml.append(f'                <duration>{sfx_dur_frames}</duration>')
            xml.append('                <rate>')
            xml.append(f'                  <timebase>{fps}</timebase>')
            xml.append('                  <ntsc>FALSE</ntsc>')
            xml.append('                </rate>')
            xml.append(f'                <start>{s_frame}</start>')
            xml.append(f'                <end>{e_frame}</end>')
            xml.append('                <in>0</in>')
            xml.append(f'                <out>{sfx_dur_frames}</out>')
            xml.append('                <file id="file-sfx">')
            xml.append('                  <name>sfx_whoosh.wav</name>')
            xml.append(f'                  <pathurl>{sfx_url}</pathurl>')
            xml.append('                  <rate>')
            xml.append(f'                    <timebase>{fps}</timebase>')
            xml.append('                    <ntsc>FALSE</ntsc>')
            xml.append('                  </rate>')
            xml.append(f'                  <duration>{sfx_dur_frames + 30}</duration>')
            xml.append('                  <media>')
            xml.append('                    <audio>')
            xml.append('                      <samplecharacteristics>')
            xml.append('                        <samplerate>44100</samplerate>')
            xml.append('                        <depth>16</depth>')
            xml.append('                      </samplecharacteristics>')
            xml.append('                      <channelcount>2</channelcount>')
            xml.append('                    </audio>')
            xml.append('                  </media>')
            xml.append('                </file>')
            xml.append('                <filter>')
            xml.append('                  <effect>')
            xml.append('                    <name>Audio Levels</name>')
            xml.append('                    <effectid>audiolevels</effectid>')
            xml.append('                    <effectcategory>audiolevels</effectcategory>')
            xml.append('                    <effecttype>audiolevels</effecttype>')
            xml.append('                    <mediatype>audio</mediatype>')
            xml.append('                    <parameter>')
            xml.append('                      <name>Level</name>')
            xml.append('                      <parameterid>level</parameterid>')
            xml.append('                      <value>0.045</value>')  # ~ -14 dB
            xml.append('                    </parameter>')
            xml.append('                  </effect>')
            xml.append('                </filter>')
            xml.append('              </clipitem>')
    xml.append('            </track>')

    xml.append('          </audio>')
    xml.append('        </media>')
    xml.append('      </sequence>')
    xml.append('    </children>')
    xml.append('  </project>')
    xml.append('</xmeml>')

    xml_content = "\n".join(xml)
    with open(output_xml_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

    return os.path.abspath(output_xml_path)
