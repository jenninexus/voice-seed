# Email signature slots — fill-in template

Copy this into your own studio overlay (a gitignored `private/` file) and fill it in there. **Never fill it in
in a tracked file**: a mailing address, a phone number and a legal name are personal data, and a public clone
should not carry them.

Routing rules and why slots exist: [`../docs/EMAIL-VOICE.md`](../docs/EMAIL-VOICE.md) § Signature slots.

---

## 1. Account slots

One row per mailbox you actually send from. The key is whatever your mail tool uses as its account key, so the
voice map never has to store an address.

| Slot key | Account key | Surface it answers | Register |
|---|---|---|---|
| `work2` | `you2` | secondary brand, collab and gifting mail | `creatorCollab` |
| `main` | `you` | professional mail, official/formal mail, personal | `creatorCollab` · `emailFormal` |
| `studio` | `studio` | company surface: partnerships, press, vendors, clients | `studioResume` · `investorSpeech` |

## 2. Slot bodies

### `collab-address` — shipping involved

```text
Thank you!

- <FIRST NAME>

MAILING ADDRESS
<street and unit>
<city>, <state> <zip>

<EMAIL> (mailto link)
YouTube: <CHANNEL NAME> - <channel URL>
Website: Media Kit & Social Stats - <media kit URL>
```

### `collab` — no shipping, or the body already gave the address

```text
Thank you!

- <FIRST NAME>

<EMAIL> (mailto link)
YouTube: <CHANNEL NAME> - <channel URL>
Website: Media Kit & Social Stats - <media kit URL>
```

### `pro` — rates, media kit, first contact

```text
Best,
<FIRST NAME>
<FULL NAME>
<professional alias>
<media kit URL>
```

### `formal-address` — official correspondence

```text
Thank you,

<FULL LEGAL NAME>
<street and unit>, <city> <state> <zip>
<phone> · <email>
```

### `personal-short` — a human wrote to a human

```text
~ <FIRST NAME>
```

### `studio` — company surface, both founders

```text
Best,

<FOUNDER ONE> & <FOUNDER TWO>
<COMPANY NAME>
```

---

## 3. Rules the template encodes

- **One slot per email.** Never two blocks, never a block plus a hand-typed name.
- **Address at most once.** Use the no-address variant when the body already lists it.
- **No image-only signature.** Text renders where images are blocked.
- **Links are the point.** Channel, media kit, mailto. Nothing else.
- **ASCII hyphen in the plain-text part.** Em dashes and smart quotes get mangled or flagged.
- **The block opens with `Thank you!`**, so the body must not also close on `Thanks,` / `Best,`.
- **Formal mail carries no channel link and no emoji.** Creator mail carries no legal-name block.
- **Keep the literals out of git.** The filled-in version belongs in a gitignored overlay, not here.
