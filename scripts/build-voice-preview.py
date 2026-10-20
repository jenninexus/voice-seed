#!/usr/bin/env python3
"""Build the Jenni Styles voice preview page.

Writes `Art/audio/listen.html`: one page that plays every voice the game has -
the shipped game clips, the cartoon character voice, the trailer voice
restoration ladder (original -> matched -> pop-fix -> clean -> studio) and the
OmniVoice clone renders - so the owner can hear each step and decide what
actually works.

The cartoon voice lives in the voice lab, `voice-seed/private/voices/`. The
builder copies it in as mp3 under `Art/audio/audition/` and reads the line text
from the `jenni-styles` VoiceStudio profile, so the lab stays the source of
truth and this page stays the single place to listen. A subfolder matters: the
Unity staging copy of Art/audio is non-recursive, so none of it can reach the
project or the portal ZIP.

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

# --- The cartoon character voice, which lives in the voice lab ----------------
# The lab (voice-seed/private/voices) holds the VoiceStudio profile SSOTs and
# the engine renders for every voice in the studio. The GAME's page needs the
# cartoon one, so the lab audio is copied in as mp3 under Art/audio/audition/.
# A subfolder matters: the Unity staging copy of Art/audio is non-recursive, so
# nothing here can reach the project or the portal ZIP.
CUTSCENE_TARGETS = [
    ("jenni-01-bedroom-intro.wav", "Morning, Bubbles! Big day today!", "also her"),
    ("jenni-02-school-ready.wav", "Bye, Bubbles! Wish me luck!", "TARGET"),
    ("jenni-03-art-class.wav", "Ta-da! I painted it myself!", "also her"),
    ("jenni-07-stage-song.wav", "Hello, everybody! Let's go!", "reject - noise, no voice"),
]

LAB_SOURCES = [
    # (lab subfolder, label, licence note, badge)
    ("jenni-styles", "OmniVoice", "CC-BY-NC weights - private audition only, never ship", "nc"),
    ("voxcpm2/jenni-styles", "VoxCPM2", "Apache-2.0 weights - the commercial-safe path", "ok"),
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


def sync_lab_audio(lab_dir: Path, dest_dir: Path) -> list[tuple[str, str]]:
    """Copy the cartoon voice out of the voice lab and into the game tree.

    The lab holds the master wavs; the game page needs to play them, so they are
    converted to mp3 under `Art/audio/audition/`. Returns the copied
    (source, destination) pairs so the page can reference them.
    """
    import subprocess

    dest_dir.mkdir(parents=True, exist_ok=True)
    copied: list[tuple[str, str]] = []

    def convert(src: Path, name: str) -> None:
        if not src.exists():
            return
        out = dest_dir / f"{name}.mp3"
        res = subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
             "-ar", "48000", "-codec:a", "libmp3lame", "-b:a", "192k", str(out)],
            capture_output=True)
        if res.returncode == 0:
            copied.append((str(src), f"audition/{name}.mp3"))

    for wav, _line, _kind in CUTSCENE_TARGETS:
        convert(lab_dir / "cutscene-target" / wav, "cutscene-" + wav[:-4])
    for folder, _label, _note, _badge in LAB_SOURCES:
        d = lab_dir / folder
        for wav in sorted(d.glob("*.wav")):
            convert(wav, f"{folder.replace('/', '-')}-{wav.stem}")
    return copied


def cartoon_section(lab_dir: Path, dest_dir: Path) -> str:
    """The cartoon character voice, compiled from the lab."""
    profile = lab_dir / "jenni-styles.voicestudio.json"
    lines: list[str] = []
    if profile.exists():
        spec = json.loads(profile.read_text(encoding="utf-8"))
        lines = list(spec.get("sampleLines", []))

    def has(name: str) -> bool:
        return (dest_dir / f"{name}.mp3").exists()

    target_rows = ""
    for wav, line, kind in CUTSCENE_TARGETS:
        src = f"audition/cutscene-{wav[:-4]}.mp3"
        if not has(f"cutscene-{wav[:-4]}"):
            continue
        badge = ('<span class="badge ok">cartoon target</span>' if kind == "TARGET"
                 else '<span class="badge ok">also her</span>' if kind == "also her"
                 else '<span class="badge nc">reject - noise, no voice</span>')
        target_rows += (
            f'<div class="take"><div class="lbl"><strong>{esc(line)}</strong> {badge}</div>'
            f'<audio controls preload="none" src="{esc(src)}"></audio>'
            f'<span class="file">{esc(src.split("/")[-1])}</span></div>'
        )

    engine_blocks = ""
    missing: list[str] = []
    for folder, label, note, badge in LAB_SOURCES:
        rows = ""
        prefix = "voxcpm2-jenni-styles" if "voxcpm2" in folder else "jenni-styles"
        if "voxcpm2" in folder:
            rows += player(f"audition/{prefix}-identity.mp3",
                           "Identity - the locked reference",
                           "the school-ready performance; every line clones this one")
        for i, line in enumerate(lines, 1):
            name = f"{prefix}-{i:02d}"
            if not has(name):
                missing.append(f"{i:02d}")
                continue
            rows += player(f"audition/{name}.mp3", f"{i:02d} - {line}")
        engine_blocks += (
            f'<h3><span class="eng">{esc(label)}</span> '
            f'<span class="badge {badge}">{esc(note)}</span></h3>'
            f'<div class="takes">{rows}</div>'
        )

    missing_note = ""
    if missing:
        missing_note = (
            f'<p class="note">Lines {esc(", ".join(missing))} (the trailer read for the character) '
            'were never generated - the profile lists them, the engine has not rendered them.</p>'
        )

    return (
        '<h2 id="cartoon">Cartoon voice - the character</h2>'
        '<p class="note">The cartoon Jenni Styles is a <b>different voice</b> from the founder\'s '
        'real voice further down this page. The target is the school-ready cutscene: bright, '
        'sweet, excited, short. Everything after the reference clips is <i>synthesised</i> - the '
        'same lines rendered by two engines, so you can hear which one is the cartoon.</p>'
        '<div class="card">'
        '<strong>jenni-02 school-ready - the performance the voice is locked to</strong>'
        '<span class="note">&ldquo;Bye, Bubbles! Wish me luck!&rdquo; The rejected '
        '&ldquo;Hello, everybody!&rdquo; take is in the reference list below, marked as noise '
        'with no voice - do not match it.</span>'
        '<video controls preload="none" src="../scenes/cutscenes/in-game/jenni-02-school-ready.mp4"></video>'
        '</div>'
        '<h3>The reference clips</h3>'
        f'<div class="takes">{target_rows}</div>'
        f'{engine_blocks}'
        f'{missing_note}'
        '<p class="note">The source of truth for these lines is the VoiceStudio profile '
        '<code>jenni-styles.voicestudio.json</code> in the voice lab; the masters live in '
        '<code>voice-seed/private/voices/audition/</code>.</p>'
    )


def build(audio_dir: Path, report: dict, transcript: list, clone_files: dict,
          cartoon: str = "") -> str:
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
    /* --- Aesyna brand layer. Values copied from the kit, not re-typed by hand:
           syna-theme-kit/css/aesyna.css and syna-theme-kit/tokens/tokens.css.
           The kit forbids @import/symlink/submodule, so the values are inlined. --- */
    @font-face {{ font-family:'Rajdhani'; src:url('../../../Runtime-UI/Fonts/Rajdhani-Bold.woff2') format('woff2');
                 font-weight:700; font-style:normal; font-display:swap; }}
    @font-face {{ font-family:'Lato'; src:url('../../../Runtime-UI/Fonts/Lato-Regular.woff2') format('woff2');
                 font-weight:400; font-style:normal; font-display:swap; }}

    :root {{
      color-scheme: dark;
      --ae-void:#05050c; --ae-surface:#0e0c16; --ae-solid:#100e1c; --ae-raised:#14112a; --ae-well:#0a0918;
      --ae-ink:#e8ecf8; --ae-ink-2:#a3acc6; --ae-ink-3:#7d86a6; --ae-ink-hot:#ffffff;
      --ae-hairline:rgb(255 255 255 / .08);
      --ae-hover-fill:rgb(255 255 255 / .04);
      --ae-rim-panel:inset 0 1px 0 rgb(255 255 255 / .16), inset 0 0 0 1px rgb(255 255 255 / .08);
      --ae-rim-hero:inset 0 1px 0 rgb(255 255 255 / .26), inset 0 0 0 1px rgb(255 255 255 / .13), inset 0 -1px 0 rgb(255 255 255 / .05);
      --ae-lift-float:0 24px 80px -24px #2b2bff66, 0 8px 24px -12px rgb(0 0 0 / .6);
      --ae-panel-fill:linear-gradient(160deg, #17143a 0%, #100e24 38%, #0c0a1c 100%);
      --ae-header-fill:linear-gradient(180deg, rgb(255 255 255 / .045), rgb(255 255 255 / 0) 100%);
      --ae-live-fill:color-mix(in oklab, var(--ae-surface) 72%, transparent);
      --ae-live-filter:blur(22px) saturate(140%);
      --ae-grad:linear-gradient(100deg, #b26bff 0%, #6f7dff 48%, #1fb6ff 100%);
      --ae-r-surface:20px; --ae-r-component:14px; --ae-r-control:10px; --ae-r-chip:6px;
      --ae-focus-ring:2px solid var(--accent-cyan); --ae-focus-offset:2px;
      --ae-floor:
        radial-gradient(60vmax 50vmax at 18% 12%, #4c1d95aa, transparent 60%),
        radial-gradient(55vmax 55vmax at 85% 30%, #1d4ed877, transparent 62%),
        radial-gradient(60vmax 40vmax at 50% 100%, #0e7490aa, transparent 60%),
        var(--ae-void);
      --motion-fast:150ms; --motion-normal:300ms; --motion-slow:500ms;
      --motion-ease:cubic-bezier(0.4, 0, 0.2, 1);
      --font-display:'Rajdhani','Outfit',system-ui,sans-serif;
      --font-body:'Lato','Outfit',ui-sans-serif,system-ui,sans-serif;
      --font-mono:ui-monospace,'JetBrains Mono',Consolas,monospace;
      --ok:#5dffc1; --warning:#ffd166; --error:#ff6b8b;
    }}

    /* --- The Dress-Up brand identity, from syna-theme-kit/profiles/dressup.json (dark).
           Declared on <body>, not :root: the kit's rule is that a flavour's custom
           properties must inherit their COMPUTED value, or one product's surface
           silently renders another product's glass. --- */
    body {{
      --bg:#08060e; --bg-elevated:#262030;
      --accent-pink:#ff2d95; --accent-purple:#b24bf3; --accent-cyan:#00e5ff;
      --text-primary:rgba(255,255,255,.92); --text-secondary:rgba(255,255,255,.65);
      --text-muted:rgba(255,255,255,.55);
      margin:0; font:16px/1.55 var(--font-body); color:var(--text-primary);
      background:var(--bg); min-height:100vh;
    }}
    /* The floor the glass is glass TO. Painted once, never animated. */
    body::before {{ content:''; position:fixed; inset:0; z-index:-1; background:var(--ae-floor); }}

    * {{ box-sizing:border-box; }}
    main {{ max-width:56rem; margin:0 auto; padding:1.75rem 1.25rem 4rem; }}

    h1 {{ font:700 2rem/1.15 var(--font-display); letter-spacing:.02em; margin:0 0 .4rem;
         background:var(--ae-grad); -webkit-background-clip:text; background-clip:text; color:transparent; }}
    h2 {{ font:700 1.2rem/1.3 var(--font-display); letter-spacing:.04em; margin:2.4rem 0 .6rem;
         padding-bottom:.45rem; border-bottom:1px solid var(--ae-hairline); }}
    h3 {{ font:700 1.05rem/1.3 var(--font-display); margin:1.5rem 0 .35rem; }}
    h4 {{ font:700 .82rem/1.3 var(--font-display); margin:1.2rem 0 .35rem; color:var(--accent-cyan);
         text-transform:uppercase; letter-spacing:.12em; }}
    p, li {{ color:var(--text-secondary); }}
    a {{ color:var(--accent-cyan); text-decoration-color:rgb(0 229 255 / .4); text-underline-offset:.18em; }}
    a:hover {{ text-decoration-color:var(--accent-cyan); }}
    a:focus-visible, button:focus-visible {{ outline:var(--ae-focus-ring); outline-offset:var(--ae-focus-offset); border-radius:var(--ae-r-chip); }}
    code {{ background:var(--ae-well); border:1px solid var(--ae-hairline); padding:.08em .38em;
            border-radius:var(--ae-r-chip); font-family:var(--font-mono); font-size:.88em; color:var(--text-primary); }}

    /* Static glass - the default panel. No backdrop-filter: costs nothing per frame. */
    .card, .clip {{ background:var(--ae-panel-fill); box-shadow:var(--ae-rim-panel), var(--ae-lift-float);
                    border-radius:var(--ae-r-surface); padding:.9rem 1.05rem; margin:.6rem 0; }}
    .clip {{ border-left:3px solid var(--accent-pink); }}
    /* Children of a glass surface use fills and dividers, never nested glass. */
    .take {{ background:var(--ae-well); box-shadow:inset 0 0 0 1px var(--ae-hairline);
             border-radius:var(--ae-r-component); padding:.55rem .7rem; }}
    .take:hover {{ background:color-mix(in oklab, var(--ae-well) 88%, var(--accent-cyan)); }}
    .take .lbl {{ display:flex; flex-wrap:wrap; gap:.5rem; align-items:baseline; }}
    .take strong {{ color:var(--text-primary); }}

    .note {{ display:block; font-size:.9rem; color:var(--text-secondary); }}
    .file {{ display:block; font-size:.76rem; color:var(--text-muted); font-family:var(--font-mono); }}
    .metric {{ display:block; font-size:.78rem; color:var(--ok); font-family:var(--font-mono); }}
    .line {{ font-style:italic; color:var(--text-primary); margin:.25rem 0 .7rem; }}
    .takes {{ display:grid; gap:.55rem; }}
    .eng {{ font-weight:700; letter-spacing:.02em; }}
    .badge {{ font-size:.7rem; border-radius:var(--ae-r-pill); padding:.14rem .6rem; white-space:nowrap;
              vertical-align:middle; }}
    .badge.ok {{ color:var(--ok); background:color-mix(in oklab, var(--ok) 15%, transparent); }}
    .badge.nc {{ color:var(--warning); background:color-mix(in oklab, var(--warning) 15%, transparent); }}
    video {{ width:100%; margin-top:.5rem; border-radius:var(--ae-r-control); }}
    audio {{ width:100%; margin-top:.45rem; border-radius:var(--ae-r-control); }}

    /* Live glass - hero layer only. Solid fill is the BASE; the blur rides inside @supports. */
    .banner {{ background:var(--ae-panel-fill-raised); box-shadow:var(--ae-rim-hero), var(--ae-lift-float);
               border-radius:var(--ae-r-component); padding:.85rem 1rem; margin:1rem 0; }}
    @supports (backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px)) {{
      .banner {{ background:var(--ae-live-fill); -webkit-backdrop-filter:var(--ae-live-filter);
                backdrop-filter:var(--ae-live-filter); }}
    }}

    ul.toc {{ columns:2; list-style:none; padding:0; margin:1rem 0 0; }}
    ul.toc li {{ margin:.15rem 0; }}

    @media (prefers-reduced-motion:no-preference) {{
      .take, a {{ transition:background var(--motion-fast) var(--motion-ease), color var(--motion-fast) var(--motion-ease); }}
    }}
    @media (prefers-reduced-motion:reduce) {{ * {{ transition:none !important; animation:none !important; }} }}
    @media (forced-colors:active) {{
      .card, .clip, .take, .banner {{ background:Canvas; border:1px solid CanvasText; box-shadow:none; }}
      h1 {{ color:CanvasText; background:none; }}
    }}
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
    <li><a href="#cartoon">Cartoon voice (the character)</a></li>
    <li><a href="#trailer">Trailer voice - restoration ladder</a></li>
    <li><a href="#clone">Clone of the founder's real voice</a></li>
  </ul>

  <div class="banner">
    <p class="note"><b>Read this first.</b> There are <b>two different Jenni voices</b> on this
    page, and they are not interchangeable. The <b>cartoon</b> voice is the character - bright,
    sweet and short, locked to the school-ready cutscene. The <b>founder</b> voice is a real
    recording, and the ladder below is that recording cleaned up. Founder Jenni is also the real
    person behind the character, which is exactly why the two must never be crossed: a
    <code>jenni-designed</code> clip or a clone of her real voice is <b>not</b> the cartoon
    Jenni Styles voice, and must never be used as it.</p>
  </div>

  <h2 id="game">Game clips - the ones the game plays</h2>
  <p class="note">These are the shipped lines. They stream from <code>Art/audio</code> and are not
    part of the initial load.</p>
  {game_rows}

  {cartoon}
  <h2 id="trailer">Trailer voice - restoration ladder</h2>
  <p class="note">Five <b>founder</b> takes recorded for the trailer, on a phone. The mic caught
    the mouth sounds and the pops, so they were restored before anything else was done with them.
    The ladder is the same audio at four settings, so you can hear exactly what each step does.
    The <b>Matched level</b> row is the fair baseline: it is the untouched recording with only the
    loudness changed, which is what makes the difference you hear the <i>processing</i> and not
    the volume. The numbers under each player are measured, not guessed: plosive events found,
    signal-to-noise ratio before and after, and the noise floor. The final level is
    <b>-16 LUFS / &le;-1 dBTP</b>, which is the house spec from
    <a href="../../../Docs/TRAILER-PLAN.md">TRAILER-PLAN.md</a>.</p>
  {ladder}

  {clone}
</main>
<footer class="note" style="margin:2.5rem auto 0;max-width:56rem;padding:1rem 1.25rem 3rem;color:var(--text-muted);font-size:.78rem;">
  Dark theme: the Aesyna brand layer (<code>syna-theme-kit/css/aesyna.css</code>,
  <code>tokens/tokens.css</code>) with the Dress-Up identity from
  <code>syna-theme-kit/profiles/dressup.json</code> &rarr; <code>dark</code>. Glass, rim, floor,
  radii and motion are the kit's; the brand colours and the type are the game's. Type is the
  project's own OFL Rajdhani and Lato.
</footer>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--lab-dir", type=Path,
                    default=Path(r"C:\Github\voice-seed\private\voices"),
                    help="the voice lab. When given, the cartoon character voice is copied in "
                         "and compiled into the page (default: this repo's private/voices)")
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

    cartoon = ""
    if args.lab_dir and args.lab_dir.is_dir():
        copied = sync_lab_audio(args.lab_dir / "audition", audio_dir / "audition")
        cartoon = cartoon_section(args.lab_dir, audio_dir / "audition")
        print(f"synced {len(copied)} lab clips into {audio_dir / 'audition'}")

    page = build(audio_dir, report, transcript, clone_files, cartoon)
    args.out.write_text(page, encoding="utf-8")
    print(f"wrote {args.out} ({len(page)} bytes, {len(clone_files)} clone clips)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
