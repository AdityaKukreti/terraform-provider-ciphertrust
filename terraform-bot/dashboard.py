from datetime import datetime, timezone
import github_api as gh
import bot_config


def label_names(item):
    return [l.get('name') for l in item.get('labels',[]) if l.get('name')]


def build_body(issues):
    prs=gh.list_open_prs()
    needs=[p for p in prs if any(l in label_names(p) for l in ['needs-tests','needs-docs','needs-info'])]
    issue_needs=[i for i in issues if any(l in label_names(i) for l in ['needs-info'])]
    lines=['# CipherTrust Bot Dashboard','', 'Updated: '+datetime.now(timezone.utc).isoformat(),'']
    lines+=['## Summary','', '| Metric | Count |','| --- | --- |',f'| Open PRs | {len(prs)} |',f'| Open issues | {len(issues)} |',f'| PRs needing tests/docs/info | {len(needs)} |',f'| Issues needing info | {len(issue_needs)} |','']
    lines.append('## Attention needed')
    lines.extend(['- PR #'+str(p.get('number'))+' '+p.get('title','')+' — '+', '.join(label_names(p)) for p in needs[:20]] or ['- none'])
    lines.append('\n_Updated by ciphertrust-bot._')
    return '\n'.join(lines)


def run():
    title=bot_config.get('bot.dashboard_issue_title','CipherTrust Bot Dashboard')
    issues=gh.list_open_issues()
    body=build_body(issues)
    existing=next((i for i in issues if i.get('title')==title),None)
    if existing:
        gh.api('/issues/'+str(existing['number']),method='PATCH',body={'body':body},area='dashboard')
        # The dashboard is the bot's own bookkeeping issue — never let stale cleanup
        # warn or close it. Backfill no-stale on dashboards created before this guard.
        if 'no-stale' not in label_names(existing):
            gh.ensure_label('no-stale')
            try:
                gh.add_labels(existing['number'],['no-stale'])
            except Exception as e:
                gh.log('dashboard','failed adding no-stale to #'+str(existing['number'])+': '+str(e)[:200])
    else:
        gh.ensure_label('bot-dashboard'); gh.ensure_label('no-stale')
        gh.api('/issues',method='POST',body={'title':title,'body':body,'labels':['bot-dashboard','no-stale']},area='dashboard')
