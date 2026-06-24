import os
import re
import bot_config
import github_api as gh
import llm
import labeler
import triage
import commenter

ALLOWED={'OWNER','MEMBER','COLLABORATOR'}
TRIGGERS=('@ciphertrust-bot',)

HELP='''## CipherTrust Bot Commands

| Command | Purpose |
| --- | --- |
| `@ciphertrust-bot help` | Show commands |
| `@ciphertrust-bot features` | Show feature summary |
| `@ciphertrust-bot label` | Apply suggested labels |
| `@ciphertrust-bot label bug` | Apply one label |
| `@ciphertrust-bot check-labels` | Add missing labels and report stale bot labels |
| `@ciphertrust-bot clean-labels` | Conservatively clean bot-managed labels |
| `@ciphertrust-bot duplicate #123` | Mark duplicate reference |
| `@ciphertrust-bot summarize` | Generate an AI-backed maintainer summary |
| `@ciphertrust-bot explain` | Explain the code changes in a PR (PR only) |

_Handled by ciphertrust-bot._'''

FEATURES='''## CipherTrust Bot Features

- Issue and PR auto-labeling
- Issue quality checks
- Strong duplicate detection
- Risk classification
- Missing tests/docs detection
- Tidy Markdown comments (automatic comments update in place; command replies repost fresh)
- Dashboard issue
- Stale cleanup
- AI-backed summaries and safe natural-language command routing

See `terraform-bot/WIKI.md` for the full documentation.

_Handled by ciphertrust-bot._'''


def allowed(comment):
    assoc=comment.get('author_association') or ''
    return assoc in ALLOWED


def is_self_or_bot(comment):
    """True if the comment was authored by the bot itself or any bot account.

    The bot posts as a COLLABORATOR, so it passes allowed(); without this guard
    it parses the example `@ciphertrust-bot ...` commands inside its own help and
    label-check output and triggers itself (see PR #130 cascade).
    """
    user=comment.get('user') or {}
    if (user.get('type') or '')=='Bot':
        return True
    me=gh.authenticated_login()
    return bool(me) and user.get('login')==me


def body_without_trigger(body):
    text=commenter.strip_code_and_quotes(body or '').strip()
    low=text.lower()
    for t in TRIGGERS:
        idx=low.find(t)
        if idx!=-1:
            return text[idx+len(t):].strip()
    return ''


def current_label_names(issue):
    return set(x.get('name') for x in issue.get('labels',[]) if x.get('name'))


# Labels clean-labels may remove: the LLM-governed content enum plus the factual
# quality labels. Excludes `duplicate` (from duplicate-detection) and every
# process/control label, so those are never stripped.
REMOVABLE=set(llm.LABEL_ENUM) | {'needs-info','needs-tests','needs-docs'}


def suggested_labels(issue):
    """Full label set the bot would apply now.

    LLM-primary content labels (labeler.suggest, reading PR files+diff when
    present) plus the factual labels: needs-tests/needs-docs for PRs,
    needs-info for issues. Returns (labels, files, patch).
    """
    num=issue['number']
    is_pr='pull_request' in issue
    files=gh.pr_files(num) if is_pr else None
    patch=gh.pr_patch(num) if is_pr else None
    labels=set(labeler.suggest(issue,files,patch))
    if is_pr:
        labels|=set(triage.missing_tests_docs(files)[0])
    else:
        labels|=set(labeler.assess_quality(issue)[0])
    return labels,files,patch


def parse_command(text):
    low=(text or '').lower().strip()
    if not low: return {'intent':'unknown','args':{}}
    parts=low.split()
    cmd=parts[0]
    if cmd in ['help','features','summarize','explain','check-labels','clean-labels','label']:
        return {'intent':cmd,'args':{'label':parts[1] if len(parts)>1 and cmd=='label' else None}}
    if cmd=='duplicate':
        m=re.search(r'#(\d+)',low)
        return {'intent':'duplicate','args':{'number':m.group(1) if m else None}}
    if re.search(r'\bcheck.{0,15}label',low): return {'intent':'check-labels','args':{}}
    if re.search(r'\b(clean|remove).{0,15}label',low): return {'intent':'clean-labels','args':{}}
    if re.search(r'\bsummar(ize|ise|y)\b',low): return {'intent':'summarize','args':{}}
    if re.search(r'\bfeatures?\b',low) or 'what can you do' in low: return {'intent':'features','args':{}}
    if bot_config.enabled('commands.natural_language',True):
        return {'intent':'unknown','args':{}}
    data=llm.intent(low)
    return {'intent':data.get('intent','unknown'),'args':data.get('args') or {}}


def check_labels(issue,clean=False):
    current=current_label_names(issue)
    # Both check-labels and clean-labels are LLM-primary (suggested_labels ->
    # labeler.suggest); the rule-based path is used only if the LLM call fails.
    suggested,_files,_patch=suggested_labels(issue)
    missing=sorted(suggested-current)
    stale=sorted((current-suggested) & REMOVABLE)
    for l in missing:
        gh.ensure_label(l); gh.add_labels(issue['number'],[l])
    removed=[]
    if clean:
        for l in stale:
            try:
                gh.remove_label(issue['number'],l); removed.append(l)
            except Exception:
                pass
    body='## Label check\n\n### Added\n'+('\n'.join('- `'+x+'`' for x in missing) or '- none')+'\n\n### Potentially stale bot labels (not removed — run `@ciphertrust-bot clean-labels` to remove)\n'+('\n'.join('- `'+x+'`' for x in stale) or '- none')
    if clean:
        body+='\n\n### Removed\n'+('\n'.join('- `'+x+'`' for x in removed) or '- none')
    body+='\n\n_Handled by ciphertrust-bot._'
    commenter.repost(issue['number'],'label-check' if not clean else 'label-cleanup',body)


def run(issue,comment):
    if is_self_or_bot(comment):
        return
    if not allowed(comment):
        return
    text=body_without_trigger(comment.get('body') or '')
    if not text:
        return
    parsed=parse_command(text)
    intent=parsed.get('intent')
    args=parsed.get('args') or {}
    num=issue['number']
    if intent=='help': commenter.repost(num,'help',HELP); return
    if intent=='features': commenter.repost(num,'features',FEATURES); return
    if intent=='summarize':
        if not os.getenv('GROQ_API_KEY'):
            commenter.repost(num,'summary','## Summary\n\nAI summary unavailable — `GROQ_API_KEY` is not configured.\n\n_Handled by ciphertrust-bot._')
            return
        patch=gh.pr_patch(num) if 'pull_request' in issue else None
        human_comments=None
        if 'pull_request' not in issue:
            bot_marker=commenter.BOT_MARKER_PREFIX
            raw=gh.issue_comments(num)
            human_comments='\n\n'.join(
                c.get('body','') for c in raw
                if bot_marker not in (c.get('body') or '')
            ) or None
        s=llm.summarize(issue.get('title'),issue.get('body'),patch=patch,comments=human_comments)
        commenter.repost(num,'summary','## Summary\n\n'+(s or 'AI summary unavailable (LLM call failed).')+'\n\n_Handled by ciphertrust-bot._')
        return
    if intent=='explain':
        if 'pull_request' not in issue:
            commenter.repost(num,'explain','`explain` works on PRs only — it reads the diff and explains the code changes. Try `@ciphertrust-bot summarize` for issue summaries.\n\n_Handled by ciphertrust-bot._')
            return
        if not os.getenv('GROQ_API_KEY'):
            commenter.repost(num,'explain','## Code Explanation\n\nAI explanation unavailable — `GROQ_API_KEY` is not configured.\n\n_Handled by ciphertrust-bot._')
            return
        patch=gh.pr_patch(num)
        explanation=llm.explain_pr(issue.get('title'),issue.get('body'),patch)
        commenter.repost(num,'explain','## Code Explanation\n\n'+(explanation or 'AI explanation unavailable (LLM call failed).')+'\n\n_Handled by ciphertrust-bot._')
        return
    if intent=='label':
        lab=args.get('label')
        labels=[lab] if lab else sorted(suggested_labels(issue)[0])
        for l in labels: gh.ensure_label(l)
        gh.add_labels(num,labels)
        applied=', '.join('`'+l+'`' for l in sorted(labels)) if labels else 'none'
        commenter.repost(num,'label','## Labels applied\n\nApplied: '+applied+'\n\n_Handled by ciphertrust-bot._')
        return
    if intent=='check-labels':
        check_labels(issue,clean=False); return
    if intent=='clean-labels': check_labels(issue,clean=True); return
    if intent=='duplicate':
        gh.ensure_label('duplicate'); gh.add_labels(num,['duplicate'])
        ref=args.get('number')
        commenter.repost(num,'duplicate','## Duplicate marker\n\nMarked as duplicate'+((' of #'+str(ref)) if ref else '')+'.\n\n_Handled by ciphertrust-bot._')
        return
    commenter.repost(num,'unknown','I could not safely map that request to a supported command. Try `@ciphertrust-bot help`.')
