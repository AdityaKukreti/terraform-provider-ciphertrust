import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

STALE_PR_DAYS=int(os.getenv('STALE_PR_DAYS','30'))
STALE_ISSUE_DAYS=int(os.getenv('STALE_ISSUE_DAYS','60'))
STALE_MINUTES=os.getenv('STALE_PR_MINUTES','').strip()
STALE_PR_LABEL=os.getenv('STALE_PR_LABEL','stale')
STALE_ISSUE_LABEL=os.getenv('STALE_ISSUE_LABEL','stale')
BOT_NAME='terraform-bot/stale'


def log(msg):
    print('[terraform-bot][stale] '+msg,flush=True)


def token():
    return os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')


def repo():
    return os.getenv('GITHUB_REPOSITORY')


def api(path,method='GET',body=None):
    t=token(); r=repo()
    if not t or not r:
        raise RuntimeError('missing GITHUB_REPOSITORY or token')
    url='https://api.github.com/repos/'+r+path
    data=None if body is None else json.dumps(body).encode('utf-8')
    req=urllib.request.Request(url,data=data,method=method,headers={
        'Authorization':'Bearer '+t,
        'Accept':'application/vnd.github+json',
        'X-GitHub-Api-Version':'2022-11-28',
        'Content-Type':'application/json',
        'User-Agent':BOT_NAME
    })
    with urllib.request.urlopen(req,timeout=30) as resp:
        raw=resp.read().decode('utf-8')
        return json.loads(raw) if raw else None


def pr_threshold_seconds():
    if STALE_MINUTES:
        return int(STALE_MINUTES)*60,'minute(s)',int(STALE_MINUTES)
    return STALE_PR_DAYS*24*60*60,'day(s)',STALE_PR_DAYS


def issue_threshold_seconds():
    return STALE_ISSUE_DAYS*24*60*60,'day(s)',STALE_ISSUE_DAYS


def ensure_label(label,description):
    try:
        api('/labels/'+urllib.parse.quote(label),method='GET')
        return
    except Exception:
        pass
    try:
        api('/labels',method='POST',body={
            'name':label,
            'color':'d73a4a',
            'description':description
        })
        log('created label '+label)
    except Exception as e:
        log('could not create label '+label+': '+type(e).__name__+': '+str(e)[:300])


def comment(issue_number,body,kind):
    api('/issues/'+str(issue_number)+'/comments',method='POST',body={'body':body})
    log('commented on '+kind+' #'+str(issue_number))


def add_label(issue_number,label,kind):
    api('/issues/'+str(issue_number)+'/labels',method='POST',body={'labels':[label]})
    log('added label '+label+' to '+kind+' #'+str(issue_number))


def close_issue(issue_number,kind='issue'):
    api('/issues/'+str(issue_number),method='PATCH',body={'state':'closed'})
    log('closed '+kind+' #'+str(issue_number))


def close_pr(pr_number):
    api('/pulls/'+str(pr_number),method='PATCH',body={'state':'closed'})
    log('closed PR #'+str(pr_number))


def parse_time(value):
    return datetime.fromisoformat(value.replace('Z','+00:00'))


def list_open_prs():
    prs=[]; page=1
    while True:
        batch=api('/pulls?state=open&sort=updated&direction=asc&per_page=100&page='+str(page))
        if not batch:break
        prs.extend(batch)
        if len(batch)<100:break
        page+=1
    return prs


def list_open_issues():
    items=[]; page=1
    while True:
        batch=api('/issues?state=open&sort=updated&direction=asc&per_page=100&page='+str(page))
        if not batch:break
        items.extend([x for x in batch if 'pull_request' not in x])
        if len(batch)<100:break
        page+=1
    return items


def human_age(seconds):
    minutes=int(seconds//60)
    if minutes<60:return str(minutes)+' minute(s)'
    hours=int(minutes//60)
    if hours<48:return str(hours)+' hour(s)'
    return str(int(hours//24))+' day(s)'


def handle_prs(now):
    threshold,unit,value=pr_threshold_seconds()
    ensure_label(STALE_PR_LABEL,'PR closed automatically after long inactivity')
    prs=list_open_prs()
    log('scanning '+str(len(prs))+' open PR(s); stale threshold='+str(value)+' '+unit)
    closed=0
    for pr in prs:
        num=pr['number']
        updated=parse_time(pr['updated_at'])
        age_seconds=(now-updated).total_seconds()
        title=pr.get('title','')
        if age_seconds<threshold:
            log('skip PR #'+str(num)+' age='+human_age(age_seconds)+' title='+title)
            continue
        body=(
            'Closing this PR automatically because it has had no activity for '
            +human_age(age_seconds)+'.\n\n'
            'If this is still relevant, please reopen it or create a fresh PR with the latest changes.\n\n'
            '_Handled by ciphertrust-bot._'
        )
        try:
            add_label(num,STALE_PR_LABEL,'PR')
            comment(num,body,'PR')
            close_pr(num)
            closed+=1
        except Exception as e:
            log('failed handling PR #'+str(num)+': '+type(e).__name__+': '+str(e)[:500])
    log('stale PR scan complete; closed='+str(closed))


def handle_issues(now):
    threshold,unit,value=issue_threshold_seconds()
    ensure_label(STALE_ISSUE_LABEL,'Issue closed automatically after long inactivity')
    issues=list_open_issues()
    log('scanning '+str(len(issues))+' open issue(s); stale threshold='+str(value)+' '+unit)
    closed=0
    for issue in issues:
        num=issue['number']
        updated=parse_time(issue['updated_at'])
        age_seconds=(now-updated).total_seconds()
        title=issue.get('title','')
        if age_seconds<threshold:
            log('skip issue #'+str(num)+' age='+human_age(age_seconds)+' title='+title)
            continue
        body=(
            'Closing this issue automatically because it has had no activity for '
            +human_age(age_seconds)+'.\n\n'
            'If this is still relevant, please reopen it with updated details.\n\n'
            '_Handled by ciphertrust-bot._'
        )
        try:
            add_label(num,STALE_ISSUE_LABEL,'issue')
            comment(num,body,'issue')
            close_issue(num,'issue')
            closed+=1
        except Exception as e:
            log('failed handling issue #'+str(num)+': '+type(e).__name__+': '+str(e)[:500])
    log('stale issue scan complete; closed='+str(closed))


def run():
    now=datetime.now(timezone.utc)
    handle_prs(now)
    handle_issues(now)
