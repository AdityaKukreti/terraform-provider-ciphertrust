import os
import fnmatch
import github_api as gh
import labeler
import triage
import bot_config
import owners
import commenter

AUTO_MERGE=os.getenv('BOT_AUTO_MERGE',str(bot_config.get('auto_merge.enabled',False))).lower()=='true'
AUTO_MERGE_LABEL=os.getenv('BOT_AUTO_MERGE_LABEL',bot_config.get('auto_merge.label','automerge'))
SAFE_AUTHOR_ASSOCIATIONS=set(os.getenv('BOT_AUTO_MERGE_TRUSTED_ASSOCIATIONS',','.join(bot_config.get('auto_merge.trusted_author_associations',['OWNER','MEMBER','COLLABORATOR']))).split(','))
HIGH_RISK_PATTERNS=bot_config.get('risk.high_risk_paths',triage.HIGH_RISK_PATTERNS) or triage.HIGH_RISK_PATTERNS
LOW_RISK_PATTERNS=bot_config.get('risk.low_risk_paths',triage.DOC_PATTERNS) or triage.DOC_PATTERNS
FIRST_TIMER_ASSOCIATIONS={'FIRST_TIMER','FIRST_TIME_CONTRIBUTOR'}


def md_label(label):
    return '`'+str(label)+'`'


def md_label_list(labels):
    labels=sorted([str(x) for x in labels if str(x)])
    if not labels:return '- none'
    return '\n'.join('- '+md_label(x) for x in labels)


def labels_from_files(files):
    labels=set()
    for f in files:
        low=f.lower()
        if low.endswith('.md') or low.startswith('docs/'):
            labels.add('documentation')
        if low.startswith('examples/'):
            labels.add('examples')
        if low.startswith('.github/'):
            labels.add('ci')
        if low.endswith('.go'):
            labels.add('go')
        if low.endswith('.tf'):
            labels.add('terraform')
        if 'provider' in low:
            labels.add('provider')
        if 'test' in low:
            labels.add('tests')
    labels.update(triage.provider_labels_from_files(files))
    return sorted(labels)


def reviewers_for_files(files):
    return owners.reviewers_for_files(files)


def matches_any(path,patterns):
    return any(fnmatch.fnmatch(path,p) for p in patterns)


def risky_files(files):
    return [f for f in files if matches_any(f,HIGH_RISK_PATTERNS)]


def all_files_low_risk(files):
    return bool(files) and all(matches_any(f,LOW_RISK_PATTERNS) for f in files)


def latest_review_states(reviews):
    states={}
    for r in reviews:
        user=(r.get('user') or {}).get('login')
        if not user:continue
        states[user]=r.get('state')
    return states


def has_approval_and_no_block(reviews):
    states=latest_review_states(reviews)
    if any(v=='CHANGES_REQUESTED' for v in states.values()):
        return False,'changes requested by reviewer'
    if not any(v=='APPROVED' for v in states.values()):
        return False,'no maintainer approval found'
    return True,'approved'


def checks_green(sha):
    status=gh.combined_status(sha)
    if status.get('state') not in ('success','pending'):
        return False,'commit status is '+str(status.get('state'))
    checks=gh.check_runs(sha)
    relevant=[c for c in checks if c.get('name')!='Run Terraform issue bot']
    if not relevant and status.get('state')=='pending':
        return False,'checks are still pending'
    bad=[c.get('name') for c in relevant if c.get('conclusion') not in ('success','neutral','skipped')]
    waiting=[c.get('name') for c in relevant if c.get('status')!='completed']
    if waiting:
        return False,'checks still running: '+', '.join(waiting[:5])
    if bad:
        return False,'checks failed: '+', '.join(bad[:5])
    return True,'checks passed'


def first_time_contributor_comment(pr):
    if pr.get('author_association') not in FIRST_TIMER_ASSOCIATIONS:
        return
    body=(
        '## Welcome\n\n'
        'Thanks for your first contribution to this repository.\n\n'
        'Please make sure the PR description includes:\n\n'
        '- what changed\n'
        '- why it changed\n'
        '- how it was tested\n\n'
        '_Handled by ciphertrust-bot._'
    )
    commenter.upsert(pr['number'],'first-time-contributor',body)


def next_steps(pr,files,labels):
    num=pr['number']
    parts=['## First-pass PR Checks','']
    parts.append('I ran the first-pass automation checks for this PR.')
    parts.append('')
    parts.append('### Detected labels')
    parts.append(md_label_list(labels))
    parts.append('')
    parts.append('### Changed files')
    parts.append('- '+str(len(files))+' file(s) checked')
    parts.append('')
    parts.append('### Maintainer checklist')
    parts.append('- confirm Terraform provider behavior is covered by tests')
    parts.append('- confirm docs/examples are updated if user-facing behavior changed')
    parts.append('- wait for CI to pass before merge')
    parts.append('')
    parts.append('_Handled by ciphertrust-bot._')
    commenter.upsert(num,'pr-next-steps','\n'.join(parts))


def auto_merge_decision(pr,files):
    num=pr['number']
    labels=[x['name'] for x in pr.get('labels',[])]
    if not AUTO_MERGE:
        return False,'auto-merge disabled'
    if AUTO_MERGE_LABEL not in labels:
        return False,'missing '+AUTO_MERGE_LABEL+' label'
    fresh=gh.get_pr(num)
    if fresh.get('draft'):
        return False,'draft PR'
    if fresh.get('state')!='open':
        return False,'PR is not open'
    author_assoc=fresh.get('author_association','')
    if author_assoc not in SAFE_AUTHOR_ASSOCIATIONS:
        return False,'untrusted author association: '+str(author_assoc)
    mergeable=fresh.get('mergeable')
    mergeable_state=fresh.get('mergeable_state')
    if mergeable is False:
        return False,'PR is not mergeable'
    if mergeable_state not in ('clean','has_hooks','unstable'):
        return False,'unsafe mergeable_state: '+str(mergeable_state)
    risky=risky_files(files)
    if risky:
        return False,'high-risk files changed: '+', '.join(risky[:5])
    if not all_files_low_risk(files):
        return False,'not a low-risk/docs/examples-only PR'
    reviews=gh.pr_reviews(num)
    ok,reason=has_approval_and_no_block(reviews)
    if not ok:
        return False,reason
    sha=(fresh.get('head') or {}).get('sha')
    if not sha:
        return False,'missing head sha'
    ok,reason=checks_green(sha)
    if not ok:
        return False,reason
    return True,'eligible for maintainer-controlled merge'


def report_merge_candidate(pr,files):
    ok,reason=auto_merge_decision(pr,files)
    gh.log('automerge','PR #'+str(pr['number'])+': '+reason)
    if ok:
        commenter.upsert(pr['number'],'merge-candidate','## Merge Candidate\n\nThis PR appears eligible under the configured safety gates.\n\n> The bot does not merge automatically in this mode. Maintainers remain in control.\n\n_Handled by ciphertrust-bot._')


def maybe_enqueue(pr,files,risk):
    if not bot_config.enabled('merge_queue.enabled',True):
        return
    q_label=bot_config.get('merge_queue.label','merge-queue')
    current=[x.get('name') for x in pr.get('labels',[])]
    if q_label in current or risk.get('level')=='high':
        return
    if all_files_low_risk(files) or risk.get('level') in ('low','medium'):
        gh.ensure_label(q_label,description='Tracked by lightweight ciphertrust-bot merge queue')
        try:
            gh.add_labels(pr['number'],[q_label])
        except Exception as e:
            gh.log('merge-queue','failed adding queue label to PR #'+str(pr['number'])+': '+type(e).__name__+': '+str(e)[:300])


def run(pr,action):
    num=pr['number']
    files=gh.pr_files(num)
    risk=triage.risk_report(pr,files)
    missing_labels,missing_reasons=triage.missing_tests_docs(files)
    labels=sorted(set(labeler.suggest(pr)+labels_from_files(files)+risk.get('labels',[])+missing_labels))
    if labels:
        for l in labels:
            gh.ensure_label(l)
        gh.add_labels(num,labels)
    reviewers=reviewers_for_files(files)
    if reviewers:
        try:
            gh.request_reviewers(num,reviewers)
        except Exception as e:
            gh.log('reviewers','failed requesting reviewers on PR #'+str(num)+': '+type(e).__name__+': '+str(e)[:300])
    maybe_enqueue(pr,files,risk)
    if action=='opened':
        next_steps(pr,files,labels)
        try:
            first_time_contributor_comment(pr)
        except Exception as e:
            gh.log('first-time','failed first-time contributor comment on PR #'+str(num)+': '+type(e).__name__+': '+str(e)[:300])
    quality_msg=triage.pr_quality_comment(missing_reasons,risk)
    if quality_msg and action in ('opened','synchronize','ready_for_review'):
        try:
            commenter.upsert(num,'pr-quality',quality_msg+'\n\n_Handled by ciphertrust-bot._')
        except Exception as e:
            gh.log('quality','failed PR quality comment on #'+str(num)+': '+type(e).__name__+': '+str(e)[:300])
    report_merge_candidate(pr,files)
