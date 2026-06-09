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

## 1. Auto-label issues

**Where:** `terraform-bot/labeler.py`

When an issue is opened or edited, the bot reads the issue title and body, then applies labels based on keyword rules and optional LLM classification.

Current examples:

| Signal | Label |
| --- | --- |
| `fail`, `error`, `panic`, `authentication`, `token`, `credential` | `bug` |
| `docs`, `readme`, `example` | `documentation` |
| `feature`, `enhance`, `improve` | `enhancement` |
| `how`, `why`, `question`, `help` | `question` |

The bot also ensures known labels exist before applying them where supported.

## 2. Auto-label PRs from title, body, and changed files

**Where:** `terraform-bot/pr_bot.py`

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
| files containing `provider` | `provider` |
| files containing `test` | `tests` |

## 3. Maintainer commands

**Where:** `terraform-bot/commands.py`

Maintainers can command the bot by commenting on an issue or PR. Only repo users with `OWNER`, `MEMBER`, or `COLLABORATOR` author association are allowed.

Supported commands:

```text
@ciphertrust-bot help
@ciphertrust-bot label
@ciphertrust-bot label bug
@ciphertrust-bot needs-repro
@ciphertrust-bot duplicate #123
@ciphertrust-bot summarize
@ciphertrust-bot groq-check
```

Notes:

- `/bot` and `@cipherbot` have intentionally been removed.
- The only supported trigger is `@ciphertrust-bot`.

## 4. Duplicate issue detection

**Where:** `terraform-bot/duplicates.py`

When a new issue is opened, the bot searches existing issues using important words from the issue title.

It then tries:

1. LLM duplicate reasoning using Groq, if available.
2. Fallback title-similarity scoring.

If possible duplicates are found, the bot comments with a short list of candidate issues.

## 5. Helpful next-step comments

**Where:** `terraform-bot/pr_bot.py`

When a PR is opened, the bot comments with a first-pass maintainer checklist:

- confirm Terraform provider behavior is covered by tests
- confirm docs/examples are updated if user-facing behavior changed
- wait for CI to pass before merge

This gives contributors and maintainers a consistent checklist early in the PR lifecycle.

## 6. Stale PR and stale issue cleanup

**Where:** `terraform-bot/stale_prs.py`

The scheduled/manual stale job scans open PRs and issues.

### PR behavior

If a PR has had no activity beyond the configured threshold, the bot:

1. Adds the stale label.
2. Comments explaining why it is being closed.
3. Closes the PR.

### Issue behavior

If an issue has had no activity beyond the configured threshold, the bot:

1. Adds the stale label.
2. Comments explaining why it is being closed.
3. Closes the issue.

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

## 7. Reviewer assignment by folder ownership

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

## 8. Safe auto-merge

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
```

### Low-risk files

Auto-merge is currently limited to docs/examples-only changes:

```text
docs/**
examples/**
*.md
**/*.md
```

This is intentional. For now, provider code and security-sensitive areas should require human merge.

## 9. Groq-backed summaries and checks

**Where:** `terraform-bot/llm.py`

Commands such as:

```text
@ciphertrust-bot summarize
@ciphertrust-bot groq-check
```

use Groq when `GROQ_API_KEY` is configured.

`groq-check` verifies that the key/model path is working.

## Testing checklist

### Test command parsing

Comment on an issue:

```text
@ciphertrust-bot help
```

Expected: bot replies with supported commands.

### Test label detection

Create or edit an issue with text like:

```text
Terraform plan fails with authentication token error
```

Expected: bot applies `bug`.

### Test duplicate detection

Create a new issue with a title similar to an older issue.

Expected: bot comments with possible duplicate issues.

### Test PR labeling

Open a PR that changes `docs/` or `examples/`.

Expected: bot applies `documentation` or `examples` labels and posts a maintainer checklist.

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
