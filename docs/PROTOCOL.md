# Voice + Discord posting protocol

Hub for **how socials, bots, agency, and voice-seed work together**.  
Register rules: [`REGISTERS.md`](REGISTERS.md) · Map: [`../registry.json`](../registry.json) · Narrative: [`OVERVIEW.md`](OVERVIEW.md)

---

## One rule

**Name the register → open the owning SSOT → edit there → preview → (bots) deploy only if runtime code/config needs it.**  
`voice-seed` is the map. Prose never accumulates here.

---

## Who is speaking? (decide first)

| Surface | Poster “character” | Register | Edit |
|---|---|---|---|
| Patreon / news / brand Discord **drafts** | Brand (“I” / “we”) — a named human face uses that card’s social prefs | `socialMarketing` | `socials/content/<brand>/format-manifest.json` |
| Announcement / Patreon / YT **webhooks** | Webhook display name | `socialMarketing` | Draft in socials; send via webhook tools (IDs stay in the socials env, not here) |
| **Join greeter** | App bot user | `botGreeter` | `{bot}/content/greeting.md` |
| Slash-command embeds | Same app bot | `discordVisual` | `{bot}/docs/STYLE-SPEC.md` + `resources/assets.json` |
| Agency loft channel | Vidette, Bloggie, … | `agencyDiscordChat` | `{bot}/resources/agency-profiles.json#chatVoice` |
| Agency site-audit personality | Same agents (deeper lore) | `agencyAudit` + `agencyStudioShared` | `agency/agents/*.md` + `agency/docs/STUDIO-VOICE.md` |
| Game security triage | Ops bot | `gameSecurityChat` | Game wiki persona file — live ops via the ops command |
| Résumé / cover letter | Human applicant | `character` + `application` | pdf-designer vault — **never** Discord |
| NEOPHI Signal Crew in-character update | Nyx / Zara / Kai / Luna / Orion / Phoenix | `signalTone` | `characters/neophi/<id>.md` (+ canon `neophi/src/assets/data/characters.md`) |

---

## Repo ownership (hard boundaries)

```
voice-seed     → map + public cards (incl. NEOPHI signalTone)
socials        → drafts, webhooks, previewer
{bot}          → greeter, slash cmds, optional loft listen/reply runtime
agency         → loft lore + STUDIO-VOICE (public characters)
pdf-designer   → human characterVoice + application voice
neophi         → Signal Crew visual/canon SSOT (characters.md) — not speaking tone
theme kits     → colors / tokens / CSS — NOT writing voice
```

`{bot}` is a clone-relative Discord runtime (live bot **or** a future bot-seed
checkout). Same relative files: `content/greeting.md`, `docs/STYLE-SPEC.md`,
`resources/assets.json`, `resources/agency-profiles.json`. Do not pin a GitHub
URL until that seed remote exists.

| Kit | Role vs voice |
|---|---|
| Theme / token kits | Brand hex / palettes — feed `discordVisual` / STYLE-SPEC |
| Syna product UI tokens | An agent may **audit** sites with them; they do not own Discord chatVoice |

---

## Daily flows

### A. Brand marketing post

1. `/voice-design social <brand>` → confirm `socialMarketing`
2. Tweak `patreon_format.voice` / `voice_faces` only if tone is wrong
3. Named-human face: read that card’s social posting style + vault `socialPostingPrefs`
4. Draft with the socials pipeline
5. Preview, then publish (confirm before any live Discord `--post`)

### B. Bot greeter tone

1. `/voice-design bot <id>` → register `botGreeter`
2. Edit `{bot}/content/greeting.md` (STYLE-SPEC for chrome)
3. Preview the greeter tab in the socials previewer if you have one
4. Do **not** paste Patreon voice or Agency banter into the greeter

### C. Agency desk (lore + Discord face)

Clone users staff a desk in **agency**, then optionally use this map so the
desk does not borrow résumé or Patreon voice.

1. **Lore / catchphrase / audit desk** → `/voice-design agency <Agent>` →
   `agency/agents/<Agent>.md` + `agency/docs/STUDIO-VOICE.md`
2. **Live Discord samples, keywords, webhook face** → same command also opens
   `{bot}/resources/agency-profiles.json#profiles[<id>].chatVoice`
3. Keep layers in sync: deep personality in the agency repo; runtime samples +
   accents in the bot catalogue. Seed blocks:
   [`../templates/agent-chatVoice.seed.md`](../templates/agent-chatVoice.seed.md)
4. Pin / smoke posts stay in socials (or your own webhook tools). Listener
   work stays in the bot repo.
5. Never let Agency claim to be a human founder; never give Agency mod power
   (that is ops)

### D. Ops / game security

1. `/voice-design ops gub` for the persona seed → game wiki for doctrine
2. Live Discord → the ops command only

### E. NEOPHI Signal Crew update (in-character)

1. `/voice-design neophi <nyx|zara|kai|luna|orion|phoenix>` → register `signalTone`
2. Confirm Visual DNA in neophi `characters.md` — don’t invent tokens
3. Draft using that card’s **cadence + update hooks + samples**
4. Site deep link: `https://neophi.world/?character={id}#gallery`
5. Do **not** paste into default brand Patreon — only when the post is explicitly that crew member

---

## Agency edit checklist (per character)

When customizing one loft agent:

| Step | File | What to change |
|---|---|---|
| 1 | `agency/docs/STUDIO-VOICE.md` | Only if shared loft rule changes |
| 2 | `agency/agents/<Name>.md` | Personality, catchphrase, audit voice |
| 3 | `{bot}/resources/agency-profiles.json` | `chatVoice`, keywords, avatar URLs, accent |
| 4 | `registry.json` | Only if paths / roster change |
| 5 | Previewer / pin draft | Visual QA before live webhook |

**Do not** duplicate full `chatVoice` into voice-seed cards.

---

## Anti-mix table

| Trap | Correct |
|---|---|
| Greeter sounds like Patreon long-form | Greeter stays ≤4–5 lines; marketing stays in format-manifest |
| Agency chatVoice → brand announcements webhook | Announcements = brand / named human; Agency = loft channel only |
| Loft bot avatar → applicant voice | Avatar ≠ register; applicant stays pdf-designer |
| Greeter / ops → Patreon “we” emoji voice | Separate SSOTs |
| Theme-kit palette tweak “updates voice” | Colors only — rewrite prose in the voice SSOT |
| Copy Agency emoji into ATS PDF | Application register stays clean |
| Signal Crew tone → default brand Patreon | Only when post is explicitly in-character via `/voice-design neophi <id>` |
| Invent shared costume tokens | Canon token rules in neophi `characters.md` first |

---

## Related roadmaps

| Repo | Roadmap |
|---|---|
| voice-seed | [`ROADMAP.md`](ROADMAP.md) |
| socials | `socials` docs (when that repo is present) |
| agency | `agency/docs` — loft lore |
| consuming bot | `{bot}/docs` — greeter + catalogue |
