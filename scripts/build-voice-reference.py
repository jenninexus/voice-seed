#!/usr/bin/env python3
"""Build a voice-clone reference from restored clips.

OmniVoice takes at most 20 s of reference audio (its own
`CLONE_REF_TEXT_MAX_SECONDS = 20.0`) and reads it at 24 kHz. This script
assembles restored clips into a reference that is under that cap, writes it at
24 kHz mono so nothing is resampled inside the model, and emits the matching
transcript - the clone conditioning is only as good as the text/audio pair.

Two shapes are produced because they answer different questions:

  solo    one continuous sentence. No cut points, so nothing about the join
          can colour the voice. This is the cleanest possible reference.
  merged  several sentences with short gaps, trimmed to the cap. More
          phonetic coverage, at the cost of a few cut points.

Usage:
  python build-voice-reference.py --clips-dir <dir> --clips V1-4 --out <wav>
  python build-voice-reference.py --clips-dir <dir> --clips V1-1,V1-3,V1-4 --out <wav>
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SR = 24000
MAX_REF_SECONDS = 19.5   # stay under OmniVoice's hard 20.0 s guard


def decode(path: Path, sr: int = SR) -> list[float]:
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path),
           "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"decode failed for {path}: {res.stderr.decode(errors='replace')}")
    import numpy as np
    return np.frombuffer(res.stdout, dtype=np.float32).astype("float64")


def write_wav(path: Path, samples, sr: int = SR) -> None:
    import numpy as np
    x = np.clip(np.asarray(samples), -1.0, 1.0)
    ints = np.round(x * 8388607.0).astype(np.int32)
    buf = bytearray(3 * len(ints))
    for i, v in enumerate(ints):
        buf[i * 3] = v & 0xFF
        buf[i * 3 + 1] = (v >> 8) & 0xFF
        buf[i * 3 + 2] = (v >> 16) & 0xFF
    data = bytes(buf)
    hdr = (b"RIFF" + (36 + len(data)).to_bytes(4, "little") + b"WAVEfmt "
           + (16).to_bytes(4, "little") + (1).to_bytes(2, "little")
           + (1).to_bytes(2, "little") + sr.to_bytes(4, "little")
           + (sr * 3).to_bytes(4, "little") + (3).to_bytes(2, "little")
           + (24).to_bytes(2, "little") + b"data" + len(data).to_bytes(4, "little"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(hdr + data)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips-dir", type=Path, required=True)
    ap.add_argument("--clips", required=True, help="comma list of clip ids, e.g. V1-1,V1-4")
    ap.add_argument("--level", default="studio", help="restoration level suffix")
    ap.add_argument("--transcript", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--gap-ms", type=int, default=260)
    ap.add_argument("--max-seconds", type=float, default=MAX_REF_SECONDS)
    args = ap.parse_args()

    import numpy as np

    records = {r["file"].rsplit(".", 1)[0]: r for r in json.loads(args.transcript.read_text(encoding="utf-8"))}

    pieces = []
    texts = []
    used = []
    skipped = []
    gap = np.zeros(int(SR * args.gap_ms / 1000))
    max_samples = int(args.max_seconds * SR)
    total = 0
    for clip in [c.strip() for c in args.clips.split(",") if c.strip()]:
        wav = args.clips_dir / f"{clip}.{args.level}.wav"
        if not wav.exists():
            print(f"MISSING {wav}", file=sys.stderr)
            return 1
        piece = decode(wav)
        need = len(piece) + (len(gap) if pieces else 0)
        if pieces and total + need > max_samples:
            # Never trim a clip in the middle: a half-clip makes the reference
            # text disagree with the reference audio, and a mismatched
            # text/audio pair is the quietest way to ruin a clone. Drop the
            # clip whole instead and keep the transcript honest.
            skipped.append(clip)
            continue
        pieces.append(piece)
        texts.append(records[clip]["text"])
        used.append(clip)
        total += need

    joined = []
    for i, p in enumerate(pieces):
        if i:
            joined.append(gap)
        joined.append(p)
    audio = np.concatenate(joined)
    if skipped:
        print(f"NOTE: dropped {skipped} (would exceed {args.max_seconds}s cap); "
              f"reference text still matches the audio exactly")

    write_wav(args.out, audio)
    ref_text = " ".join(texts)
    meta = {
        "clips": used,
        "level": args.level,
        "sample_rate": SR,
        "duration_s": round(len(audio) / SR, 3),
        "ref_text": ref_text,
        "engine": "omnivoice",
        "weights_licence": "CC-BY-NC (non-commercial) - private audition only",
    }
    args.out.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
