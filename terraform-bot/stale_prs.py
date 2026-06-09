import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

STALE_DAYS=int(os.getenv('STALE_PR_DAYS','30'))
STALE_LABEL=os.getenv('STALE_PR_LABEL','stale')
BOT_NAME='terraform-bot/stale-prs'


def log(msg):
    print('[terraform-bot][stale-prs] '+msg,flush=True)


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


def ensure_label():
    try:
        api('/labels/'+urllib.parse.quote(STALE_LABEL),method='GET')
        return
    except Exception:
        pass
    try:
        api('/labels',method='POST',body={
            'name':STALE_LABEL,
            'color':'d73a4a',
            'description':'PR closed automatically after long inactivity'
        })
        log('created label '+STALE_LABEL)
    except Exception as e:
        log('could not create label '+STALE_LABEL+': '+type(e).__name__+': '+str(e)[:300])


def comment(issue_number,body):
    api('/issues/'+str(issue_number)+'/comments',method='POST',body={'body':body})
    log('commented on PR #'+str(issue_number))


def add_label(issue_number):
    api('/issues/'+str(issue_number)+'/labels',method='POST',body={'labels':[STALE_LABEL]})
    log('added label '+STALE_LABEL+' to PR #'+str(issue_number))


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


def run():
    now=datetime.now(timezone.utc)
    ensure_label()
    prs=list_open_prs()
    log('scanning '+str(len(prs))+' open PR(s); stale threshold='+str(STALE_DAYS)+' day(s)')
    closed=0
    for pr in prs:
        num=pr['number']
        updated=parse_time(pr['updated_at'])
        age=(now-updated).days
        title=pr.get('title','')
        if age<STALE_DAYS:
            log('skip PR #'+str(num)+' age='+str(age)+'d title='+title)
            continue
        body=(
            'Closing this PR automatically because it has had no activity for '
            +str(age)+' days.\n\n'
            'If this is still relevant, please reopen it or create a fresh PR with the latest changes.\n\n'
            '_Handled by ciphertrust-bot._'
        )
        try:
            add_label(num)
            comment(num,body)
            close_pr(num)
            closed+=1
        except Exception as e:
            log('failed handling PR #'+str(num)+': '+type(e).__name__+': '+str(e)[:500])
    log('stale PR scan complete; closed='+str(closed))
