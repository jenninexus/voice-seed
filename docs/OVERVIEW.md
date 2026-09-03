# Voice design overview

We design **voices by register**, then give each **character** a home register
plus pointers to the others. Personality is not one blob reused everywhere.

```
                    ┌─────────────────────────┐
                    │   voice-seed (this repo) │
                    │   map + public overviews │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┬────────────────┐
        ▼                       ▼                       ▼                ▼
  Humans (private)        Brands (marketing)      Agency (fiction)   Ops (games)
  pdf-designer            socials format-manifest agency + jenni-bot Tank Off wiki
  characterVoice          + bot greeters          agents/*.md        Gub-Persona.md
  vault voice             STYLE-SPEC / greeting   agency-profiles    /gub skill
```

Cross-repo posting matrix: [`PROTOCOL.md`](PROTOCOL.md).

---

## Humans — Jenni & Shade

Both are co-founders of Martian Games. They share tools and many studio facts;
they must **not** share the same opening energy or specialty tell.

| | Jenni | Shade |
|---|---|---|
| Energy | Warm, enthusiastic, collaborative; performer comfort with audience | Assured senior research engineer; AI-primary on Default |
| Open | What she can *do*, then what she shipped | AI: Theory→Implementation→Impact · Non-AI: arts → tech |
| Specialty tell | CC4 apparel, UI/UX, broadcast/community, co-founder mobilizing studio | IQO/HRM/Synagen on Default; audio + founder spine on other tracks |
| Tenure trap | **15 years** (joined 2011) | **25 years** (founded 2000) |
| Social register | JN first-person “I” + hearts | MG studio “we / Shade & Jenni” (marketing) — solo apps stay “I, Shade” |

**Edit:** private SSOTs under pdf-designer `storage/` — see
[`../characters/humans/jenni.md`](../characters/humans/jenni.md) and
[`shade.md`](../characters/humans/shade.md).

Reference self-descriptions (private, local): e.g.
`pdf-designer/storage/shade/refrence/Self-Described.md` — use to refresh
`characterVoice`, never commit into this repo.

---

## Brands — marketing only

| Brand | POV | Emoji / chrome |
|---|---|---|
| **JenniNexus** | Jenni “I” | 💜🩷, `jenniheart`, Vidette as *bot face* (not applicant) |
| **Martian Games** | Shade & Jenni “we” | 🪐🚀👽🧡, MG logo |

These feed Patreon / Discord / news — **not** ATS résumés and **not** join greeters.

## Bots — greeter + app face

| Bot | Prose | Chrome |
|---|---|---|
| **jenni-bot** | `content/greeting.md` | STYLE-SPEC + assets |
| **martian-bot** | `content/greeting.md` | STYLE-SPEC + assets |

Short welcome copy only. Brand long-form stays in socials. Index:
[`../characters/bots/`](../characters/bots/).

---

## Agency — fictional loft crew

One employer (the Agency), one cyberpunk loft, many desks. Shared attributes in
agency `STUDIO-VOICE.md`. Distinct chat signatures (Vidette calm/precise,
Bloggie warm editor, GraphViz dry color wit, …).

They staff **site audits** and **Discord agency-channel** replies (runtime
catalogue: jenni-bot `agency-profiles.json`). They are never the human applying
for a job, and they never post JN announcements.

---

## Ops — game security / triage

**Sergeant Gub** (Tank Off / Martian Games Discord) is professional support &
moderation: lead with the answer, zero role-play, zero emoji, never leak logins.
Etymology *bug*→Gub is not a costume. Deep wiki: Tank Off `Gub-Persona.md`.
Card: [`../characters/ops/gub.md`](../characters/ops/gub.md). Invoke ops work with `/gub`.

Do not mix with Agency loft playfulness or MG Patreon marketing voice.

---

## Adding a new voice

1. Pick the family (human / brand / agency / ops).
2. Copy the right seed from [`../templates/`](../templates/) (ops: mirror `characters/ops/gub.md`).
3. Add a card under [`../characters/`](../characters/).
4. Add an entry to [`../registry.json`](../registry.json).
5. Put the *deep* content in the owning SSOT (pdf-designer / socials / agency / bot / game wiki) — not here.
