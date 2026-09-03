# Plans — session handoff

This folder is the **session log** for voice-seed. It replaces `dev-log-sego.yaml`
(gitignored, retired here).

| Path | Role |
|------|------|
| `_active/` | At most one carryover plan. Today's file is the cold-start. |
| `_complete/` | Finished session plans |

Keep plans **clone-safe**: no machine-absolute disks, emails, legal names, or vault paths.
Studio-only notes stay in gitignored `private/` or `*.local.md`.
