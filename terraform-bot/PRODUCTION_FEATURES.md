# CipherTrust Bot Production Features

This bot now has a few production-style capabilities beyond simple issue labeling.

## Configuration

The bot reads `.ciphertrust-bot.yml` from the repository root.

Important sections:

- `bot.dashboard_issue_title`
- `bot.idempotent_comments`
- `owners.fallback`
- `risk.high_risk_paths`
- `risk.low_risk_paths`
- `auto_merge`
- `merge_queue`
- `commands`

## Idempotent comments

The bot can update existing comments instead of posting duplicate comments.

It uses hidden HTML markers such as:

```md
<!-- ciphertrust-bot:pr-quality -->
```

This is used for PR checks, PR quality output, first-time contributor comments, and merge candidate comments.

## CODEOWNERS support

The bot reads `CODEOWNERS` when present and requests reviewers based on changed files.

If `CODEOWNERS` is missing, it falls back to the `owners.fallback` section in `.ciphertrust-bot.yml`.

## Dashboard

The bot can create or update a dashboard issue.

Run manually with workflow dispatch:

```text
mode = dashboard
```

Scheduled runs also refresh the dashboard.

## Command parser hardening

The command parser now handles explicit commands first, then deterministic natural-language phrases, then Groq-backed safe intent classification.

Allowed LLM intents remain restricted to safe actions only.

## Lightweight merge queue

The bot supports a lightweight queue label, configured by:

```yaml
merge_queue:
  enabled: true
  label: merge-queue
  ready_label: automerge
```

This is not a full Prow/Tide replacement. It tracks PRs with labels, reports eligibility, and keeps maintainers in control. Actual auto-merge remains disabled unless explicitly configured.

Manual workflow dispatch modes:

```text
mode = dashboard
mode = merge-queue
mode = stale-prs
```

## Safety boundaries

- Auto-merge remains disabled by default.
- Natural language cannot close, merge, delete, or approve changes.
- Clean-labels removes only bot-managed labels.
- Unknown/manual labels are preserved.
