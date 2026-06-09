import json
import os
import urllib.parse
import urllib.request

USER_AGENT='ciphertrust-terraform-bot'


def log(area,msg):
    print('[terraform-bot]['+area+'] '+str(msg),flush=True)


def repo():
    return os.getenv('GITHUB_REPOSITORY')


def token():
    return os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')


def api(path,method='GET',body=None,area='github'):
    r=repo(); t=token()
    if not r or not t:
        raise RuntimeError('missing GITHUB_REPOSITORY or token')
    url='https://api.github.com/repos/'+r+path
    data=None if body is None else json.dumps(body).encode('utf-8')
    req=urllib.request.Request(url,data=data,method=method,headers={
        'Authorization':'Bearer '+t,
        'Accept':'application/vnd.github+json',
        'X-GitHub-Api-Version':'2022-11-28',
        'Content-Type':'application/json',
        'User-Agent':USER_AGENT
    })
    with urllib.request.urlopen(req,timeout=30) as resp:
        raw=resp.read().decode('utf-8')
        return json.loads(raw) if raw else None


def quote(value):
    return urllib.parse.quote(str(value),safe='')


def add_comment(issue_number,body):
    res=api('/issues/'+str(issue_number)+'/comments',method='POST',body={'body':body},area='comments')
    log('comments','commented on #'+str(issue_number))
    return res


def ensure_label(name,color='ededed',description='Managed by ciphertrust-bot'):
    try:
        api('/labels/'+quote(name),area='labels')
        return True
    except Exception:
        pass
    try:
        api('/labels',method='POST',body={'name':name,'color':color,'description':description},area='labels')
        log('labels','created label '+name)
        return True
    except Exception as e:
        log('labels','failed creating label '+name+': '+type(e).__name__+': '+str(e)[:300])
        return False


def add_labels(issue_number,labels):
    if not labels:return []
    api('/issues/'+str(issue_number)+'/labels',method='POST',body={'labels':labels},area='labels')
    log('labels','added '+', '.join(labels)+' to #'+str(issue_number))
    return labels


def close_issue(issue_number):
    api('/issues/'+str(issue_number),method='PATCH',body={'state':'closed'},area='issues')
    log('issues','closed #'+str(issue_number))


def close_pr(pr_number):
    api('/pulls/'+str(pr_number),method='PATCH',body={'state':'closed'},area='prs')
    log('prs','closed PR #'+str(pr_number))


def list_open_prs():
    prs=[]; page=1
    while True:
        batch=api('/pulls?state=open&sort=updated&direction=asc&per_page=100&page='+str(page),area='prs')
        if not batch:break
        prs.extend(batch)
        if len(batch)<100:break
        page+=1
    return prs


def list_open_issues():
    issues=[]; page=1
    while True:
        batch=api('/issues?state=open&sort=updated&direction=asc&per_page=100&page='+str(page),area='issues')
        if not batch:break
        issues.extend([x for x in batch if 'pull_request' not in x])
        if len(batch)<100:break
        page+=1
    return issues


def pr_files(pr_number):
    files=[]; page=1
    while True:
        batch=api('/pulls/'+str(pr_number)+'/files?per_page=100&page='+str(page),area='prs')
        if not batch:break
        files.extend([f.get('filename','') for f in batch])
        if len(batch)<100:break
        page+=1
    return files


def request_reviewers(pr_number,reviewers):
    if not reviewers:return
    api('/pulls/'+str(pr_number)+'/requested_reviewers',method='POST',body={'reviewers':reviewers},area='reviewers')
    log('reviewers','requested '+', '.join(reviewers)+' on PR #'+str(pr_number))


def merge_pr(pr_number,method='squash'):
    api('/pulls/'+str(pr_number)+'/merge',method='PUT',body={'merge_method':method},area='merge')
    log('merge','merged PR #'+str(pr_number)+' via '+method)
