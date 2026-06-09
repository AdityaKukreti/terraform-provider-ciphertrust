import os
import fnmatch
import github_api as gh
import labeler
import triage

AUTO_MERGE=os.getenv('BOT_AUTO_MERGE','false').lower()=='true'
AUTO_MERGE_LABEL=os.getenv('BOT_AUTO_MERGE_LABEL','automerge')
AUTO_MERGE_METHOD=os.getenv('BOT_AUTO_MERGE_METHOD','squash')
TRUSTED_ASSOCIATIONS={'OWNER','MEMBER','COLLABORATOR'}
SAFE_AUTHOR_ASSOCIATIONS=set(os.getenv('BOT_AUTO_MERGE_TRUSTED_ASSOCIATIONS','OWNER,MEMBER,COLLABORATOR').split(','))
HIGH_RISK_PATTERNS=triage.HIGH_RISK_PATTERNS
LOW_RISK_PATTERNS=triage.DOC_PATTERNS
FIRST_TIMER_ASSOCIATIONS={'FIRST_TIMER','FIRST_TIME_CONTRIBUTOR'}

# Simple ownership map. Replace reviewers with real GitHub usernames when ready.
OWNERS={
    'provider/**':[],
    'internal/**':[],
    'examples/**':[],
    'docs/**':[],
    '*.md':[]
}


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
    reviewers=set()
    for f in files:
        for pattern,names in OWNERS.items():
            if fnmatch.fnmatch(f,pattern):
                reviewers.update(names)
    return sorted(reviewers)


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
        'Thanks for your first contribution to this repository.\n\n'
        'A maintainer will review it soon. Please make sure the PR description includes what changed, why it changed, and how it was tested.\n\n'
        '_Handled by ciphertrust-bot._'
    )
    gh.add_comment(pr['number'],body)


def next_steps(pr,files,labels):
    num=pr['number']
    parts=[]
    parts.append('Thanks for the PR. I ran the first-pass automation checks.')
    if labels:
        parts.append('Detected labels: '+', '.join(labels)+'.')
    if files:
        parts.append('Changed files checked: '+str(len(files))+'.')
    parts.append('Maintainer checklist:')
    parts.append('- confirm Terraform provider behavior is covered by tests')
    parts.append('- confirm docs/examples are updated if user-facing behavior changed')
    parts.append('- wait for CI to pass before merge')
    parts.append('\n_Handled by ciphertrust-bot._')
    gh.add_comment(num,'\n'.join(parts))


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
    return True,'safe to auto-merge'


def try_auto_merge(pr,files):
    num=pr['number']
    ok,reason=auto_merge_decision(pr,files)
    if not ok:
        gh.log('automerge','skip PR #'+str(num)+': '+reason)
        return
    gh.log('automerge','merging PR #'+str(num)+': '+reason)
    gh.merge_pr(num,AUTO_MERGE_METHOD)


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
    if action=='opened':
        next_steps(pr,files,labels)
        try:
            first_time_contributor_comment(pr)
        except Exception as e:
            gh.log('first-time','failed first-time contributor comment on PR #'+str(num)+': '+type(e).__name__+': '+str(e)[:300])
    quality_msg=triage.pr_quality_comment(missing_reasons,risk)
    if quality_msg and action in ('opened','synchronize','ready_for_review'):
        try:
            gh.add_comment(num,quality_msg)
        except Exception as e:
            gh.log('quality','failed PR quality comment on #'+str(num)+': '+type(e).__name__+': '+str(e)[:300])
    try_auto_merge(pr,files)
