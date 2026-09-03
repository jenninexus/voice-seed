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
- `Plans/` — session handoff (clone-safe; replaces a local sego yaml)
- Fictional public-safe cards (e.g. NEOPHI Signal Crew) if they stay pointer-or-in-character with no private URLs

## Keep local / strip before public

Never ship these on a public `main`:

| Kind | Examples |
|------|----------|
| Absolute disks | Windows drive-letter clones, user-profile trees, finance folders |
| Human PII | Legal names, personal emails, operator-platform identity |
| Studio-only registers | Handshake / investor / collab cards — Handshake hub `Voice/` only, never this repo |
| Secrets | `.env`, webhooks, vault claims, analytics IDs |
| Session logs | `dev-log-*.yaml` (already gitignored) |
| Studio overlay | `private/` (gitignored) |

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
