import github_api as gh
import labeler
import triage
import commenter

FIRST_TIMER_ASSOCIATIONS={'FIRST_TIMER','FIRST_TIME_CONTRIBUTOR'}


def md_label_list(labels):
    labels=sorted([str(x) for x in labels if str(x)])
    return '\n'.join('- `'+x+'`' for x in labels) if labels else '- none'


def first_time_contributor_comment(pr):
    if pr.get('author_association') not in FIRST_TIMER_ASSOCIATIONS:
        return
    body='## Welcome\n\nThanks for your first contribution. Please include what changed, why it changed, and how it was tested.\n\n_Handled by ciphertrust-bot._'
    commenter.upsert(pr['number'],'first-time-contributor',body)


def pr_triage_comment(files,labels,missing_reasons,risk):
    parts=['## PR Triage','']
    parts+=['### Detected labels',md_label_list(labels),'']
    parts+=['### Changed files','- '+str(len(files))+' file(s) checked','']
    if missing_reasons:
        parts.append('### Missing checks')
        parts.extend('- '+r for r in missing_reasons)
        parts.append('')
    if risk.get('level')=='high':
        parts.append('### Risk')
        parts.extend('- '+r for r in risk.get('reasons',[]))
        parts.append('')
    parts+=['### Maintainer checklist',
            '- confirm Terraform provider behavior is covered by tests',
            '- confirm docs/examples are updated if user-facing behavior changed',
            '- wait for CI to pass before maintainer review',
            '']
    parts.append('_Handled by ciphertrust-bot._')
    return '\n'.join(parts)


def run(pr,action):
    num=pr['number']
    files=gh.pr_files(num)
    patch=gh.pr_patch(num)
    risk=triage.risk_report(pr,files)
    missing_labels,missing_reasons=triage.missing_tests_docs(files)
    # Content/area labels come from the LLM (reading files + diff), or the rule
    # fallback inside suggest(); needs-tests/needs-docs stay factual.
    labels=sorted(set(labeler.suggest(pr,files,patch)) | set(missing_labels))
    current=set(x.get('name') for x in pr.get('labels',[]) if x.get('name'))
    labeler.sync_labels(num,labels,current,add_only=(action!='opened'))
    if action=='opened':
        commenter.upsert(num,'pr-triage',pr_triage_comment(files,labels,missing_reasons,risk))
        first_time_contributor_comment(pr)
    elif action in ('synchronize','ready_for_review') and (missing_reasons or risk.get('level')=='high'):
        commenter.upsert(num,'pr-triage',pr_triage_comment(files,labels,missing_reasons,risk))
