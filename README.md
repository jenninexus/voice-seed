<div align="center">

# Voice Seed

![MIT](https://img.shields.io/badge/license-MIT-9b5cf6?style=flat-square&labelColor=1a1a2e)
![Type](https://img.shields.io/badge/type-register%20map-63b3ed?style=flat-square&labelColor=1a1a2e)
![Deps](https://img.shields.io/badge/dependencies-zero--deps-9b5cf6?style=flat-square&labelColor=1a1a2e)
![Mode](https://img.shields.io/badge/mode-public--safe-ff6ec4?style=flat-square&labelColor=1a1a2e)

## One map. Many writing rooms.
## Résumé voice stays out of Patreon.

A small **writing-register map**. Clone it beside [Agency](https://github.com/jenninexus/agency)
if you want a desk index so résumé voice, Patreon voice, and loft `chatVoice` stay in
separate rooms. This repo is the **map**, not a second copy of private personality
or résumé claims.

</div>

- One map so each writing job opens the file that owns it
- Copy-ready `chatVoice` seed for Agency desks
- Relative paths only — clone beside Agency, never a submodule
- Public-safe pointers; personality and claims stay in *your* vaults

Agency works without this repo.

---

## Quick Start

```text
git clone https://github.com/jenninexus/agency.git
# optional:
git clone https://github.com/jenninexus/voice-seed.git
```

1. Read [`docs/REGISTERS.md`](docs/REGISTERS.md) — which register owns what.
2. Open [`registry.json`](registry.json) — relative `ssotPattern` paths only.
3. Copy [`templates/agent-chatVoice.seed.md`](templates/agent-chatVoice.seed.md)
   into `agency/agents/YourAgent.md`.
4. Deepen Discord samples in the consuming bot’s `resources/agency-profiles.json`
   (same relative path whether you use a live bot or a future bot-seed clone).

| Question | Answer |
|---|---|
| Where do I edit cover-letter tone? | pdf-designer vault `voice` (see registry) |
| Where is personality / partner contrast? | pdf-designer `users/<id>.json#characterVoice` |
| Where is a loft agent’s Discord chat face? | `{bot}/resources/agency-profiles.json` + `agency/agents/<Name>.md` |
| Where is the join greeter? | `{bot}/content/greeting.md` |
| How do socials + bots + agency fit? | [`docs/PROTOCOL.md`](docs/PROTOCOL.md) — **Flow C** is the desk |
| What must never mix? | [`docs/REGISTERS.md`](docs/REGISTERS.md) |

---

## What it does

| Family | Who | Edit voice in… |
|---|---|---|
| **Humans** | Public-safe pointers | pdf-designer `characterVoice` + vault `voice` |
| **Brands** | Marketing faces | socials `format-manifest.json` |
| **Bots** | Greeter + chrome | `{bot}/content/greeting.md` + STYLE-SPEC |
| **Agency agents** | Vidette, Bloggie, … | `agency/agents/*.md` + bot catalogue |
| **Ops** | Game security triage | Game wiki persona — card [`characters/ops/gub.md`](characters/ops/gub.md) |
| **NEOPHI** | Signal Crew in-character | [`characters/neophi/`](characters/neophi/) (`signalTone`) |

### Agent entrypoints

| Invoke | Where |
|---|---|
| `/voice-design` | [`.claude/commands/voice-design.md`](.claude/commands/voice-design.md) |
| Capability map | [`AGENTS.md`](AGENTS.md) |

---

## Docs

| | |
|---|---|
| [`docs/REGISTERS.md`](docs/REGISTERS.md) | Hard separation rules |
| [`docs/PROTOCOL.md`](docs/PROTOCOL.md) | socials ↔ bots ↔ agency posting flow |
| [`docs/PUBLIC-LOCAL-SPLIT.md`](docs/PUBLIC-LOCAL-SPLIT.md) | Clone vs studio-only |
| [`docs/PRODUCT.md`](docs/PRODUCT.md) | Free map + tip |
| [`docs/OVERVIEW.md`](docs/OVERVIEW.md) | Narrative map |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Next work |

---

## Privacy

- **Tracked here:** public-safe overviews, register map, templates, relative pointers.
- **Never commit here:** real emails, vault claims, Discord webhook URLs, analytics IDs,
  machine-absolute disks, legal names, or studio-only operator cards.

See [`docs/PUBLIC-LOCAL-SPLIT.md`](docs/PUBLIC-LOCAL-SPLIT.md).

---

MIT — use, fork, customize. See [`LICENSE`](LICENSE).

<div align="center">

If this helped you keep writing voices in separate rooms:

[Star this repo](https://github.com/jenninexus/voice-seed) · [Links](https://jenninexus.com/links) · [Patreon](https://www.patreon.com/c/JenniNexus) · [PayPal](https://paypal.me/jenninexus)

Published by [Jenni](https://github.com/jenninexus) at [Monofinity Studio](https://github.com/monofinitystudio).

</div>
