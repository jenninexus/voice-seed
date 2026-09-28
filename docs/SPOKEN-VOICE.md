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

A voice brief written for a character card can be pasted into a voice-design tool's
description prompt as-is — that is the whole integration.
