# CipherTrust Bot — Wiki

The CipherTrust Bot (`@ciphertrust-bot`) automates issue and PR triage for this Terraform provider repository. It labels new issues and PRs automatically, detects duplicates, tracks PR quality, and responds to maintainer commands.

---

## Table of Contents

- [How it works](#how-it-works)
- [Commands](#commands)
- [Labels](#labels)
- [Automatic behaviours](#automatic-behaviours)
- [Stale cleanup](#stale-cleanup)
- [Configuration](#configuration)
- [Control labels](#control-labels)
- [Safety boundaries](#safety-boundaries)

---

## How it works

The bot is a Python script (`terraform-bot/bot.py`) that runs as a GitHub Actions workflow on four event types:

| Trigger | What runs |
|---|---|
| `issues` — opened / edited / labeled | Auto-labels the issue; runs duplicate detection on `opened` |
| `issue_comment` — created | Parses the comment for a `@ciphertrust-bot` command and executes it |
| `pull_request_target` — opened / edited / synchronize / reopened / ready\_for\_review / labeled | Auto-labels the PR; posts a PR triage comment |
| `schedule` (daily) | Stale cleanup; dashboard update |

The bot avoids duplicate-comment spam using hidden HTML markers (`<!-- ciphertrust-bot:key -->`). **Automatic** comments (PR triage, issue-quality, duplicates, welcome) are updated **in-place**. **Command replies** (`help`, `features`, `summarize`, `explain`, `label`, `check-labels`, `clean-labels`, `duplicate`) are **reposted** — the previous one is deleted and a fresh one is added at the bottom — so re-running a command always produces a visible reply while still keeping just one comment of that kind.

---

## Commands

Commands can appear anywhere in a comment body. Only maintainers, members, and collaborators can trigger them.

| Command | What it does |
|---|---|
| `@ciphertrust-bot help` | Shows the command reference table |
| `@ciphertrust-bot features` | Shows a summary of all bot features |
| `@ciphertrust-bot summarize` | AI-generated summary of the issue or PR. On a PR, reads the actual diff — not just the description |
| `@ciphertrust-bot explain` | AI walkthrough of the code changes in a PR. PR-only; issues get a helpful error |
| `@ciphertrust-bot check-labels` | Re-runs label assessment and posts a report of what was added and what may be stale |
| `@ciphertrust-bot clean-labels` | Same as `check-labels` but also removes bot-governed labels the LLM no longer considers applicable. Removal is limited to the LLM-governed content labels plus `needs-tests`/`needs-docs`/`needs-info` — `duplicate` and process/control labels are never removed |
| `@ciphertrust-bot label` | Re-applies all suggested labels for the issue/PR |
| `@ciphertrust-bot label <name>` | Applies a single specific label, e.g. `@ciphertrust-bot label bug` |
| `@ciphertrust-bot duplicate #N` | Marks the issue as a duplicate of `#N`, applies the `duplicate` label, and posts a duplicate marker comment |

> **Natural language routing:** If the command doesn't match a keyword exactly, the bot sends it to an LLM to resolve the intent. For example, `"can you give me a summary?"` routes to `summarize`. Unknown or unsafe requests are rejected with a message.

---

## Labels

**How labels are decided:** the **type** and **area** labels are chosen by an LLM that reads the issue/PR content — and, for PRs, the changed files and the diff — constrained to the fixed label set below (it can never apply a label outside this set). The keyword/path patterns listed in the "Applied when" columns are the guidance the model follows; they are also the **deterministic fallback** used only if the LLM is unavailable (no key / API error / unparseable reply). The other labels are not LLM-decided: `needs-tests`/`needs-docs` are computed from the changed files, `needs-info` is the issue-completeness check (LLM with regex fallback), and `duplicate` comes from duplicate detection or the `duplicate #N` command.

### Type labels

| Label | Applied when |
|---|---|
| `bug` | Title/body contains `bug`, `fail`, `error`, `panic`, `broken`, or `crash`. Also applied by the LLM classifier |
| `documentation` | Title/body contains `doc`, `documentation`, `readme`, or `examples`. On PRs, also when a `.md` file or `docs/` path is changed |
| `enhancement` | Title/body contains `feature`, `enhance`, `improve`, or `request`. Also applied by the LLM classifier |
| `duplicate` | Applied by the LLM classifier when the issue/PR reads as a duplicate, or manually via `@ciphertrust-bot duplicate #N` |

### Area labels

| Label | Applied when |
|---|---|
| `auth` | Title/body contains `auth`, `login`, `unauthorized`, `forbidden`, `certificate`, or `tls`. On PRs, also when a changed filename contains `auth` or `tls` |
| `security` | Always applied alongside `auth`. Also applied standalone when the word `security` appears anywhere in the title/body, or when an `auth`/`tls` file is changed in a PR |
| `ciphertrust-manager` | Title/body contains `ciphertrust manager`, `ciphertrust`, or `cm` |
| `provider-config` | Title/body contains `provider config`, `provider block`, `endpoint`, or `ciphertrust manager`. On PRs, also when a changed filename contains `provider` |
| `resource` | Title/body contains `resource_` or `resource`. On PRs, also when a `resource_*.go` file is changed |
| `data-source` | Title/body contains `data source` or `datasource`. On PRs, also when a `data_source_*.go` file is changed |

### Quality / completeness labels

| Label | Applied when |
|---|---|
| `needs-info` | The LLM (or regex fallback) judges that 2 or more of the 5 required issue sections are missing, or the body is under 80 characters. The 5 sections are: Terraform version, provider version, steps to reproduce, expected behavior, actual behavior |
| `needs-tests` | PR-only. A `.go` file was changed but no `_test.go` file was included |
| `needs-docs` | PR-only. A `.go` file was changed but no `.md` / `docs/` / `examples/` file was changed |

### Process labels

| Label | Applied when |
|---|---|
| `bot-dashboard` | Applied only to the bot's own dashboard issue. Never applied to real issues |
| `stale` | Applied by the scheduled stale checker (see [Stale cleanup](#stale-cleanup)) |

---

## Automatic behaviours

### Issue opened
1. Type/area labels are applied by the LLM reading the issue content (keyword rules are the fallback if the LLM is unavailable).
2. The LLM assesses completeness (with regex as fallback if Groq is unavailable). If 2+ sections are missing, `needs-info` is added and a "More information needed" comment is posted listing what's missing.
3. Duplicate detection runs: searches for similar open issues using title keywords, resource names, error phrases, and HTTP status codes. If a strong match is found, a "Possible duplicate issues" comment is posted with a similarity table.

### Issue edited / re-labeled
Labels are re-synced. Labels a maintainer manually removed are never re-added (tracked via the issue events API).

### PR opened
1. Type/area labels are applied by the LLM reading the PR title, body, changed files, and diff (file-path/keyword rules are the fallback if the LLM is unavailable).
2. `needs-tests` / `needs-docs` applied if code was changed without test or docs files (always computed from the changed files, not the LLM).
3. A PR triage comment is posted summarising labels and any missing checks.
4. First-time contributors receive a welcome comment.

### PR synchronize / ready for review
Labels re-synced (add-only). Triage comment updated if there are missing checks or a high-risk change.

---

## Stale cleanup

Runs on a daily schedule.

| Type | Inactivity threshold | Behaviour |
|---|---|---|
| PRs | 30 days (or `STALE_PR_DAYS` / `STALE_PR_MINUTES` env vars) | Phase 1: add `stale` label + warning comment. Phase 2 (next run): close |
| Issues | 60 days (`STALE_ISSUE_DAYS`) | Same two-phase behaviour |

**To reset staleness:** comment, push new changes, or remove the `stale` label. Any activity more than 2 minutes after the warning automatically revives the item (the `stale` label is dropped and the cycle restarts) instead of closing it.
**To exempt permanently:** add the `no-stale` label.

Grace period between warning and close: 7 days (`STALE_GRACE_DAYS`).

---

## Configuration

The bot reads `.ciphertrust-bot.yml` in the repo root (if present) and deep-merges it over the defaults below.

```yaml
bot:
  dashboard_issue_title: "CipherTrust Bot Dashboard"
  idempotent_comments: true

labels:
  managed_extra: []

risk:
  high_risk_paths:
    - .github/workflows/**
    - terraform-bot/**
    - go.mod
    - go.sum
    - "**/*auth*"
    - "**/*credential*"
    - "**/*token*"
    - "**/*secret*"
    - "**/*tls*"
  low_risk_paths:
    - docs/**
    - examples/**
    - "*.md"
    - "**/*.md"

commands:
  natural_language: true
```

> `risk.high_risk_paths` and `risk.low_risk_paths` are used internally to compute whether a PR is high-risk. High-risk PRs always include a risk section in their triage comment.

### Environment variables

| Variable | Purpose |
|---|---|
| `GITHUB_TOKEN` / `GH_TOKEN` | GitHub API authentication (required) |
| `GITHUB_REPOSITORY` | `owner/repo` (set automatically by Actions) |
| `GROQ_API_KEY` | Enables LLM features (summarize, explain, issue quality assessment, NL command routing). If unset, the bot falls back to regex-based quality checks and logs a warning |
| `GROQ_MODEL` | LLM model to use (default: `llama-3.3-70b-versatile`) |
| `STALE_PR_DAYS` | Days before a PR is stale (default: 30) |
| `STALE_ISSUE_DAYS` | Days before an issue is stale (default: 60) |
| `STALE_GRACE_DAYS` | Days between stale warning and close (default: 7) |
| `STALE_PR_MINUTES` | Testing only: minute-granularity PR staleness threshold; overrides `STALE_PR_DAYS` when set |
| `STALE_GRACE_MINUTES` | Testing only: minute-granularity grace between warning and close; overrides `STALE_GRACE_DAYS` when set |

---

## Control labels

These are never applied by the bot — they are applied manually to change the bot's behaviour.

| Label | Effect |
|---|---|
| `bot-labels-locked` | The bot stops **automatically** changing labels on this issue/PR — no adds or removes during issue open/edit or PR open/synchronize. Note: explicit maintainer commands (`@ciphertrust-bot label`, `check-labels`, `clean-labels`) still apply, since they are deliberate actions |
| `no-stale` | Permanently exempts this issue/PR from stale warnings and auto-close |

---

## Safety boundaries

- Commands only execute for users with `OWNER`, `MEMBER`, or `COLLABORATOR` author association.
- The bot ignores comments authored by itself or any other bot, so the example commands shown in its own help/label output never self-trigger.
- The bot never merges PRs.
- `clean-labels` only ever removes LLM-governed content labels plus `needs-tests`/`needs-docs`/`needs-info`; `duplicate` and process/control labels (`stale`, `no-stale`, `bot-dashboard`, `bot-labels-locked`) are never removed.
- Labels a maintainer manually removed are never re-applied by the bot (tracked via issue events API).
- Natural-language commands are enum-validated before execution — the LLM can only resolve to a known intent, never invent new ones.
- Unknown or unsafe command text routes to `"I could not safely map that request to a supported command"` with no side effects.
