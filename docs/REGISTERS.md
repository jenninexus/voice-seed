# Voice registers — do not conflate

Each **register** is a purpose + an SSOT path. Agents and humans must open the
right file for the job. Mixing registers is how a loft agent starts sounding like
a résumé, or a cover letter starts sounding like Patreon.

---

## Register map

| ID | Purpose | “I” / “we” | SSOT (edit here) | Index card |
|---|---|---|---|---|
| `application` | Résumé + cover letter prose | Applicant as person | pdf-designer `storage/<user>/resume-source.json#voice` | [`../characters/humans/`](../characters/humans/) |
| `character` | Personality, partner contrast, emoji prefs, register pointers | Person | pdf-designer `storage/users/<user>.json#characterVoice` | same |
| `mission` | Owner research / life’s-work spine | Person | pdf-designer vault `#mission` (optional) | [`../characters/humans/shade.md`](../characters/humans/shade.md) |
| `studioResume` | Studio capability **or** games applications | Studio “we” | `studio-resume.json` · `martian-resume.json` | [`../characters/brands/martiangames.md`](../characters/brands/martiangames.md) |
| `socialMarketing` | Patreon / Discord brand posts | Brand or creator | socials `content/<brand>/format-manifest.json` | [`../characters/brands/`](../characters/brands/) |
| `botGreeter` | Join-welcome embed **prose** | App bot face | `{bot}/content/greeting.md` | [`../characters/bots/`](../characters/bots/) |
| `discordVisual` | Bot embed chrome, custom emoji IDs, layout | Brand UI | `{bot}/docs/STYLE-SPEC.md` + `resources/assets.json` | brand / bots cards |
| `agencyAudit` | Site QA character personality | Agent character | `agency/agents/<Name>.md` | [`../characters/agency/`](../characters/agency/) |
| `agencyStudioShared` | Loft attributes every agent shares | Agency crew | `agency/docs/STUDIO-VOICE.md` | agency index |
| `agencyDiscordChat` | Loft channel posters (`chatVoice`, faces) | Agent character | `{bot}/resources/agency-profiles.json` | agency index |
| `gameSecurityChat` | Player-facing game security / triage | Ops — professional CM | Tank Off `Gub-Persona.md` | [`../characters/ops/gub.md`](../characters/ops/gub.md) |
| `signalTone` | NEOPHI Signal Crew in-character lines / updates | Crew member “I” | `characters/neophi/<id>.md` (+ canon in neophi `characters.md`) | [`../characters/neophi/`](../characters/neophi/) |

**Not voice registers:** theme kits (colors & UI tokens). They may supply hex values used by
`discordVisual`; they never own greeter or chat prose. Flow: [`PROTOCOL.md`](PROTOCOL.md).

Bot greeter, embed chrome, and loft `chatVoice` use the same **relative** `{bot}/`
paths whether you run a live bot or a future Discord-bot seed clone. Do not treat
a missing GitHub remote as a broken map.

---

## Hard rules

1. **Agency agents never claim to be the human founders.**
2. **No Discord emoji / hearts on ATS light PDFs.**
3. **Studio marketing “we” ≠ a solo application voice.**
4. **Deepen claims in the vault; deepen personality in `characterVoice`; deepen
   agent lore in agency agents — not in this registry.**
5. **This repo only updates when the map or public overviews change** — not on
   every cover-letter tweak.
6. **Ops ≠ Agency ≠ marketing ≠ greeter.** Zero role-play / emoji for Gub; never
   leak logins. Ops doctrine → game wiki. Greeter → `greeting.md`. Agency
   loft → `agency-profiles.json`. Brand posts → format-manifest.
7. **Agency has two edit layers.** Lore/audit in `agency/agents/*.md`; Discord
   runtime samples/faces in the consuming bot’s `agency-profiles.json`. Keep them
   aligned; do not fork a third copy into voice-seed.
8. **NEOPHI Signal Crew:** Visual DNA + traits stay in neophi `characters.md`.
   Speaking tone for updates lives in `characters/neophi/*.md` (`signalTone`).
   Never dump Signal Crew chat into default brand Patreon unless the post is
   explicitly in-character and routed via `/voice-design neophi <id>`.

---

## How `/make-resume` uses this

1. Resolve user → `character` register (`characterVoice`).
2. Load `application` register (vault `voice` + `leadIdentityByTrack`).
3. Shade Default / AI track → also load `mission`.
4. Ignore `agency*` and `socialMarketing` for prose (inspire only if needed).

Full routine: pdf-designer `.claude/commands/make-resume.md` step **0b**.
