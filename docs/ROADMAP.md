# voice-seed roadmap

Session handoff: [`../Plans/_active/`](../Plans/_active/) (carryover) · [`../Plans/_completed/`](../Plans/_completed/) (done) + this file. `/jen/roadmap`
reads here. Do not recreate `dev-log-sego.yaml` (archived under gitignored `private/archive/`).

## Public seed

GitHub is **public** (2026-09-03). History is a single clean snapshot.

- [x] `docs/PUBLIC-LOCAL-SPLIT.md` + `docs/PRODUCT.md`
- [x] Relative paths in `registry.json` + public cards
- [x] Handshake / investor / legal-name cards off the public slice (Handshake hub `Voice/` only)
- [x] README clone-first + contrast-safe badges + LICENSE + tip footer
- [x] Orphan snapshot + GitHub visibility → Public (2026-09-03)
- [ ] Agency pairing GETTING-STARTED / STUDIO-VOICE / README — **push from the agency repo**

Keep this repo a **thin map**. Deep work happens in owning SSOTs.

## Done (2026-07-14)

- [x] `registry.json` + `docs/REGISTERS.md` + human/brand/agency/ops cards
- [x] `/voice-design` router
- [x] socials format-manifest → network-map pointers
- [x] bot catalogue → `voiceLayers.networkRegistry`
- [x] Gub ops card + `gameSecurityChat` separation
- [x] Cross-repo protocol hub: [`PROTOCOL.md`](PROTOCOL.md)

### Recent (2026-07-15 → 09-03)

- Agency loft listener + slash desks live on the consuming JN bot (`agencyDiscordChat`).
- socials previewer + marketing drafts use **`socialMarketing`** only.
- **2026-09-03:** public-seed leak scrub, then orphan history + GitHub Public.
  Handshake cards live in the local Handshake hub `Voice/` only.
- **2026-09-03:** retired repo-root `dev-log-sego.yaml`. Live handoff is `Plans/` + this file.
  Frozen copy: gitignored `private/archive/dev-log-sego.yaml` (two COMPLETED 2026-07-16
  notes). Remaining follow-ups are in Next below.

## Next — bot + agency customization

### 1. Register completeness

- [x] Document `botGreeter` (`{bot}/content/greeting.md`)
- [x] Document theme kits as **non-voice** (color only) in PROTOCOL
- [ ] Optional: seed cards under `characters/bots/` when greeter tone diverges enough
- [ ] Keep `agencyDiscordChat` samples in sync with `agency/agents/*.md`

### 2. `/voice-design` UX

- [x] Subcommand `bot` → greeter SSOT
- [x] Agency path documents two layers (audit md vs Discord catalogue)
- [ ] Dashboard lists bot posters + agency roster from registry (no prose dump)

### 3. Downstream (owned elsewhere — track only)

| Work | Owner |
|---|---|
| Agency pairing GETTING-STARTED push | **agency** repo (this map is already public) |
| Agency pin + webhook smoke | socials + consuming bot |
| MessageCreate keyword MVP | consuming bot |
| Brand Discord still confirm-before-post | socials policy |
| JN `/products#voice-seed` free card | product-design + jenninexus.com |
| MG `format-manifest` studio-we depth (same pattern as JN `voice_guide`) | socials — when MG marketing needs it |
| Optional `/voice-design agency` verify-sample via socials `:8777` | socials + this command |

## Non-goals

- No second prose SSOT under `characters/`
- No webhook URLs, tokens, or vault claims in this repo
- No merging human `characterVoice` into bot greeters
- Bot Seed URL is [jenninexus/bot-seed](https://github.com/jenninexus/bot-seed) — still never a submodule
- No Handshake / investor / collab cards — those never return here
