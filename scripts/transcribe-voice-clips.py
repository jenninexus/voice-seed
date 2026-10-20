"""Transcribe the trailer voice takes and emit word-level timings.

Uses faster-whisper (CPU, int8, small.en) - the same model and settings the
trailer's own `transcribe.py` used, so the wording matches the trailer notes.

The transcript is not only documentation: OmniVoice needs a reference text
that matches the reference audio, and word timings show exactly where the
pops and mouth sounds sit relative to the words.
"""
import json
import re
import sys
from pathlib import Path

from faster_whisper import WhisperModel

# whisper small.en hears these proper nouns as homophones. The clone's
# reference text has to be the words that were actually spoken, so the
# corrections are applied to the transcript rather than left to the model.
NAME_FIXES = [
    (r"\bJenny Stiles\b", "Jenni Styles"),
    (r"\bJenny Styles\b", "Jenni Styles"),
    (r"\bJenny\b", "Jenni"),
    (r"\bfree\s*-\s*to\s*-\s*play\b", "free-to-play"),
    (r"\s+-\s+", "-"),
]


def fix_names(text: str) -> str:
    for pattern, repl in NAME_FIXES:
        text = re.sub(pattern, repl, text)
    return re.sub(r"\s+", " ", text).strip()


def transcribe_dir(src: Path, out_json: Path, model_name: str = "small.en"):
    m = WhisperModel(model_name, device="cpu", compute_type="int8")
    results = []
    for f in sorted(src.glob("V1-*.m4a")):
        segs, info = m.transcribe(str(f), word_timestamps=True, beam_size=5)
        words = [w for s in segs for w in (s.words or [])]
        text = fix_names(" ".join(w.word.strip() for w in words).strip())
        results.append({
            "file": f.name,
            "language": info.language,
            "language_probability": round(float(info.language_probability), 4),
            "duration": round(info.duration, 3),
            "text": text,
            "raw_text": " ".join(w.word.strip() for w in words).strip(),
            "words": [
                {"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2),
                 "prob": round(float(w.probability), 3)}
                for w in words
            ],
        })
        print(f"{f.name}: {text}")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n-> {out_json}")
    return results


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        r"C:\Github\game-dev\games\Dress-Up\Jenni-Styles\Art\audio\trailer")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(
        r"C:\Github\game-dev\games\Dress-Up\Jenni-Styles\Art\audio\omni\transcript.json")
    transcribe_dir(src, out)
