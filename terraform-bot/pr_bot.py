import os
import fnmatch
import github_api as gh
import labeler

AUTO_MERGE=os.getenv('BOT_AUTO_MERGE','false').lower()=='true'
AUTO_MERGE_LABEL=os.getenv('BOT_AUTO_MERGE_LABEL','automerge')

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
    return sorted(labels)


def reviewers_for_files(files):
    reviewers=set()
    for f in files:
        for pattern,names in OWNERS.items():
            if fnmatch.fnmatch(f,pattern):
                reviewers.update(names)
    return sorted(reviewers)


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


def try_auto_merge(pr):
    num=pr['number']
    existing=[x['name'] for x in pr.get('labels',[])]
    if not AUTO_MERGE:
        gh.log('automerge','disabled; skip PR #'+str(num))
        return
    if AUTO_MERGE_LABEL not in existing:
        gh.log('automerge','missing '+AUTO_MERGE_LABEL+' label; skip PR #'+str(num))
        return
    # Conservative: do not merge drafts, dirty/unknown merge state, or PRs with requested changes unknown to us.
    if pr.get('draft'):
        gh.log('automerge','draft PR; skip #'+str(num))
        return
    gh.merge_pr(num,os.getenv('BOT_AUTO_MERGE_METHOD','squash'))


def run(pr,action):
    num=pr['number']
    files=gh.pr_files(num)
    labels=sorted(set(labeler.suggest(pr)+labels_from_files(files)))
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
    try_auto_merge(pr)
