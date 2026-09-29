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
3. **Give it to agents.** VoiceStudio mounts an MCP server at `/mcp` on its local backend
   (`generate_speech`, `clone_voice`, `transcribe`, `list_voices`). Point your agent's MCP config at it and
   bind the saved voice per agent. The voice profile stays inside VoiceStudio's data folder — never in git.
4. **Record the binding by name only.** The card's `Tool profile:` line is the only link. Anyone cloning this repo
   designs their own voice from the same brief.

GPU note from its docs: on Windows, GPU acceleration is NVIDIA/CUDA only; other GPUs run on CPU, much slower.

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
