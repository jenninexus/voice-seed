#!/usr/bin/env python3
"""Normalise the OmniVoice clone renders and make mp3 previews.

The engine writes 24 kHz mono at roughly -13 to -15 LUFS. The preview page
puts every clip at the same level, so a difference in loudness never gets
mistaken for a difference in voice. Each render is measured, given a static
gain to -16 LUFS, limited to -1.5 dBTP, and written out as both a
normalised WAV and an mp3 for the page.

The raw engine output is left untouched in `raw/` so the change is auditable.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("restore", HERE / "restore-voice-clip.py")
restore = importlib.util.module_from_spec(spec)
spec.loader.exec_module(restore)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone-dir", type=Path, required=True)
    ap.add_argument("--lufs", type=float, default=-16.0)
    ap.add_argument("--bitrate", default="192k")
    ap.add_argument("--keep-native-rate", action="store_true",
                    help="keep the engine's 24 kHz instead of resampling to 48 kHz")
    args = ap.parse_args()

    raw_dir = args.clone_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for wav in sorted(args.clone_dir.glob("*.wav")):
        if wav.parent == raw_dir:
            continue
        # keep the untouched engine output
        (raw_dir / wav.name).write_bytes(wav.read_bytes())

        norm = restore.normalize_static(wav, args.lufs)
        out = wav.with_suffix(".mp3")
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav),
               "-codec:a", "libmp3lame", "-b:a", args.bitrate]
        if not args.keep_native_rate:
            cmd += ["-ar", "48000"]
        cmd.append(str(out))
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode != 0:
            print(f"FAIL {wav.name}: {res.stderr.decode(errors='replace')[:160]}")
            continue
        meas = restore.measure(restore.decode(wav))
        rows.append({
            "file": wav.name,
            "mp3": out.name,
            "lufs": norm.get("target_lufs"),
            "gain_db": norm.get("gain_db"),
            "true_peak_dbfs": norm.get("true_peak_dbfs"),
            "duration_s": meas["duration_s"],
        })
        print(f"{wav.name}: {norm.get('measured_lufs')} -> {args.lufs} LUFS "
              f"(gain {norm.get('gain_db')} dB), TP {norm.get('true_peak_dbfs')}")

    out_json = args.clone_dir / "clone-report.json"
    out_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"\n-> {out_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
