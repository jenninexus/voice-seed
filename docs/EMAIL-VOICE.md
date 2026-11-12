# Email voice, accounts, and signatures

**Composition SSOT.** How a mail *reads*, who signs it, and which links it carries. Delivery is a
different question and a different owner.

| Question | Owning SSOT |
|---|---|
| How does mail leave, thread, authenticate, avoid Spam | `sys-admin` → `docs/EMAIL-PROTOCOL.md` (+ `email.js`, `email-threading.test.js`) |
| Which mailbox is which account key | `sys-admin` env: `GMAIL_<KEY>_ADDRESS` / `GMAIL_<KEY>_APP_PASSWORD` |
| How the mail reads, which register, which signature | **this file** (map + slot shapes) → `private/signatures.md` (literal bodies) |
| The letter's argument and pricing | the surface template the register points at (collab, investor, formal) |
| Personality and deep voice content | pdf-designer `users/<id>.json#characterVoice` · `vaults/<id>.json#voice` |

Rule: **the transport doc never decides tone, and this doc never decides DNS.** If a task needs both,
read both, and say which one you acted in.

---

## Account keys are the join column

This repo stores **no mailbox address**. The key below is the same key `sys-admin` uses
(`email_send` / `email_fetch` `account` argument, `GMAIL_<KEY>_ADDRESS`). Resolve the address with
`sys-admin`; resolve the voice here. That way a machine can change mailboxes without editing a voice map,
and this public repo never ships a mailbox.

| Account key | Surface it answers | Register | Default signature slot |
|---|---|---|---|
| `jenninexus2` | **DIY w Jenni lane.** Brand collabs, influencer and creator programs, gifted product, review requests, platform support (publishers, storefronts) | `creatorCollab` (DIY) | `diy-collab` · `diy-collab-address` |
| `jenninexus` | Professional creator mail (rates, media kit, sponsors) **and** formal or official correspondence (landlord, banks, agencies, utilities), **and** personal | `creatorCollab` (professional) · `emailFormal` · none | `pro-collab` · `formal-address` · `personal-short` |
| `martiangames` | Studio and brand surface: partnerships, press, vendors, client work, investor first contact | `studioResume` · `investorSpeech` · `professionalNetwork` | `studio-jenni-shade` |
| Handshake surfaces (mailbox above, register elsewhere) | Task authoring, reviewer replies, staff mail | `technicalAuthorship` | `hs` (pointer only) |

Somebody asking "which voice do I use for this email?" answers in two steps: **account key → register**,
then **register → owning card**. Never pick a register by how the mail feels; pick it by which surface
the account belongs to.

---

## The DIY lane (`jenninexus2`)

The lane exists because the channel does. It is not "Jenni, but shorter".

- **Channel:** DIY w Jenni, `https://www.youtube.com/@diywjenni` (the bare `youtube.com/diywjenni` 404s)
- **Hub page:** `https://jenninexus.com/diy` - fashion, hair, nails, self-care, cooking tutorials and playlists
- **Media kit:** `https://jenninexus.com/media` - counts, brand assets, collab contact
- **What the channel actually is:** self-care, beauty and makeup, nail art, and cooking, shot and edited by
  her. Brand collabs in this lane are product-in-hand, filmed at home.
- **What it is not:** a 3D / game-dev pitch. The 3D and tech audience is a separate channel. Never pad a
  dinnerware or skincare offer with engine work, and never pitch the tech channel to a lifestyle brand.

### How mail in this lane reads

| Prefer | Avoid |
|---|---|
| Warm inbound open, then one honest product-fit line naming the exact product | "Hey friends" · hearts · a yes before naming what she looked at |
| Who she is in one paragraph, creator first, then the channel facts | Résumé-identity dump · studio "we" |
| A concrete deliverable offer with counts of pieces, not adjectives | "beautiful content" with no length, no platforms |
| Honest scale: name the channel that fits, say the smaller channels are smaller, point at the kit | Invented engagement %, blended totals that hide off-lane channels |
| Terms she is actually willing to sign: content live 6+ months, review copy before publish, organic reposts fine, paid ads and whitelisting quoted separately | Unpaid "ambassador", affiliate-only as the whole deal |
| One signature slot, address printed once | Address in the body *and* the signature |

### Default offer shape (gifted or paid)

One dedicated cook-with-me / get-ready-with-me vlog up to 10 minutes featuring the product end to end,
**plus** at least one YouTube Short and one TikTok from the same shoot, product linked in the description
and pinned comment, code or link spoken in the video, brand tagged on YouTube, TikTok and Instagram.
Production fee is separate from any affiliate or commission component.

### Naming in this lane

`Jenni` alone in the signature. The full legal name is used only where a shipping form or a platform
account needs a legal-looking field (`private/signatures.md` holds it, this repo does not). See the naming
ladder in `characters/humans/jenni.md` § Names on email.

---

## Signature slots

A slot is a fixed block with fixed links. Pick one per email, paste it, never retype it. Literal bodies
(including the mailing address and phone) live in `private/signatures.md`; this file defines the shape and
the routing. **Fill-in template for your own stack:**
[`../templates/email-signature.example.md`](../templates/email-signature.example.md).

| Slot | Account key | Carries address | Use when |
|---|---|---|---|
| `diy-collab-address` | `jenninexus2` | yes | Gifting or product exchange: the brand needs somewhere to ship, and the body has not already given it |
| `diy-collab` | `jenninexus2` | no | Paid-only or platform threads, or the body already lists the address |
| `pro-collab` | `jenninexus` | no | Rates, media kit, sponsors, first contact from the professional address |
| `formal-address` | `jenninexus` | yes | Landlord, property management, banks, utilities, benefit agencies, legal, medical. Full legal name, street address, phone |
| `personal-short` | `jenninexus` | no | A human wrote to a human. One line, no links, no blocks |
| `studio-jenni-shade` | `martiangames` | no | Studio or client surface signed by both founders |
| `hs` | Handshake surfaces | no | Task authoring precisely as the Handshake card specifies. **No decoration** |

### Slot shape (neutral example)

```text
Thank you!

- Jenni

MAILING ADDRESS
Street and unit
City, State ZIP

EMAIL (mailto link)
YouTube: CHANNEL NAME
Website: Media Kit & Social Stats
```

Rules that make it survive clients, CRMs and forwarding:

- **No image-only signature.** Text renders where images are blocked.
- **One `<br>` per line, no tables.** Emoji label + bold text is enough.
- **The links are the point.** Channel link, media kit link, mailto. Nothing else.
- **Address once.** If the body already gave it, use the no-address variant.
- **ASCII hyphen in the plain-text part.** Em dashes and smart quotes get mangled or flagged.
- **The signature opens with `Thank you!`**, so the body must not also close on `Thanks,` / `Best,`. End the
  body on its own line and let the block carry the thanks and the name.

---

## Resolution order for any agent

1. **Which account did the mail arrive in, or are we sending from?** → account key.
2. **Account key → register** (table above).
3. **Register → owning card.** `characters/humans/jenni.md` for humans, `private/studio-voice.md` for the
   private registers (`creatorCollab`, `investorSpeech`, `emailFormal`, `professionalNetwork`), the Handshake
   hub card for `technicalAuthorship`.
4. **Surface template** for the argument: the collab letter shape, the investor letter shape, or the formal
   shape. Templates are studio-only; a public clone has the register rules only.
5. **One signature slot.** Body copy from `private/signatures.md`, links live.
6. **Send** with `sys-admin` `email_send`, in-thread (`inReplyTo` + `references` from `email_fetch`
   `replyHeaders`), then verify the Sent copy by its Message-ID.

## Who owns what (do not fork)

| Fact | Owner |
|---|---|
| Delivery, threading, DMARC, send-as | `sys-admin` `docs/EMAIL-PROTOCOL.md` + `email.js` |
| Account list and addresses | `sys-admin` env (`GMAIL_<KEY>_*`) |
| Register map and signature routing | this file + `registry.json` → `email` |
| Literal signature bodies with PII | `private/signatures.md` (never tracked) |
| Collab / investor / formal letter shapes and rates | `private/studio-voice.md` + the surface templates |
| Personality, application voice, deep samples | pdf-designer `users/<id>.json` · `vaults/<id>.json` |
| Handshake authoring voice | Handshake hub `Voice/<name>-handshake.md` |
| Brand marketing prose | `socials/content/<brand>/format-manifest.json` |
| Spoken voice, TTS, clones | `docs/SPOKEN-VOICE.md` and `private/voices/` |

A consumer repo (site app, admin panel, agent) should read `registry.json` → `email` and follow the pointers.
It should not carry its own account table or its own signature block.

## Pre-send checklist

- [ ] Right account key, and the mail is a reply with `inReplyTo` + `references` when a thread exists
- [ ] One register, named out loud before drafting
- [ ] The lane's own links (DIY page, channel, media kit) where the lane applies
- [ ] One signature slot, address printed at most once
- [ ] ASCII hyphens; no em dashes; no AI stock phrasing (see `characters/humans/jenni.md`)
- [ ] Numbers that appear are the ones in the live kit, not a hand-sum
- [ ] Sent copy verified in `[Gmail]/Sent Mail` by Message-ID
