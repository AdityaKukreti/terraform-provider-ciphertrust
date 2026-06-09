import json
import os
import subprocess as s
import urllib.request
import llm
import labeler
ALLOWED={'OWNER','MEMBER','COLLABORATOR'}
TRIGGERS=('/bot','@cipherbot','@ciphertrust-bot')
HELP='''Terraform bot commands:\n- `/bot help`, `@cipherbot help`, or `@ciphertrust-bot help`\n- `/bot label`, `@cipherbot label`, or `@ciphertrust-bot label` auto-detect labels\n- `/bot label bug`, `@cipherbot label bug`, or `@ciphertrust-bot label bug` add one label manually\n- `/bot needs-repro`, `@cipherbot needs-repro`, or `@ciphertrust-bot needs-repro`\n- `/bot duplicate #123`, `@cipherbot duplicate #123`, or `@ciphertrust-bot duplicate #123`\n- `/bot summarize`, `@cipherbot summarize`, or `@ciphertrust-bot summarize`\n- `/bot groq-check`, `@cipherbot groq-check`, or `@ciphertrust-bot groq-check`\n'''

def log(msg):
    print('[terraform-bot][commands] '+msg,flush=True)

def comment(n,msg):
    repo=os.getenv('GITHUB_REPOSITORY')
    token=os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if not repo or not token:
        log('cannot comment: missing GITHUB_REPOSITORY or token')
        return False
    url='https://api.github.com/repos/'+repo+'/issues/'+str(n)+'/comments'
    data=json.dumps({'body':msg}).encode('utf-8')
    req=urllib.request.Request(url,data=data,method='POST',headers={
        'Authorization':'Bearer '+token,
        'Accept':'application/vnd.github+json',
        'X-GitHub-Api-Version':'2022-11-28',
        'Content-Type':'application/json',
        'User-Agent':'terraform-issue-bot'
    })
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            log('commented on #'+str(n)+' via REST, status='+str(r.status))
            return True
    except Exception as e:
        log('failed to comment on #'+str(n)+' via REST: '+type(e).__name__+': '+str(e)[:500])
        return False

def parse_command(body):
    body=body.strip()
    low=body.lower()
    for t in TRIGGERS:
        if low.startswith(t):
            rest=body[len(t):].strip()
            return rest.split()
    return None

def label_result(n,labels):
    added,failed=labeler.add_labels(n,labels)
    parts=[]
    if added:parts.append('Added labels: '+', '.join(added))
    if failed:parts.append('Failed labels: '+', '.join(failed))
    return comment(n,'\n'.join(parts) if parts else 'No labels changed.')

def run(issue,c):
    p=parse_command(c.get('body',''))
    if p is None:
        log('no command trigger matched for comment on #'+str(issue.get('number')))
        return
    n=issue['number']
    log('matched command on #'+str(n)+': '+' '.join(p))
    if c.get('author_association') not in ALLOWED:
        return comment(n,'Only repo collaborators can run bot commands.')
    if len(p)<1 or p[0]=='help':return comment(n,HELP)
    cmd=p[0]
    if cmd=='groq-check':return comment(n,llm.status())
    if cmd=='summarize':
        msg=llm.summarize(issue) or ('LLM summary unavailable. '+llm.LAST_ERROR)
        return comment(n,msg)
    if cmd=='label':
        if len(p)>1:return label_result(n,[' '.join(p[1:])])
        labels=labeler.suggest(issue)
        if not labels:return comment(n,'No matching labels detected for this issue.')
        return label_result(n,labels)
    if cmd=='needs-repro':
        msg=llm.summarize(issue) or 'Please add reproduction steps, expected/actual behavior, and provider/Terraform versions.'
        labeler.add_labels(n,['needs-repro']);return comment(n,msg)
    if cmd=='duplicate' and len(p)>1:
        labeler.add_labels(n,['duplicate']);return comment(n,'Possible duplicate of '+p[1])
