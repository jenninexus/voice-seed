# Public vs local split — voice-seed

This repository is the **writing-register map**. It is not a second copy of résumé
claims, Patreon drafts, Discord webhook URLs, or Agency loft lore.

**GitHub:** [`jenninexus/voice-seed`](https://github.com/jenninexus/voice-seed)
is **public** (2026-09-03). History is a single clean snapshot. Agency remains
useful without this repo.

## Track (clone-safe)

- `registry.json` — relative `ssotPattern` paths only (`agency/agents/<Name>.md`, `{bot}/…`)
- `docs/REGISTERS.md` · `docs/PROTOCOL.md` · `docs/OVERVIEW.md`
- `docs/PUBLIC-LOCAL-SPLIT.md` (this file) · `docs/PRODUCT.md`
- `characters/agency/` — pointers to Agency prose, not a second SSOT
- `templates/agent-chatVoice.seed.md` · `templates/character-voice.seed.json`
- `AGENTS.md` · `README.md` — no machine-absolute disks, no emails, no legal names
- `docs/ROADMAP.md` — the public roadmap (session plans are local, see below)
- `docs/SPOKEN-VOICE.md` — spoken-voice boundary, how-to, and fork attribution for external TTS tools
- `.claude/commands/voice-design.md` — the **one** command; other agents read it via `AGENTS.md`. `CLAUDE.md` is a pointer to `AGENTS.md`
- Fictional public-safe cards (e.g. NEOPHI Signal Crew) if they stay pointer-or-in-character with no private URLs

## Keep local / strip before public

Never ship these on a public `main`:

| Kind | Examples |
|------|----------|
| Absolute disks | Windows drive-letter clones, user-profile trees, finance folders |
| Human PII | Legal names, personal emails, operator-platform identity |
| Studio-only registers | Handshake / investor / collab cards — Handshake hub `Voice/` only, never this repo |
| Secrets | `.env`, webhooks, vault claims, analytics IDs |
| Session plans | `Plans/` (gitignored) — studio work notes; the clone gets `docs/ROADMAP.md` instead |
| Session logs | `dev-log-*.yaml` — retired; do not recreate |
| Generated agent wrappers | `.codex/`, `.agents/` (gitignored) — rebuilt per machine from the one command |
| Studio overlay | `private/` (gitignored) — see below |

Human personality and application voice stay in **pdf-designer** gitignored vaults.
Brand marketing prose stays in **socials** format-manifests.
Agency *lore* stays in **agency** `agents/*.md`. This repo only **routes**.

## Pairing with Agency (optional)

Clone users:

```text
git clone https://github.com/jenninexus/agency.git
# optional:
git clone https://github.com/jenninexus/voice-seed.git
```

Then copy `voice-seed/templates/agent-chatVoice.seed.md` into `agency/agents/YourAgent.md`.
Do **not** add voice-seed as a git submodule of agency. Do **not** install studio
network-admin tools — those are not product dependencies.

Bot greeter / embed chrome / loft `chatVoice` use relative `{bot}/` paths. A
future Discord-bot seed clone will use the same files. Do not link a GitHub
remote for that seed until it exists.

## Leak belts (keep empty)

Run from the repo root on **tracked** files (exclude `private/`, `node_modules/`):

- [x] No Windows drive-letter paths (`Github`, `Users`, finance `Documents`)
- [x] No legal surnames or personal mailbox addresses
- [x] Handshake / investor / collab cards gitignored or absent (`**/*handshake*` in `.gitignore`)
- [x] README tip footer present; no webhook URLs
- [x] `git status` clean of `.env` / `storage/` / `*.local.md`
- [x] `git log` on public `main` is a single snapshot (orphan rewrite 2026-09-03)

Keep the belts in `.gitignore`. Do not put Handshake / investor / collab cards back.

The pre-public history is kept only as a local archive in `private/archive/2026-09-03-pre-public-overlay/`
(there are no backup branches). `origin` stays the clean snapshot.

## `private/` — the local-private convention

One gitignored folder at the repo root, **visible** on disk (unlike a buried `storage/`), holds everything
studio-only. A public clone simply doesn't have it and works the same.

| Path | Role |
|---|---|
| `private/voice-design.local.md` | Extra `/voice-design` routes; the public command reads it when present |
| `private/studio-voice.md` | Private registers (e.g. investor, creator-collab) |
| `private/VOICE-CONSUMERS.md` | Audit of how sibling repos consume this map |
| `private/archive/` | Frozen history, read-only |

Never a second `.claude/` inside `private/` — overlays are plain files the one command loads.
Any repo that wants the same split can copy this pattern: `private/` + a `*.local.md` overlay the public file reads.
