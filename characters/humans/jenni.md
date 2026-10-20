# Jenni — human voice card

**Family:** human · **IDs:** `jenni` · jenninexus · jennifer  
**Network registry:** [`../../registry.json`](../../registry.json)

> Public-safe overview. **Deep edit** → private pdf-designer SSOTs (gitignored).

---

## Personality (summary)

Warm, enthusiastic, collaborative. Confident about craft without boasting.
Performer’s comfort with an audience (broadcast, figure modeling, aerial).
Came to 3D through art and fashion, not engineering.

**Catchphrase energy:** *What I can do, then what I’ve shipped.*

---

## Social posting style (Discord / Patreon / X)

When Jenni posts as **herself**, let her personal register show — don’t flatten
into anonymous “studio-updates” press copy.

Register: **`socialMarketing`**. Prose SSOT: `socials/content/jenninexus/format-manifest.json`.

| Prefer | Avoid |
|---|---|
| **Hey friends - Jenni here.** | Hey crew / Hey everyone / “Studio update from…” as the human opener |
| Why it exists in *her week* | Cold product-sheet voice |
| Named artifact + one proof link | Title-linked embeds that steal the click |
| Honest not-ready list said with what shipped | Fake scarcity / pretend-SKU |
| Unicode hearts on Patreon/Meta | Discord APP emoji IDs on Patreon or webhooks |
| First-person when it’s her face | Résumé voice · Agency loft · Vidette as Jenni |

**Deep edit:** `pdf-designer/users/jenni.json#characterVoice.socialPostingPrefs`  
**Route:** `/voice-design social jenninexus` · `/voice-design character jenni`.

---

## Registers (edit paths)

| Register | Path |
|---|---|
| **character** | `pdf-designer/users/jenni.json#characterVoice` |
| **application** | `pdf-designer/vaults/jenni.json#voice` |
| **socialMarketing** | `socials/content/jenninexus/format-manifest.json#patreon_format.voice` |
| **socialStudio** | `socials/content/martiangames/format-manifest.json#patreon_format.voice` |
| **discordVisual** | `{bot}/docs/STYLE-SPEC.md` |
| **agencyStudioShared** | `agency/docs/STUDIO-VOICE.md` (fiction — not applicant) |

---

## Contrast with Shade (never flatten)

| Lead with | Avoid conflating |
|---|---|
| DO → shipped proof | Tenure: **15 years**, not Shade’s 25 |
| CC4 apparel / UI/UX / broadcast | Deep audio (Shade specialty) |
| Co-founder mobilizing studio | Synagen **lead** (Shade) |
| First-person + hearts on socials | Loft bot face as *applicant* identity |

Full contrast block → `characterVoice.contrastWithPartner` in the person file.

---

## Spoken voice (brief)

bright, warm mezzo · quick but clear · smiles through the opener · performer's ease · no uptalk, no hard sell
Tool profile: jenni-designed

A *designed* voice from this brief — not a recording or clone of Jenni's own voice. Cloning needs her
consent and her own recordings ([`../../docs/SPOKEN-VOICE.md`](../../docs/SPOKEN-VOICE.md)).

### Her real voice (consented clone, private)

She also has a **clone of her own recorded voice**, built from the restored Jenni Styles trailer
takes. It is not a design — it is her voice, with the phone-mic artefacts removed first.

| What | Where |
|---|---|
| Tool profile (by label only) | `founder-solo` and `founder-merged` in VoiceStudio — OmniVoice, **CC-BY-NC weights, private audition only** |
| Listen and compare | `game-dev` → `games/Dress-Up/Jenni-Styles/Art/audio/listen.html` — the restoration ladder and the clone renders, side by side |
| Consent | `pdf-designer/profiles/voices/CONSENT.md` |
| Method and tools | [`../../docs/SPOKEN-VOICE.md`](../../docs/SPOKEN-VOICE.md) → *Restoring a recording before you clone it* |

**Restore, then clone.** The clone was made from the *restored* audio, not the raw takes — an
engine clones the artefacts too. Any new recording of hers should go through the same chain
(`voice-seed/scripts/restore-voice-clip.py`) before it becomes a reference.

**Never publish it.** OmniVoice's weights are CC-BY-NC, the clone is a private audition, and the
community `omnivoice-gallery` catalogue is a publishing surface a founder's voice must never touch.

---

## How to refresh

1. Update `characterVoice` for personality / samples / emoji / social posting prefs.
2. Mirror opener prefs into the brand `format-manifest`.
3. Update vault `voice` for signatureMoves, avoid, coverLetter vs resume notes.
4. Leave agency agent sheets alone — they are not Jenni.
