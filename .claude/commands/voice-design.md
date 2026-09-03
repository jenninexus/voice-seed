---
description: "Resolve writing voice — pick the register, open the owning SSOT, edit safely."
argument-hint: "[character|application|social|bot|agency|ops|neophi|signal|lookup] [jenni|shade|jenninexus|martiangames|gub|neophi|nyx|zara|kai|luna|orion|phoenix|vidette|<agent>]"
---

# /voice · /voice-design — Network Voice Router

⭐ **THIS FILE IS THE SSOT** for the repo-local command. Global twins should
point here, not duplicate protocol.

**Shorthand:** `/voice` == `/voice-design`.

**Protocol hub:** [`docs/PROTOCOL.md`](../../docs/PROTOCOL.md).

## Quick answer — socials drafts?

**Yes — for routing, not as the prose file.**

1. Read `registry.json` → brand → register `socialMarketing`
2. Edit tone in `socials/content/<brand>/format-manifest.json` (`patreon_format.voice`)
3. Run the usual socials draft pipeline

Do **not** dump résumé `characterVoice`, bot greeter, Agency loft chat, or NEOPHI
`signalTone` into default brand Patreon.

## Quick answer — bot / Agency / NEOPHI?

| Poster | Command | SSOT |
|---|---|---|
| Join greeter | `/voice bot <id>` | `{bot}/content/greeting.md` |
| Agency loft face | `/voice agency <Agent>` | `agency/agents/*.md` **+** `{bot}/resources/agency-profiles.json#chatVoice` |
| Brand Discord draft | `/voice social <brand>` | format-manifest |
| NEOPHI Signal Crew in-character | `/voice neophi <id>` | `characters/neophi/<id>.md` (`signalTone`) + canon `neophi/src/assets/data/characters.md` |

Full matrix: [`docs/PROTOCOL.md`](../../docs/PROTOCOL.md). Flow C is the Agency desk.

## Quick answer — résumé or cover letter?

Register = **`application`**. Two layers, both blocking before prose.

## Usage

```
/voice-design                              # dashboard — open registry + ask intent
/voice-design lookup jenni                 # show all registers for a human/brand/bot
/voice-design character jenni              # edit characterVoice SSOT
/voice-design application shade            # edit vault #voice (+ #mission if present)
/voice-design social jenninexus            # edit format-manifest marketing voice
/voice-design bot <id>                     # greeter prose
/voice-design agency vidette               # loft agent (audit md + Discord catalogue)
/voice-design ops gub                      # game security triage voice
/voice-design neophi zara                  # Signal Crew signalTone
/voice-design signal luna                  # alias → neophi
```

Aliases: `marketing` → `social`, `resume`/`cover` → `application`, `person` → `character`,
`greeter` → `bot`, `gub`/`security`/`mod` → `ops gub`, `signal` → `neophi`.

## Protocol (always)

### 0. Open the map

1. Read `registry.json`
2. If cross-register or unclear → `docs/REGISTERS.md` + `docs/PROTOCOL.md`
3. Name the **register** out loud before editing anything

### 1. Route by intent

| User intent | Register | Open |
|---|---|---|
| Personality, contrast, emoji prefs | `character` | pdf-designer `users/<id>.json` → `#characterVoice` |
| Résumé / cover letter wording | `application` | vault `#voice` (+ optional `#mission`) |
| Patreon / Discord / news drafts | `socialMarketing` | `socials/content/<brand>/format-manifest.json` |
| Join greeter copy | `botGreeter` | `{bot}/content/greeting.md` |
| Embed chrome / emoji IDs | `discordVisual` | `{bot}/docs/STYLE-SPEC.md` + `assets.json` |
| Loft agent personality + Discord face | `agency*` | `agency/agents/<Agent>.md` + `STUDIO-VOICE.md` **and** `{bot}/resources/agency-profiles.json#chatVoice` |
| Game security triage | `gameSecurityChat` | Game wiki persona — live ops via `/gub` |
| NEOPHI Signal Crew in-character | `signalTone` | `characters/neophi/<id>.md` (+ neophi canon) |
| “Where does X’s voice live?” | lookup | Print registry paths only |

### 2. Edit rules

- **Edit the owning file.** Most cards under `characters/` stay short pointers —
  **exception:** NEOPHI `signalTone` cards *are* the speaking SSOT.
- Visual DNA → neophi `characters.md` first.
- **Update the map** (`registry.json` / notes) only when paths or roster change.
- **Never** put vault claims, contacts, webhooks, or draft post bodies here.

### 3. Cross-repo traps (refuse these)

| Trap | Correct move |
|---|---|
| Résumé → Patreon | Keep `socialMarketing`; tweak format-manifest |
| Agency emoji → ATS PDF | Application register — no Discord emoji |
| Solo app as studio “we” | Applicant vs studio brand |
| Agency → `characterVoice` | Agency stays in agency/ + bot catalogue |
| Patreon long-form → greeter | Greeter stays short in `greeting.md` |
| Agency loft → brand announcements | Loft channel only |
| Ops RP / emoji | Persona hard rule — professional only |
| Theme-kit tweak “fixes voice” | Colors only — rewrite the voice SSOT |
| Signal Crew → default brand Patreon | Only when explicitly in-character |
| Invent shared costume tokens | Canon token rules first |

## Subcommands

### `lookup <id>`

Compact card from `registry.json` + matching `characters/**` — paths only.

### `character <jenni|shade>`

1. Register = `character`
2. Open `pdf-designer/storage/users/<id>.json` → **`#characterVoice`**
3. Card `characters/humans/<id>.md` stays a **short public pointer** — deep edit goes in the JSON
4. Remind: this is *who they are*, **not** how a résumé sounds (that is `application`)

### `application <jenni|shade>`

| Edit… | File |
|---|---|
| Personality, partner contrast, emoji prefs, register map | `pdf-designer/storage/users/<id>.json#characterVoice` |
| Tone, `signatureMoves`, `avoid`, `leadIdentityByTrack` | `pdf-designer/storage/<id>/resume-source.json#voice` |

1. Register = `application`
2. **Shade:** lead identity changes by track — read `voice.leadIdentityByTrack` first.
3. **Never blur the founders:** Jenni = 15 yrs (joined Dec 2011); Shade = 25 yrs (founded 2000).
   Synagen lead is Shade's; Jenni *contributed*.
4. Remind: no Discord/social emoji on ATS PDFs

### `social <brand>`

1. Register = `socialMarketing`
2. Edit `socials/content/<brand>/format-manifest.json` → `patreon_format.voice`
3. This command sets the voice; it does not post
4. Confirm before anything reaches a live Discord `--post`

Jenni-face posts: load `characters/humans/jenni.md` § Social posting style.
Prefer **Hey friends**; not “Hey crew” / anonymous studio-updates copy.

### `bot <id>`

1. Register = `botGreeter` (+ `discordVisual` if chrome/emoji)
2. Open `{bot}/content/greeting.md`
3. Remind: not Patreon, not Agency loft, not ops

### `agency <Agent>`

1. Read `agency/docs/STUDIO-VOICE.md`
2. Edit lore: `agency/agents/<Agent>.md`
3. Edit Discord runtime: `{bot}/resources/agency-profiles.json` → `profiles[<id>].chatVoice`
4. Remind: two layers; keep aligned; loft channel only; no mod authority
5. Seed: `templates/agent-chatVoice.seed.md`

### `ops gub`

1. Card: `characters/ops/gub.md`
2. Deep SSOT: Tank Off `Gub-Persona.md`
3. Live Discord → `/gub`

### `neophi <id>` (aliases: `signal <id>`)

Ids: `nyx` · `zara` · `kai` · `luna` · `orion` · `phoenix`

1. Register = `signalTone`
2. Open `characters/neophi/<id>.md`
3. Cross-check Visual DNA in `neophi/src/assets/data/characters.md`
4. Use **Update hooks** + samples
5. Deep link: `https://neophi.world/?character=<id>#gallery`
6. Remind: not applicant, not studio “we”, not Agency, not greeter

No id → list six cards + `characters/brands/neophi.md`.

## Dashboard (no args)

1. Summarize registers (include `botGreeter`, agency Discord, `signalTone`)
2. List humans, brands, bots, agency agents, **Signal Crew** from registry
3. Ask which lane: character / application / social / bot / agency / ops / neophi / lookup

## Related

| Command | When |
|---|---|
| socials draft pipeline | Marketing drafts after social voice is set |
| `/make-resume` · `/make-cover-letter` | Application build (they *consume* the `application` register) |
| `/gub` | Live security ops |

> **"Voice" is overloaded.** This command owns **written register** (how prose sounds).
> Speech audio and mouth animation are other tools.

## Repo docs

- `AGENTS.md` · `docs/REGISTERS.md` · `docs/PROTOCOL.md` · `docs/ROADMAP.md` · `docs/OVERVIEW.md` · `docs/PUBLIC-LOCAL-SPLIT.md`
