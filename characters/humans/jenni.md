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

**Deep edit:** `pdf-designer/storage/users/jenni.json#characterVoice.socialPostingPrefs`  
**Route:** `/voice-design social jenninexus` · `/voice-design character jenni`.

---

## Registers (edit paths)

| Register | Path |
|---|---|
| **character** | `pdf-designer/storage/users/jenni.json#characterVoice` |
| **application** | `pdf-designer/storage/jenni/resume-source.json#voice` |
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

## How to refresh

1. Update `characterVoice` for personality / samples / emoji / social posting prefs.
2. Mirror opener prefs into the brand `format-manifest`.
3. Update vault `voice` for signatureMoves, avoid, coverLetter vs resume notes.
4. Leave agency agent sheets alone — they are not Jenni.
