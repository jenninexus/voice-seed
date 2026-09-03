# AGENTS.md — voice-seed capability map

Vendor-neutral map of writing voices. Any assistant should drive voice work from
this page + `/voice-design`.

Human-facing overview: [`README.md`](README.md). Register rules:
[`docs/REGISTERS.md`](docs/REGISTERS.md). Cross-repo flow:
[`docs/PROTOCOL.md`](docs/PROTOCOL.md). Clone contract:
[`docs/PUBLIC-LOCAL-SPLIT.md`](docs/PUBLIC-LOCAL-SPLIT.md).

## What this repo is

**A register map + seed templates — not the prose SSOT.**

Deep voice content lives in owning repos. This repo indexes *which* register
applies and *where* to edit. Never paste résumé claims, contacts, or Patreon
drafts here.

| Register | Owns | Edit here? |
|---|---|---|
| `character` | Who they are (personality, contrast) | No — pointer only → `pdf-designer/storage/users/<id>.json#characterVoice` |
| `application` | Résumé / cover-letter prose | No → vault `#voice` (+ optional `#mission`) |
| `socialMarketing` | Patreon / Discord / news | No → `socials/content/<brand>/format-manifest.json` |
| `botGreeter` | Join-welcome prose | No → `{bot}/content/greeting.md` |
| `discordVisual` | Embed chrome / emoji IDs | No → `{bot}/docs/STYLE-SPEC.md` + `assets.json` |
| `agency*` | Loft audit + Discord chat | No → `agency/agents/*.md` + `STUDIO-VOICE.md` + `{bot}/resources/agency-profiles.json` |
| `gameSecurityChat` | Game Discord triage | No → game wiki persona (card: `characters/ops/gub.md`) |
| `signalTone` | NEOPHI Signal Crew in-character updates | **Yes** — `characters/neophi/<id>.md` (Visual DNA stays in neophi `characters.md`) |
| map / seeds | Index + templates | **Yes** — `registry.json`, `characters/`, `templates/` |

## Commands

| Invoke | Where | Purpose |
|---|---|---|
| `/voice-design` | This repo (`.claude/commands/`) | Resolve register → open SSOT → edit safely |
| `/make-resume` | `pdf-designer` | Application register (after loading character) |

## First file to open

[`registry.json`](registry.json), then [`docs/REGISTERS.md`](docs/REGISTERS.md)
if the task crosses registers.

## Hard rules

1. **Register before prose.** Name the register before writing a sentence.
2. **Edit the owning SSOT**, not a copy in this repo — **exception:** NEOPHI
   `signalTone` cards under `characters/neophi/` *are* the speaking SSOT.
3. **Agency ≠ humans.** Loft agents never bleed into applications. Humans never
   become loft mascots in Patreon copy.
4. **Ops ≠ Agency ≠ marketing.** Triage is zero role-play / zero emoji; never
   put logins in Discord.
5. **No Discord emoji / slang on ATS PDFs.** Application register stays clean.
6. **Studio “we” ≠ solo applicant.** Marketing voice ≠ résumé voice.
7. **Privacy.** No vault claims, phones, emails, webhooks, or private drafts in this repo.

## When socials drafts ask for voice

1. Open `registry.json` → brand entry.
2. Confirm register = `socialMarketing`.
3. Edit `socials/content/<brand>/format-manifest.json` → `patreon_format.voice`.
4. Do **not** dump `characterVoice`, greeter, Agency `chatVoice`, or NEOPHI
   `signalTone` into default brand Patreon unless the post is explicitly in-character.

## When NEOPHI Signal Crew asks for voice

1. Register = `signalTone` → `/voice-design neophi <nyx|zara|kai|luna|orion|phoenix>`
2. Edit `characters/neophi/<id>.md` (cadence / update hooks / samples)
3. Visual DNA / tokens → `neophi/src/assets/data/characters.md` first
4. Site deck: `https://neophi.world/?character=<id>#gallery`

## When bot greeters / Agency Discord ask for voice

1. Greeter → register `botGreeter` → `{bot}/content/greeting.md`.
2. Agency loft → `agencyAudit` + `agencyDiscordChat` (two layers — see PROTOCOL Flow C).
3. Chrome/emoji IDs → `discordVisual`, not prose.
4. Theme kits supply colors only — never treat them as voice SSOTs.

## When résumés ask for voice

1. Register = `character` + `application` (some tracks also load `#mission`).
2. Follow `/make-resume` step **0b** in pdf-designer — this repo only confirms
   the pointer paths.

## Repo map

| Path | Role |
|---|---|
| `registry.json` | Machine index of every voice |
| `docs/REGISTERS.md` | Hard separation rules |
| `docs/PROTOCOL.md` | socials ↔ bots ↔ agency posting flow |
| `docs/ROADMAP.md` | Map / router next work |
| `docs/OVERVIEW.md` | Narrative map |
| `docs/PUBLIC-LOCAL-SPLIT.md` | Clone vs studio-only |
| `characters/humans/` | Human index cards (pointers) |
| `characters/brands/` | Brand marketing pointers |
| `characters/bots/` | App greeter / bot face pointers |
| `characters/agency/` | Agency layer pointer |
| `characters/ops/` | Game security voices |
| `templates/` | Seed shapes for new voices |
| `.claude/commands/voice-design.md` | Repo-local procedure |
| `Plans/` | Session handoff (replaces a local sego yaml) |

## Related

- pdf-designer: `AGENTS.md`, `/make-resume`, vault docs
- socials: format-manifest marketing voice
- agency: `docs/STUDIO-VOICE.md`
- consuming bot: `resources/agency-profiles.json`
- **Packaging (studio hub, not this clone):** product-design `/products` · `SEED-FAMILY.md` · `VOICE-SEED.md`. Sequence plan stays there. GitHub is public; do not copy hub plans into this repo.
