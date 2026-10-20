#!/usr/bin/env python3
"""Build the Jenni Styles voice preview page.

Writes `Art/audio/listen.html`: one page that plays the game's shipped voice
clips, the trailer voice restoration ladder (original -> matched -> pop-fix ->
clean -> studio) and the OmniVoice clone renders, so the owner can hear each
step and decide what actually works.

The page links to the audio files by relative path. It never embeds them:
base64 audio in a tracked HTML file would bloat the repo, and the game-dev
tree is private-LAN but still a git repository.

Usage:
  python build-voice-preview.py --audio-dir <Art/audio> --out <Art/audio/listen.html>
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
from pathlib import Path

# The ladder, in the order the owner should hear them.
LEVELS = [
    ("original", "Original", "exactly as recorded - nothing touched"),
    ("raw", "Matched level", "same audio, loudness matched to the rest of the page - "
                             "this is the honest baseline, because it isolates the "
                             "processing from the level change"),
    ("popfix", "Pop fix", "de-clicked, plosives tamed, de-essed. Room and mouth "
                          "sounds left alone"),
    ("clean", "Clean", "pop fix plus spectral denoising and a gap expander"),
    ("studio", "Studio", "the most processing. This is what the clone reference "
                         "was built from"),
]

CLONE_SOURCES = [
    ("founder-solo", "V1-4 alone (8.9 s)", "one continuous sentence, no cut points"),
    ("founder-merged", "V1-2 + V1-3 + V1-4 (19.0 s)", "more phonetic coverage, three sentences"),
]

CLONE_LINES = [
    ("compare", "Her own line (V1-2)", "Find her look for each scene, choose her replies, and see her day unfold."),
    ("compare-b", "Her own line, second seed", "Same line, a different seed - how much the voice moves between takes."),
    ("new", "A line she never said", "Oh, that's the one! Now you look ready for the stage."),
    ("short", "Short line", "Thanks for playing Jenni Styles."),
]

GAME_CLIPS = [
    ("let's-go.mp3", "Title Play", "(no new caption)"),
    ("hm-3.mp3", "Wrong look 1", "GameUI.yaml wrongLookLines"),
    ("hmm-2.mp3", "Wrong look 2", "GameUI.yaml wrongLookLines"),
    ("hmmm-1.mp3", "Wrong look 3", "GameUI.yaml wrongLookLines"),
    ("hm-4.mp3", "Wrong look 4", "GameUI.yaml wrongLookLines"),
    ("hmmm-5.mp3", "Wrong look 5", "GameUI.yaml wrongLookLines"),
    ("not-for-tonight.mp3", "Pool suit while she still needs the stage look", "Pretty, but not for tonight."),
    ("ok-this-one-is-perfect.mp3", "She completes the chapter's own look 1", "Perfect Fit stamp"),
    ("ok-this-one-is-perfect-2.mp3", "She completes the chapter's own look 2", "Perfect Fit stamp"),
]


def esc(s: str) -> str:
    return html.escape(str(s))


def player(src: str, label: str, note: str = "") -> str:
    note_html = f'<span class="note">{esc(note)}</span>' if note else ""
    return (
        f'<div class="take"><div class="lbl"><strong>{esc(label)}</strong>{note_html}</div>'
        f'<audio controls preload="none" src="{esc(src)}"></audio>'
        f'<span class="file">{esc(src.split("/")[-1])}</span></div>'
    )


def build(audio_dir: Path, report: dict, transcript: list, clone_files: dict) -> str:
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    by_clip: dict = {}
    for row in report:
        by_clip.setdefault(row["Clip"], {})[row["Level"]] = row

    texts = {t["file"].rsplit(".", 1)[0]: t["text"] for t in transcript}

    # --- game clips -------------------------------------------------------
    game_rows = ""
    for fname, when, caption in GAME_CLIPS:
        p = audio_dir / fname
        if not p.exists():
            continue
        game_rows += (
            f'<div class="card"><strong>{esc(when)}</strong>'
            f'<span class="note">{esc(caption)}</span>'
            f'<audio controls preload="none" src="{esc(fname)}"></audio>'
            f'<span class="file">{esc(fname)}</span></div>'
        )

    # --- restoration ladder ----------------------------------------------
    ladder = ""
    for clip in sorted(by_clip):
        rowset = by_clip[clip]
        base = rowset.get("raw", {})
        before = base.get("SNRbefore", 0)
        floor_before = base.get("FloorBefore", 0)
        plos_before = base.get("Plosives", "")
        plos_before_n = plos_before.split("->")[0].strip() if isinstance(plos_before, str) else ""
        text = texts.get(clip, "")
        cards = ""
        for level, label, note in LEVELS:
            f = audio_dir / "omni" / f"{clip}.{level}.mp3"
            if not f.exists():
                continue
            r = rowset.get(level)
            extra = ""
            if r and level != "original":
                extra = (f'<span class="metric">plosives {esc(plos_before_n)}&rarr;{esc(str(r["Plosives"]).split("->")[-1].strip())}'
                         f' &middot; SNR {esc(str(r["SNRbefore"]))}&rarr;{esc(str(r["SNRafter"]))} dB'
                         f' &middot; floor {esc(str(r["FloorBefore"]))}&rarr;{esc(str(r["FloorAfter"]))} dBFS'
                         f' &middot; {esc(str(r["LUFS"]))} LUFS</span>')
            cards += player(f"omni/{clip}.{level}.mp3", label, note)
            if extra:
                cards += extra
        if not cards:
            continue
        ladder += (
            f'<div class="clip"><h3>{esc(clip)}</h3>'
            + (f'<p class="line">&ldquo;{esc(text)}&rdquo;</p>' if text else "")
            + f'<div class="takes">{cards}</div></div>'
        )

    # --- clone renders ----------------------------------------------------
    clone = ""
    if clone_files:
        rows = ""
        # her real take of the same line, for the A/B
        real = audio_dir / "omni" / "V1-2.original.mp3"
        if real.exists():
            rows += ('<h4>Her real voice, same line</h4>'
                     + player("omni/V1-2.original.mp3", "Recorded take (V1-2)",
                              "the actual recording, untouched"))
        for cid, label, note in CLONE_LINES:
            rows += f'<h4>{esc(label)}</h4>'
            for src_key, src_label, src_note in CLONE_SOURCES:
                for seed in ("s42", "s7"):
                    f = clone_files.get(f"{src_key}.{cid}.{seed}")
                    if not f:
                        continue
                    rows += player(f, f"Clone - {src_label}",
                                   f"{note} (seed {seed[1:]})")
        clone = (
            '<section id="clone"><h2>OmniVoice clone of the founder voice</h2>'
            '<p class="note">These are <b>synthesised</b>, not recorded. OmniVoice cloned the '
            'restored trailer takes and spoke new lines in that voice. '
            '<b>OmniVoice weights are CC-BY-NC</b> - private audition only, never publish, never ship. '
            'The reference audio was the <i>restored</i> clip, so the clone inherits the clean '
            'recording, not the pops.</p>'
            + rows + '</section>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Jenni Styles voice - preview</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {{ color-scheme: light; --ink:#1e1e32; --dim:#61506d; --pink:#db2777; --card:#fff;
             --line:#e4dcec; --ok:#0f7b5f; --warn:#b45309; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font:16px/1.5 "Segoe UI", sans-serif; color:var(--ink); background:#faf8ff; }}
    main {{ max-width:52rem; margin:0 auto; padding:1.5rem 1.25rem 4rem; }}
    h1 {{ font-size:1.7rem; letter-spacing:.03em; margin:0 0 .3rem; }}
    h2 {{ font-size:1.15rem; margin:2.2rem 0 .5rem; padding-bottom:.35rem; border-bottom:1px solid var(--line); }}
    h3 {{ font-size:1rem; margin:1.4rem 0 .3rem; }}
    h4 {{ font-size:.92rem; margin:1.1rem 0 .3rem; color:var(--dim); text-transform:uppercase; letter-spacing:.08em; }}
    p, li {{ color:var(--dim); }}
    a {{ color:var(--pink); }}
    code {{ background:#f1ecfa; padding:.1em .35em; border-radius:4px; font-size:.9em; }}
    .card, .clip {{ background:var(--card); border:1px solid var(--line); border-radius:14px;
                    padding:.8rem 1rem; margin:.55rem 0; }}
    .clip {{ border-left:3px solid var(--pink); }}
    .note {{ display:block; font-size:.88rem; color:var(--dim); }}
    .file {{ display:block; font-size:.78rem; color:#9a8fa8; font-family:ui-monospace,Consolas,monospace; }}
    .metric {{ display:block; font-size:.78rem; color:var(--ok); font-family:ui-monospace,Consolas,monospace; }}
    .line {{ font-style:italic; color:var(--ink); margin:.2rem 0 .6rem; }}
    .takes {{ display:grid; gap:.55rem; }}
    .take {{ border:1px solid var(--line); border-radius:10px; padding:.5rem .65rem; }}
    .take .lbl {{ display:flex; flex-wrap:wrap; gap:.5rem; align-items:baseline; }}
    audio {{ width:100%; margin-top:.4rem; }}
    .banner {{ background:#fff4f8; border:1px solid #f6d3e4; border-radius:12px; padding:.7rem .9rem; margin:.8rem 0; }}
    ul.toc {{ columns:2; }}
  </style>
</head>
<body>
<main>
  <h1>Jenni Styles voice</h1>
  <p class="note">Open this file from disk; no server needed. Rebuilt {esc(stamp)} by
     <code>voice-seed/scripts/build-voice-preview.py</code>. How the game clips map onto play is
     <a href="../../../Docs/AUDIO.md">AUDIO.md</a>.</p>

  <ul class="toc">
    <li><a href="#game">Game clips</a></li>
    <li><a href="#inspiration">Inspiration</a></li>
    <li><a href="#trailer">Trailer voice - restoration ladder</a></li>
    <li><a href="#clone">OmniVoice clone</a></li>
  </ul>

  <div class="banner">
    <p class="note"><b>Read this first.</b> The trailer takes were recorded on a phone and the mic
    caught the mouth sounds and the pops. The restoration ladder below is the same audio at four
    settings, so you can hear exactly what each step does. The
    <b>Matched level</b> row is the fair baseline: it is the untouched recording with only the
    loudness changed, which is what makes the difference you hear the <i>processing</i> and not
    the volume.</p>
  </div>

  <h2 id="game">Game clips - the ones the game plays</h2>
  <p class="note">These are the shipped lines. They stream from <code>Art/audio</code> and are not
    part of the initial load.</p>
  {game_rows}

  <h2 id="inspiration">Inspiration, before these clips</h2>
  <p class="note">The cartoon lock was the school-ready cutscene, &ldquo;Bye, Bubbles! Wish me luck!&rdquo;
    The rejected &ldquo;Hello, everybody!&rdquo; take is not here. Founder Jenni
    (<code>jenni-designed</code>) is a different voice and is not on this page.</p>
  <div class="card">
    <strong>jenni-02 school-ready</strong>
    <video controls preload="none" src="../scenes/cutscenes/in-game/jenni-02-school-ready.mp4"></video>
  </div>

  <h2 id="trailer">Trailer voice - restoration ladder</h2>
  <p class="note">Five founder takes recorded for the trailer. Same words, five settings.
    The numbers under each player are measured, not guessed: plosive events found, signal-to-noise
    ratio before and after, and the noise floor. The final level is
    <b>-16 LUFS / &le;-1 dBTP</b>, which is the house spec from
    <a href="../../../Docs/TRAILER-PLAN.md">TRAILER-PLAN.md</a>.</p>
  {ladder}

  {clone}
</main>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    audio_dir = args.audio_dir
    omni = audio_dir / "omni"
    report = json.loads((omni / "restoration-report.json").read_text(encoding="utf-8"))
    transcript = json.loads((omni / "transcript.json").read_text(encoding="utf-8"))

    # clone renders: omni/clone/<name>.mp3
    clone_files = {}
    clone_dir = omni / "clone"
    if clone_dir.is_dir():
        for f in sorted(clone_dir.glob("*.mp3")):
            clone_files[f.stem] = f"omni/clone/{f.name}"

    page = build(audio_dir, report, transcript, clone_files)
    args.out.write_text(page, encoding="utf-8")
    print(f"wrote {args.out} ({len(page)} bytes, {len(clone_files)} clone clips)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
