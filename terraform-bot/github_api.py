import json
import os
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT='ciphertrust-terraform-bot'


def log(area,msg):
    print('[terraform-bot]['+area+'] '+str(msg),flush=True)


def repo():
    return os.getenv('GITHUB_REPOSITORY')


def token():
    return os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')


def _request(url,method='GET',body=None):
    t=token()
    if not t:
        raise RuntimeError('missing token')
    data=None if body is None else json.dumps(body).encode('utf-8')
    req=urllib.request.Request(url,data=data,method=method,headers={
        'Authorization':'Bearer '+t,
        'Accept':'application/vnd.github+json',
        'X-GitHub-Api-Version':'2022-11-28',
        'Content-Type':'application/json',
        'User-Agent':USER_AGENT,
    })
    try:
        with urllib.request.urlopen(req,timeout=30) as resp:
            raw=resp.read().decode('utf-8')
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        try:
            detail=e.read().decode('utf-8','replace')[:400]
        except Exception:
            detail=''
        raise RuntimeError('GitHub API '+method+' '+str(e.code)+(': '+detail if detail else '')) from e


def api(path,method='GET',body=None,area='github'):
    r=repo()
    if not r:
        raise RuntimeError('missing GITHUB_REPOSITORY')
    return _request('https://api.github.com/repos/'+r+path,method=method,body=body)


def global_api(path,method='GET',body=None,area='github'):
    return _request('https://api.github.com'+path,method=method,body=body)


_AUTH_LOGIN=None


def authenticated_login():
    """Login of the account behind the token (cached).

    Used so the bot never processes its own comments as commands — its help and
    label-check output embed example `@ciphertrust-bot ...` commands, which would
    otherwise self-trigger. Best-effort: returns '' if the lookup fails.
    """
    global _AUTH_LOGIN
    if _AUTH_LOGIN is None:
        try:
            me=global_api('/user')
            _AUTH_LOGIN=(me or {}).get('login') or ''
        except Exception as e:
            log('github','could not resolve authenticated login: '+type(e).__name__+': '+str(e)[:200])
            _AUTH_LOGIN=''
    return _AUTH_LOGIN


def quote(value):
    return urllib.parse.quote(str(value),safe='')


def add_comment(issue_number,body):
    res=api('/issues/'+str(issue_number)+'/comments',method='POST',body={'body':body},area='comments')
    log('comments','commented on #'+str(issue_number))
    return res


def issue_comments(issue_number):
    comments=[]; page=1
    while True:
        batch=api('/issues/'+str(issue_number)+'/comments?per_page=100&page='+str(page),area='comments')
        if not batch:break
        comments.extend(batch)
        if len(batch)<100:break
        page+=1
    return comments


def issue_events(issue_number):
    events=[]; page=1
    while True:
        batch=api('/issues/'+str(issue_number)+'/events?per_page=100&page='+str(page),area='events')
        if not batch:break
        events.extend(batch)
        if len(batch)<100:break
        page+=1
    return events


def maintainer_removed_labels(issue_number):
    """Labels that were removed (unlabeled event) on this issue/PR.

    Used by add-only label sync so the bot never re-applies a label a
    maintainer deliberately removed. Best-effort: any API failure yields
    an empty set, falling back to prior behavior.
    """
    removed=set()
    try:
        for e in issue_events(issue_number):
            if e.get('event')=='unlabeled':
                name=(e.get('label') or {}).get('name')
                if name:
                    removed.add(name)
    except Exception as e:
        log('labels','could not read events for #'+str(issue_number)+': '+type(e).__name__+': '+str(e)[:200])
    return removed


def update_comment(comment_id,body):
    res=api('/issues/comments/'+str(comment_id),method='PATCH',body={'body':body},area='comments')
    log('comments','updated comment '+str(comment_id))
    return res


def delete_comment(comment_id):
    api('/issues/comments/'+str(comment_id),method='DELETE',area='comments')
    log('comments','deleted comment '+str(comment_id))


def ensure_label(name,color='ededed',description='Managed by ciphertrust-bot'):
    try:
        api('/labels/'+quote(name),area='labels')
        return True
    except RuntimeError as e:
        if '404' not in str(e):
            log('labels','ensure_label check failed for '+name+': '+str(e)[:200])
            return False
    except Exception as e:
        log('labels','ensure_label check failed for '+name+': '+type(e).__name__+': '+str(e)[:200])
        return False
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


def remove_label(issue_number,label):
    api('/issues/'+str(issue_number)+'/labels/'+quote(label),method='DELETE',area='labels')
    log('labels','removed '+label+' from #'+str(issue_number))


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


def search_issues(query,limit=20):
    q='repo:'+repo()+' is:issue '+query
    try:
        res=global_api('/search/issues?q='+quote(q)+'&sort=updated&order=desc&per_page='+str(min(limit,100)),area='search')
        return res.get('items',[]) if isinstance(res,dict) else []
    except Exception as e:
        log('search','issue search failed for '+query+': '+type(e).__name__+': '+str(e)[:200])
        return []


def pr_file_metadata(pr_number):
    files=[]; page=1
    while True:
        batch=api('/pulls/'+str(pr_number)+'/files?per_page=100&page='+str(page),area='prs')
        if not batch:break
        files.extend(batch)
        if len(batch)<100:break
        page+=1
    return files


def pr_files(pr_number):
    return [f.get('filename','') for f in pr_file_metadata(pr_number)]


def pr_patch(pr_number,max_chars=6000):
    patches=[]
    for f in pr_file_metadata(pr_number):
        name=f.get('filename','')
        patch=f.get('patch') or ''
        if patch:
            patches.append('--- '+name+'\n'+patch)
    full='\n'.join(patches)
    if len(full)>max_chars:
        cut=full.rfind('\n',0,max_chars)
        cut=cut if cut>0 else max_chars
        return full[:cut]+'\n\n_[diff truncated — explanation covers partial changes only]_'
    return full
