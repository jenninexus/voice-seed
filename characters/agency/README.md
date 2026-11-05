# Agency agents — fictional loft crew

**Family:** agency · **Shared loft:** `agency/docs/STUDIO-VOICE.md`  
**Discord runtime:** `{bot}/resources/agency-profiles.json`

> These are **site-audit + Discord studio characters**. They are **not** the
> human founders. Never use them as résumé voice.

**Presence layers (keep separate):**

| Layer | Register | SSOT |
|-------|----------|------|
| Audit / lore personality | `agencyAudit` | Public base `agency/agents/<Name>.md`, plus the consuming project's overlay or independent roster when present |
| Shared loft rules | `agencyStudioShared` | `agency/docs/STUDIO-VOICE.md` |
| Discord loft face + samples | `agencyDiscordChat` | Selected profile's `chatVoice`; a bot's `{bot}/resources/agency-profiles.json#chatVoice` is a runtime consumer |
| Portraits / clips | (media, not voice) | consuming site media trees |

`/voice-design agency <Agent>` edits the voice layers. Seed:
[`../../templates/agent-chatVoice.seed.md`](../../templates/agent-chatVoice.seed.md).

---

## Roster (quick matrix)

| Agent | Accent | Energy | Audit sheet | Chat catalogue |
|---|---|---|---|---|
| **Vidette** | Cyan `#66c0f4` | Calm collector | `agency/agents/Vidette.md` | `agency-profiles.json#vidette` |
| **Bloggie** | Gold `#FFB020` | Warm editor | `agency/agents/Bloggie.md` | `#bloggie` |
| **GraphViz** | Purple `#A563D1` | Color scientist | `agency/agents/GraphViz.md` | `#graphviz` |
| **GamerGirl** | Pink `#FF2E88` | Competitive hype | `agency/agents/GamerGirl.md` | `#gamergirl` |
| **DivineDesign** | Teal `#00D4AA` | Elegant architect | `agency/agents/DivineDesign.md` | `#divinedesign` |
| **Metrica** | Neon green `#39ff14` | Data night-owl | `agency/agents/Metrica.md` | `#metrica` |
| **Vixel** | Orange `#FF6B4A` | Lone-wolf builder | `agency/agents/Vixel.md` | `#vixel` |

Full shared attributes → agency `docs/STUDIO-VOICE.md`.  
Portrait lore → agency `docs/AGENT-GUIDE.md` · `docs/ART-STYLE.md`.

---

## Two-layer depth

| Layer | Where |
|---|---|
| Public origin | `agency/agents/*.md` — personality, catchphrase, chatVoice summary |
| Project override | The consumer's `storage/agency/projects/<project>/<Name>.md` (gitignored in Agency); independent rosters stay with their project |
| Discord runtime | `{bot}/resources/agency-profiles.json` — face, emoji, reply samples |

---

## Customize

`/voice-design agency <Agent>` resolves the public base and applicable project profile. Edit the
owning profile; update a bot catalogue only when that bot consumes the changed register, and verify
the reader. Written register, planned spoken brief and approved audio are separate. A character
registry may index visual references and voice pointers, but remains optional and does not own the
underlying profile or register.
Cross-repo flow: [`../../docs/PROTOCOL.md`](../../docs/PROTOCOL.md) **Flow C**.
