import re

import commenter
import github_api as gh
import llm
import triage

CUSTOM_LABELS={
    'needs-info':'Issue needs more information',
    'needs-tests':'PR needs tests',
    'needs-docs':'PR needs docs or examples',
    'auth':'Authentication area',
    'provider-config':'Provider configuration area',
    'ciphertrust-manager':'CipherTrust Manager area',
    'resource':'Terraform resource area',
    'data-source':'Terraform data source area',
    'security':'Security-sensitive',
}
# Word-boundary regexes (text is lowercased before matching). Boundaries stop
# substring false positives like "helper"->question or "monkey"->key while a
# trailing stem (no closing \b) still catches inflections like fail/failed/failure.
RULES={
    'bug':[r'\bbug', r'\bfail', r'\berror', r'\bpanic', r'\bbroken\b', r'\bcrash'],
    'documentation':[r'\bdocs?\b', r'\bdocumentation\b', r'\breadme\b', r'\bexamples?\b'],
    'enhancement':[r'\bfeature', r'\benhance', r'\bimprove', r'\brequest'],
}


def bot_managed():
    return set(CUSTOM_LABELS.keys()) | set(RULES.keys())


def sync_labels(num, desired, current, add_only=False):
    desired=set(desired)
    current=set(current)
    if 'bot-labels-locked' in current:
        return
    managed=bot_managed()
    to_add=sorted(desired-current)
    # Never re-apply a label a maintainer deliberately removed. This holds in both
    # add-only (PR updates) and full-sync (issues) modes, so a maintainer's removal
    # is honored on issues and PRs alike.
    removed=gh.maintainer_removed_labels(num)
    if removed:
        to_add=[l for l in to_add if l not in removed]
    to_remove=[] if add_only else sorted((current-desired) & managed)
    for l in to_add:
        gh.ensure_label(l,description=CUSTOM_LABELS.get(l,'Managed by ciphertrust-bot'))
    if to_add:
        gh.add_labels(num,to_add)
    for l in to_remove:
        try:
            gh.remove_label(num,l)
        except Exception as e:
            gh.log('labels','failed removing '+l+' from #'+str(num)+': '+str(e)[:200])


def text(issue):
    return ((issue.get('title') or '')+'\n'+(issue.get('body') or '')).lower()


def suggest_rule_based(issue):
    """Rule-based label suggestions only — deterministic, no LLM."""
    t=text(issue)
    labels=set()
    for label,patterns in RULES.items():
        if any(re.search(p,t) for p in patterns): labels.add(label)
    labels.update(triage.provider_labels_from_text(issue))
    labels.update(triage.risk_report(issue).get('labels',[]))
    return sorted(labels)


def suggest(issue,files=None,patch=None):
    """LLM-primary content-label suggestions; deterministic rules as fallback.

    The LLM reads the issue/PR content (and, for PRs, the changed files + diff)
    and returns labels from the fixed enum. The keyword/path rules are used ONLY
    when the LLM call fails (no key, API error, unparseable reply), so labeling
    never goes dark. Returns content labels only — needs-tests/needs-docs
    (factual) and needs-info (completeness) are added by the callers.
    """
    is_pr='pull_request' in issue
    try:
        llm_labels=llm.classify_labels(issue.get('title'),issue.get('body'),files=files,patch=patch,context='PR' if is_pr else 'issue')
    except Exception:
        llm_labels=None
    if llm_labels is not None:
        return sorted(set(llm_labels))
    gh.log('labels','#'+str(issue.get('number'))+': LLM label classification unavailable, using rule fallback')
    labels=set(suggest_rule_based(issue))
    if files:
        for f in files:
            lf=str(f).lower()
            if lf.endswith('.md') or lf.startswith('docs/'):
                labels.add('documentation')
        labels.update(triage.provider_labels_from_files(files))
        labels.update(triage.risk_report(issue,files).get('labels',[]))
    return sorted(labels)


def assess_quality(issue):
    """Issue-completeness check: LLM-primary, regex fallback.

    Completeness is a semantic judgment, so the LLM is authoritative when it
    answers. When it is unavailable (no key, API error, unparseable reply) we
    fall back to the deterministic regex check and log it, so triage never goes
    silently dark. Returns (labels, missing) like triage.issue_quality.
    """
    body=issue.get('body') or ''
    missing=llm.assess_quality(issue.get('title'),body)
    if missing is None:
        gh.log('quality','#'+str(issue.get('number'))+': LLM quality assessment unavailable, using regex fallback')
        return triage.issue_quality(issue)
    return triage.quality_labels_from_missing(body,missing),missing


def run(issue):
    num=issue['number']
    desired=set(suggest(issue))
    quality_labels,missing=assess_quality(issue)
    desired.update(quality_labels)
    current=set(x.get('name') for x in issue.get('labels',[]) if x.get('name'))
    sync_labels(num,desired,current)
    msg=triage.issue_quality_comment(missing)
    if msg:
        commenter.upsert(num,'issue-quality',msg)
    elif commenter.find_existing_comment(num,'issue-quality'):
        commenter.upsert(num,'issue-quality','All required issue information is now present.\n\n_Handled by ciphertrust-bot._')
