# CipherTrust Terraform Bot Features

This repository includes a GitHub Actions based maintainer bot for issue and PR triage. The bot runs from `.github/workflows/terraform-bot.yml` and uses the Python modules under `terraform-bot/`.

The bot identity is expected to be a normal GitHub user named `ciphertrust-bot`, authenticated through the `CIPHERBOT_PAT` repository secret.

## Required secrets

| Secret | Purpose |
| --- | --- |
| `CIPHERBOT_PAT` | GitHub token used to comment, label, close issues/PRs, request reviewers, and optionally merge PRs. For a public repo, a classic PAT with `public_repo` is usually enough during testing. |
| `GROQ_API_KEY` | Optional Groq key used for LLM summaries, classification, and duplicate reasoning. |

## Workflow triggers

The workflow currently runs on:

- `issues`: opened, edited
- `pull_request_target`: opened, edited, synchronize, reopened, ready_for_review, labeled
- `issue_comment`: created
- `schedule`: daily at `03:00 UTC`
- `workflow_dispatch`: manual run from the Actions UI

## Command quick reference

```text
@ciphertrust-bot help
@ciphertrust-bot features
@ciphertrust-bot risk
@ciphertrust-bot label
@ciphertrust-bot label bug
@ciphertrust-bot needs-repro
@ciphertrust-bot duplicate #123
@ciphertrust-bot summarize
@ciphertrust-bot groq-check
```

Only maintainers/collaborators can run commands. `/bot` and `@cipherbot` are intentionally not supported.

## AI usage

The bot is mostly deterministic and auditable. AI/Groq is only used for:

- optional issue label classification
- issue/PR summaries
- duplicate issue reasoning

The following features are deterministic and do not depend on AI:

- stale closing
- missing tests/docs detection
- risk scoring
- reviewer assignment
- safe auto-merge gates
- first-time contributor comments
- command parsing

## 1. Auto-label issues

**Where:** `terraform-bot/labeler.py`, `terraform-bot/triage.py`

When an issue is opened or edited, the bot reads the issue title/body and applies labels using keyword rules, provider-specific rules, and optional Groq classification.

Examples:

| Signal | Label |
| --- | --- |
| `fail`, `error`, `panic`, `authentication`, `token`, `credential` | `bug` |
| `docs`, `readme`, `example` | `documentation` |
| `feature`, `enhance`, `improve` | `enhancement` |
| `how`, `why`, `question`, `help` | `question` |
| `auth`, `token`, `credential`, `unauthorized` | `auth`, `security-review-required` |
| `provider config`, `provider block` | `provider-config` |
| `resource`, `data source` | `resource`, `data-source` |
| `key`, `kms`, `encrypt`, `decrypt`, `rotation` | `key-management` |
| `regression`, `worked before`, `after upgrade` | `regression` |

## 2. Auto-label PRs from title, body, and changed files

**Where:** `terraform-bot/pr_bot.py`, `terraform-bot/triage.py`

When a PR is opened, edited, synchronized, reopened, marked ready, or labeled, the bot looks at:

- PR title
- PR body
- Changed file paths

File-based labels include:

| Changed files | Label |
| --- | --- |
| `docs/**`, `*.md`, `**/*.md` | `documentation` |
| `examples/**` | `examples` |
| `.github/**` | `ci` |
| `*.go` | `go` |
| `*.tf` | `terraform` |
| `provider/**`, `*provider*` | `provider`, `provider-config` |
| `resource_*.go` | `resource` |
| `data_source_*.go` | `data-source` |
| `*_test.go`, `*acctest*` | `tests`, `acceptance-test` |
| `go.mod`, `go.sum` | `dependencies` |

## 3. Missing test detector

**Where:** `terraform-bot/triage.py`, `terraform-bot/pr_bot.py`

If a PR changes provider/internal Go code but does not change tests, the bot applies:

```text
needs-tests
```

It also comments with the reason, for example:

```text
provider/internal Go code changed but no test files were changed
```

This is deterministic and does not use AI.

## 4. Missing docs/examples detector

**Where:** `terraform-bot/triage.py`, `terraform-bot/pr_bot.py`

If a PR appears to change user-facing provider/resource behavior but does not update docs or examples, the bot applies:

```text
needs-docs
```

It comments with the reason, for example:

```text
user-facing provider/resource behavior may have changed but docs/examples were not updated
```

This is deterministic and does not use AI.

## 5. Terraform provider-specific labeler

**Where:** `terraform-bot/triage.py`

The bot now understands provider-specific areas:

```text
auth
provider-config
ciphertrust-manager
key-management
resource
data-source
regression
acceptance-test
security-review-required
breaking-change
risk/high
risk/medium
risk/low
```

These labels are derived from title/body text and changed file paths.

## 6. Auto-triage issue quality

**Where:** `terraform-bot/triage.py`, `terraform-bot/labeler.py`

For issues, the bot checks whether the report includes signals for:

- Terraform version
- Provider version
- Steps to reproduce
- Expected behavior
- Actual behavior or error output

If details are missing, it applies:

```text
needs-info
needs-repro
```

and comments asking the author to add the missing details.

## 7. Maintainer commands

**Where:** `terraform-bot/commands.py`

Maintainers can command the bot by commenting on an issue or PR. Only repo users with `OWNER`, `MEMBER`, or `COLLABORATOR` author association are allowed.

Supported commands:

```text
@ciphertrust-bot help
@ciphertrust-bot features
@ciphertrust-bot risk
@ciphertrust-bot label
@ciphertrust-bot label bug
@ciphertrust-bot needs-repro
@ciphertrust-bot duplicate #123
@ciphertrust-bot summarize
@ciphertrust-bot groq-check
```

## 8. Risk command

**Where:** `terraform-bot/commands.py`, `terraform-bot/triage.py`

Use:

```text
@ciphertrust-bot risk
```

On issues, it reads the title/body. On PRs, it also reads changed files.

It returns:

- risk level: `low`, `medium`, `high`, or `unknown`
- reasons
- suggested risk/security labels

Risk examples:

| Signal | Risk result |
| --- | --- |
| docs/examples only | `risk/low` |
| provider/internal Go code | `risk/medium` |
| auth/token/credential/secret/TLS files or wording | `risk/high`, `security-review-required` |
| workflow/bot/go.mod/go.sum changes | `risk/high` |
| breaking-change wording | `risk/high`, `breaking-change` |

## 9. Duplicate issue detection

**Where:** `terraform-bot/duplicates.py`

When a new issue is opened, the bot searches existing issues using:

- title keywords
- body keywords
- Terraform resource/data-source names
- auth/token/error signals
- similar error wording

It then tries:

1. Groq duplicate reasoning, if available.
2. Deterministic fallback scoring using overlapping words, resources, auth signals, and error wording.

If possible duplicates are found, the bot comments with candidate issues.

## 10. Helpful next-step PR comments

**Where:** `terraform-bot/pr_bot.py`

When a PR is opened, the bot comments with a first-pass maintainer checklist:

- confirm Terraform provider behavior is covered by tests
- confirm docs/examples are updated if user-facing behavior changed
- wait for CI to pass before merge

## 11. First-time contributor comments

**Where:** `terraform-bot/pr_bot.py`

If GitHub marks the PR author as `FIRST_TIMER` or `FIRST_TIME_CONTRIBUTOR`, the bot posts a friendly onboarding comment asking for:

- what changed
- why it changed
- how it was tested

This is deterministic and does not use AI.

## 12. Stale PR and stale issue cleanup

**Where:** `terraform-bot/stale_prs.py`

The scheduled/manual stale job scans open PRs and issues.

If a PR or issue has had no activity beyond the configured threshold, the bot:

1. Adds the stale label.
2. Comments explaining why it is being closed.
3. Closes it.

### Configuration

In `.github/workflows/terraform-bot.yml`:

```yaml
STALE_PR_DAYS: ${{ github.event.inputs.stale_pr_days || '30' }}
STALE_ISSUE_DAYS: ${{ github.event.inputs.stale_issue_days || '60' }}
STALE_PR_LABEL: stale
STALE_ISSUE_LABEL: stale
```

### Minute-based testing

Manual workflow runs support:

```text
stale_pr_minutes
```

For testing, run:

```text
Actions → Terraform Issue Bot → Run workflow
stale_pr_minutes = 5
```

That closes PRs inactive for 5+ minutes. Leave `stale_pr_minutes` empty in normal use.

## 13. Reviewer assignment by folder ownership

**Where:** `terraform-bot/pr_bot.py`

The bot has a simple ownership map:

```python
OWNERS={
    'provider/**':[],
    'internal/**':[],
    'examples/**':[],
    'docs/**':[],
    '*.md':[]
}
```

To enable reviewer assignment, add real GitHub usernames:

```python
OWNERS={
    'provider/**':['AdityaKukreti'],
    'internal/**':['AdityaKukreti'],
    'examples/**':['AdityaKukreti'],
    'docs/**':['AdityaKukreti'],
    '*.md':['AdityaKukreti']
}
```

When a changed file matches a pattern, the bot requests those reviewers.

## 14. Safe auto-merge

**Where:** `terraform-bot/pr_bot.py`

Auto-merge exists but is disabled by default.

```yaml
BOT_AUTO_MERGE: 'false'
BOT_AUTO_MERGE_LABEL: automerge
```

To even consider merging, all of these must be true:

1. `BOT_AUTO_MERGE=true`
2. PR has the `automerge` label
3. PR is open and not draft
4. PR author association is trusted: `OWNER`, `MEMBER`, or `COLLABORATOR`
5. PR is mergeable
6. `mergeable_state` is one of `clean`, `has_hooks`, or `unstable`
7. No high-risk files changed
8. PR is low-risk/docs/examples-only
9. At least one approval exists
10. No reviewer requested changes
11. Commit statuses/check runs are successful
12. Merge method defaults to `squash`

### High-risk files

Auto-merge is blocked if any changed file matches:

```text
.github/workflows/**
terraform-bot/**
go.mod
go.sum
**/*auth*
**/*credential*
**/*token*
**/*secret*
**/*tls*
```

### Low-risk files

Auto-merge is currently limited to docs/examples-only changes:

```text
docs/**
examples/**
*.md
**/*.md
```

This is intentional. Provider code and security-sensitive areas should require human merge.

## 15. Groq-backed summaries and checks

**Where:** `terraform-bot/llm.py`

Commands such as:

```text
@ciphertrust-bot summarize
@ciphertrust-bot groq-check
```

use Groq when `GROQ_API_KEY` is configured.

`groq-check` verifies that the key/model path is working.

## Natural-language command support: recommended design

Natural language should be added as a controlled intent router, not as direct LLM-to-GitHub mutation.

Recommended flow:

1. Comment starts with `@ciphertrust-bot`.
2. Existing explicit commands are checked first.
3. If no explicit command matches, send the remaining text to an LLM intent classifier.
4. The LLM returns a strict JSON intent, for example:

```json
{
  "intent": "apply_label",
  "confidence": 0.86,
  "args": {"label": "needs-tests"}
}
```

5. The bot validates the intent against an allowlist.
6. The bot validates the user is a maintainer/collaborator.
7. The bot executes only safe mapped functions.
8. If confidence is low, the bot asks for clarification instead of acting.

Recommended allowed intents:

```text
show_help
show_features
summarize
risk
label
needs_repro
mark_duplicate
triage
```

Do not allow natural language to directly trigger destructive actions like closing issues, merging PRs, or changing workflow files without explicit command syntax and strict confirmation.

## Testing checklist

### Test command parsing

Comment on an issue:

```text
@ciphertrust-bot help
```

Expected: bot replies with supported commands.

### Test features command

```text
@ciphertrust-bot features
```

Expected: bot replies with feature summary and link to this file.

### Test risk command

```text
@ciphertrust-bot risk
```

Expected: bot replies with deterministic risk level and reasons.

### Test label detection

Create or edit an issue with text like:

```text
Terraform plan fails with authentication token error
```

Expected: bot applies `bug`, `auth`, and possibly `security-review-required`.

### Test issue quality triage

Create an issue without reproduction steps or version details.

Expected: bot applies `needs-info` / `needs-repro` and asks for missing details.

### Test duplicate detection

Create a new issue with a title/body/error similar to an older issue.

Expected: bot comments with possible duplicate issues.

### Test PR labeling and quality checks

Open a PR that changes `provider/*.go` without tests/docs.

Expected: bot applies provider-specific labels plus `needs-tests` and possibly `needs-docs`.

### Test first-time contributor comment

Open a PR from an account GitHub marks as first-time contributor.

Expected: bot posts onboarding guidance.

### Test stale PR cleanup in minutes

Open a test PR, wait a few minutes, then manually run:

```text
Actions → Terraform Issue Bot → Run workflow
stale_pr_minutes = 5
```

Expected: if the PR has been inactive for 5+ minutes, the bot labels, comments, and closes it.

### Test auto-merge safely

Only after basic features work:

1. Keep the PR docs/examples-only.
2. Add `automerge` label.
3. Ensure CI passes.
4. Ensure at least one approval exists.
5. Temporarily set `BOT_AUTO_MERGE=true`.

Expected: bot merges only if all safety gates pass. Otherwise, it logs the skip reason.

## Current safety defaults

The bot is intentionally conservative:

- Auto-merge is off by default.
- Auto-merge only allows docs/examples/Markdown changes.
- High-risk files always block auto-merge.
- Commands only run for maintainers/collaborators.
- Stale cleanup is scheduled but configurable.
- Natural-language command support should be added with allowlisted intents only.
