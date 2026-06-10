import datetime
import github_api as gh
import bot_config


def label_names(item):
    return [x.get('name') for x in item.get('labels',[]) if x.get('name')]


def find_dashboard_issue(title):
    for issue in gh.list_open_issues():
        if issue.get('title')==title:
            return issue
    return None


def build_body():
    prs=gh.list_open_prs()
    issues=gh.list_open_issues()
    queue=[]; risks=[]; needs=[]
    q_label=bot_config.get('merge_queue.label','merge-queue')
    for pr in prs:
        labels=label_names(pr)
        if q_label in labels:
            queue.append(pr)
        if any(x.startswith('risk/') for x in labels):
            risks.append(pr)
        if any(x in labels for x in ['needs-tests','needs-docs','needs-info','needs-repro']):
            needs.append(pr)
    issue_needs=[i for i in issues if any(x in label_names(i) for x in ['needs-info','needs-repro'])]
    lines=['## CipherTrust Bot Dashboard','']
    lines.append('_Last updated: '+datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z_')
    lines.append('')
    lines.append('| Area | Count |')
    lines.append('| --- | ---: |')
    lines.append('| Open PRs | '+str(len(prs))+' |')
    lines.append('| Open issues | '+str(len(issues))+' |')
    lines.append('| Merge queue PRs | '+str(len(queue))+' |')
    lines.append('| Risk-labeled PRs | '+str(len(risks))+' |')
    lines.append('| PRs needing tests/docs/info | '+str(len(needs))+' |')
    lines.append('| Issues needing info/repro | '+str(len(issue_needs))+' |')
    lines.append('')
    lines.append('### Merge queue')
    if queue:
        for pr in queue[:20]:
            lines.append('- #'+str(pr.get('number'))+' '+pr.get('title',''))
    else:
        lines.append('- none')
    lines.append('')
    lines.append('### Attention needed')
    attention=needs[:10]+issue_needs[:10]
    if attention:
        for item in attention[:20]:
            labels=', '.join(label_names(item))
            lines.append('- #'+str(item.get('number'))+' '+item.get('title','')+' — `'+labels+'`')
    else:
        lines.append('- none')
    lines.append('')
    lines.append('_Managed by ciphertrust-bot._')
    return '\n'.join(lines)


def run():
    title=bot_config.get('bot.dashboard_issue_title','CipherTrust Bot Dashboard')
    body=build_body()
    issue=find_dashboard_issue(title)
    if issue:
        gh.api('/issues/'+str(issue['number']),method='PATCH',body={'body':body},area='dashboard')
        gh.log('dashboard','updated dashboard issue #'+str(issue['number']))
    else:
        gh.api('/issues',method='POST',body={'title':title,'body':body,'labels':['bot-dashboard']},area='dashboard')
        gh.log('dashboard','created dashboard issue')
