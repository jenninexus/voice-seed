# Spoken voice — outside the register map

voice-seed maps **writing** voice: which register owns a sentence. A character's
**spoken** voice (TTS, cloning, dubbing) is a different job with different risks.
This page marks the boundary so the two never blur.

| | Writing register (this repo) | Spoken voice (elsewhere) |
|---|---|---|
| What it is | Tone, cadence, word choice | Timbre, pitch, accent, a synthesized or cloned voice |
| Where it lives | `registry.json` → owning SSOT | Your TTS tool and its private voice profiles |
| Safe to publish? | Pointers and seeds, yes | Descriptions only — **never** reference audio or voice profiles |

## Rules

1. **No audio in this repo.** No reference recordings, cloned voice profiles,
   embeddings, or model outputs. A voice sample is biometric data; it belongs in a
   private store you control.
2. **Describe, don't capture.** A character card may carry a short, public-safe
   *spoken voice brief* ("warm alto, unhurried, light rasp"). That brief is prose,
   so the character's writing register still governs how it is worded.
3. **Consent before cloning.** Clone only a voice whose owner agreed, and record
   that agreement where the profile lives — not here.
4. **Link, never vendor.** Point at external tools. Copying their code into this
   MIT repo can change its license.

## Tools

- **[VoiceStudio](https://github.com/debpalash/VoiceStudio)** — local-first,
  open-source voice cloning, text-described **voice design**, dubbing, dictation
  and transcription, with a local API and an MCP server so agents can speak in a
  chosen voice. **AGPL-3.0:** use it as a separate app; do not copy its code here.
  ⚠ **The app is free; the models have their own licences.** VoiceStudio's default engine, OmniVoice, has
  Apache-2.0 code but **CC-BY-NC (non-commercial) pretrained weights**, and its audio tokenizer carries separate
  community-licence terms. Use it for private auditions only. For anything commercial (a brand, a paid product, a
  monetised channel), pick an engine whose *weights* allow it. **VoxCPM2** is Apache-2.0 for code and weights, and it
  also designs voices from a text description. Read the model card before release; licences change. Checked 2026-09-30.
- **Models and weights.** See [Models we have tried](#models-we-have-tried) below.
- **Ports.** If VoiceStudio runs for this map, keep it off its stock port 3900 so it never collides with a desktop
  install. The keys are in [`.env.example`](../.env.example) (`VOICESTUDIO_PORT`, `VOICESTUDIO_TUNNEL_PORT`).

## Use it with a character

1. **Write a brief on the card.** Add an optional section to the character's card (e.g. `characters/<group>/<id>.md`):

   ```markdown
   ## Spoken voice (brief)
   warm alto · unhurried · slight rasp on low notes · smiles through vowels · no uptalk
   Tool profile: <name you gave it in your TTS tool — a label, not a file>
   ```

   Keep it to texture words and pacing. It is public-safe prose, worded in the character's own register.
2. **Design the voice** in VoiceStudio's *Voice design* workspace: paste the brief as the description,
   generate, keep the take you like as a saved voice. Or *Voice cloning* from a consenting speaker's clean clip.
   ⚠ Design mode hears **tags only**: gender, age, pitch, whisper, English accent. Texture words
   ("warm", "rasp") come back as *unmatched* and are dropped. Carry pace with the generation speed setting,
   carry texture in how the script is written.
   API save: `POST /profiles` (multipart form: `kind=design`, `vd_states` JSON, `instruct` tags, `seed`) on the
   local backend (default port 3900).
   ⚠ **A saved design voice is its sample line.** On save, VoiceStudio renders the sample line (`ref_text`) once,
   at a fixed preview seed rather than the profile's `seed`. Every later generation with that profile copies
   that one clip. To audition a different speaker, change the sample line, delete the profile and save it again.
   Changing `seed` does nothing. Measure the saved clip's loudness against your other voices: a quiet clip passes
   VoiceStudio's blank-audio check but makes every line near-silent. Seen 2026-09-30 on VoiceStudio 0.5.6: one
   sample line rendered at RMS ~600 against ~3,500 for the others. A new line fixed it.
3. **Give it to agents.** VoiceStudio mounts an MCP server at `/mcp` on its local backend
   (`generate_speech`, `clone_voice`, `transcribe`, `list_voices`). Point your agent's MCP config at it and
   bind the saved voice per agent. The voice profile stays inside VoiceStudio's data folder — never in git.
4. **Record the binding by name only.** The card's `Tool profile:` line is the only link. Anyone cloning this repo
   designs their own voice from the same brief.

GPU note from its docs: on Windows, GPU acceleration is NVIDIA/CUDA only; other GPUs run on CPU, much slower.

## Models we have tried

VoiceStudio is the app. The voice comes from an **engine**, and each engine downloads its own **weights** under its
own licence. The app's licence (AGPL-3.0) says nothing about whether you may publish what a model says: the
**weights** licence does. Check the model card again before any release; licences change.

| Engine (VoiceStudio id) | Weights to download | Size on disk | GPU memory | Code licence | **Weights licence** | Public / commercial use? | Clone from a recording | Design from a description |
|---|---|---|---|---|---|---|---|---|
| OmniVoice (`omnivoice`, default) | [`k2-fsa/OmniVoice`](https://huggingface.co/k2-fsa/OmniVoice), 0.6B params | ~2.6 GB | ≥ 6 GB (VoiceStudio's floor) | Apache-2.0 | **CC-BY-NC** (non-commercial). Its audio tokenizer adds Boson Higgs Audio 2 / Llama community terms | **No.** Private auditions only | ✅ (uses up to 20 s) | ✅ tags only: gender, age, pitch, whisper, English accent |
| VoxCPM2 (`voxcpm2`) | [`openbmb/VoxCPM2`](https://huggingface.co/openbmb/VoxCPM2), 2B params: `model.safetensors` 4.6 GB + `audiovae.pth` 0.4 GB | ~5 GB weights + ~5 GB engine environment (CUDA PyTorch) | ~8 GB (model card); loads in bf16 at ~5.5 GB on an 8 GB RTX 3070. **Loading also takes ~10 GB of system RAM** | Apache-2.0 | **Apache-2.0** | **Yes**, with the usual AI-voice disclosure | ✅ (uses the first 30 s) | ✅ free-text description, 48 kHz output, 30 languages |

Where to get them: VoiceStudio downloads the weights on first use. OmniVoice ships with the app. VoxCPM2 installs from
**Model Catalogue → VoxCPM2 → Install** (or `POST /engines/sidecar/voxcpm2/install` on the local backend) into its own
Python environment under VoiceStudio's data folder. VoiceStudio unloads the previous engine before loading the next,
so the two never share the GPU.

Install traps seen on Windows (2026-09-30, VoiceStudio 0.5.6): when the backend runs over ssh or as a background
process, `uv` cannot read its own managed Python installs (`os error 448`), so the one-click install fails at
"create venv". Start the backend with `UV_PYTHON_PREFERENCE=only-system`, and if another Python on `PATH` trips the
same error, pre-create the engine's `.venv` with an explicit system Python (3.10–3.12) and click Install again. A
machine memory guard can also kill the engine while it loads, which VoiceStudio reports only as "sidecar closed pipe
mid-generate": check free system memory first.

Checked against both model cards on 2026-09-30. An earlier note in this repo called OmniVoice "Apache-2.0": that is
true of its code only, not its weights.

**Cloning a real person** (your own voice included) is the same mechanism as above with a reference recording. Do it
only with that person's recorded consent, and keep the recording and the saved voice out of every repo. Hosted
services (for example ElevenLabs instant / professional voice cloning) also work; read their commercial terms per plan.

## Restoring a recording before you clone it

**A synthesis engine cannot repair audio.** OmniVoice and VoxCPM2 take a reference recording and
reproduce a *voice*; neither de-clicks, de-esses, de-noises or de-plosives anything. They clone
whatever you hand them, artefacts included. A reference that still has the lip pops and the mouth
sounds teaches the model those sounds, and every line it says afterwards carries them.

So the order is always: **restore the recording first, then clone the restored audio.** The tools
below live in `scripts/` and hold no audio.

| Script | Does |
|---|---|
| `scripts/restore-voice-clip.py` | The restoration chain: high-pass, de-click, spectral transient suppression (plosives *and* mouth sounds, detected separately), spectral gating against a gap-derived noise profile, de-esser, gentle compression, loudness normalisation. `--analyze` reports measurements, `--spectrogram` writes a PNG so the artefacts are seen, not guessed. |
| `scripts/restore-trailer-set.ps1` | Runs the chain over a folder of clips at four settings and writes the measurement table. |
| `scripts/transcribe-voice-clips.py` | faster-whisper (small.en, CPU) word-level transcript. A clone's reference text must match the audio exactly, and the transcript is what makes that checkable. |
| `scripts/build-voice-reference.py` | Assembles restored clips into a clone reference that fits the engine's cap, with the matching transcript. |
| `scripts/normalize-clone-renders.py` | Puts every rendered line at the same loudness, so a difference in level is never mistaken for a difference in voice. |
| `scripts/build-voice-preview.py` | Builds the audition page: every clip, every setting, side by side. |

**The three settings, and why they are separate.** "Cleaned" is a dial, not a switch:

- **popfix** — de-click, tame the plosives, de-ess. Room tone and mouth sounds left alone.
- **clean** — popfix plus spectral denoising and a gap expander.
- **studio** — the most processing. This is what a clone reference should be built from.

Always keep a **level-matched but otherwise untouched** copy of the original next to them. Without
it, the loudness change masquerades as an improvement and the A/B proves nothing.

**Measured on the five Jenni Styles trailer takes (2026-10-19).** Phone recordings, 44.1/48 kHz mono
AAC, room noise around -46 to -59 dBFS, plosive bursts on the P/B/T consonants. The chain took the
plosive events from 3-8 per clip down to 0-2, lifted SNR by 4 to 28 dB, dropped the noise floor by
up to 24 dB, and landed every clip at -16 LUFS / <= -1 dBTP — the house spec in the Dress-Up
`TRAILER-PLAN.md`. The full measurement table is in the game's
`Art/audio/omni/restoration-report.json`.

**OmniVoice constraints, found the hard way (2026-10-19, VoiceStudio 0.5.6):**

| Constraint | Consequence |
|---|---|
| Reference audio caps at **20.0 s** (`CLONE_REF_TEXT_MAX_SECONDS`) | A longer reference is rejected. Build the reference to fit — and drop a clip whole rather than trimming it mid-sentence, because a half-clip makes the reference text disagree with the reference audio, and a mismatched pair is the quietest way to ruin a clone. |
| Reads the reference at **24 kHz** | Write references at 24 kHz so nothing is resampled inside the model. |
| `ref_text` must match the audio | Pass the transcript explicitly. Omitting it makes VoiceStudio transcribe at save time from *already-installed* ASR models only; with none installed it stays blank and the first take inherits stray words from the reference. |
| Mid-silences over 300 ms are stripped from the reference | Long gaps between sentences are fine — the model removes them. |
| Clone profile: `POST /profiles` multipart, `kind=clone`, `ref_audio` + `ref_text` | The save is the clone. `POST /generate` with `profile_id` then re-uses that sample for every line. `seed` changes the take; it does not change the speaker. |

**Never publish a person's clone.** The
[`omnivoice-gallery`](https://github.com/debpalash/omnivoice-gallery) submodule in the VoiceStudio
checkout is a **community content catalogue** — the app loads it from a CDN and it accepts
contributed *recorded reference clips*. It is a publishing surface. A founder's clone stays on a
private machine, and the OmniVoice weights are CC-BY-NC besides.

**Where the results live.** The Jenni Styles trailer work is the worked example: the restoration
ladder, the clone renders and the measurements are in the game's
`Jenni-Styles/Art/audio/omni/`, with the audition page at
`Jenni-Styles/Art/audio/listen.html` (private LAN repo, never a portal build — the Unity staging
copy is non-recursive and takes only the top-level game clips). Consent is logged in
`private/voices/CONSENT.md`.

**The lab lives here, in `private/`.** The VoiceStudio profile SSOTs, the clone-consent ledger and
the engine renders are `private/voices/` in **this** repo — gitignored, never pushed, because a
voice sample is biometric data. It moved there from `pdf-designer/profiles/voices/` on 2026-10-20:
pdf-designer owns *written* voice (personality and résumé prose), and spoken voice is a different
job with different risks. The lab's own audition page is `private/voices/audition/listen.html`
(`listen.ps1` opens it); the **game's** voices are compiled into the game's own page instead, so
auditioning the game never means opening a second tab.

## Forking VoiceStudio

Forking is allowed. It is AGPL-3.0-only (see its `LICENSE-NOTICE.md`). A fork you customize must:

- **Keep** `LICENSE` (verbatim AGPL-3.0) and `LICENSE-NOTICE.md`, and every existing copyright notice.
- **Say it is modified:** a line at the top of the fork's README, e.g.
  *"Fork of [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) (AGPL-3.0), modified by <you>, <date>."*
  Mark changed files or keep a changelog of your changes (AGPL §5a).
- **Stay AGPL-3.0.** Your changes are licensed the same way. If you run the modified app **as a network service**
  others use, you must offer them its source (AGPL §13). Private local use carries no publishing duty.
- **Mind the separate licences.** The bundled `omnivoice/` package is Apache-2.0; downloaded model weights have their
  own terms (the default OmniVoice weights are CC-BY-NC — non-commercial).
- **Name and logo:** the licence covers code, not the brand. A published fork should not present itself as the
  official app — give it its own name (e.g. "<you>'s VoiceStudio fork") and credit the original.

This repo only **links** to VoiceStudio or a fork of it, so voice-seed stays MIT.
