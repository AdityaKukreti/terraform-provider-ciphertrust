import json
import os
import urllib.request
import llm
import labeler
import triage
import github_api as gh
ALLOWED={'OWNER','MEMBER','COLLABORATOR'}
TRIGGERS=('@ciphertrust-bot',)
FEATURES_URL='https://github.com/AdityaKukreti/terraform-provider-ciphertrust/blob/main/terraform-bot/FEATURES.md'
HELP='''Terraform bot commands:\n- `@ciphertrust-bot help`\n- `@ciphertrust-bot features` show available bot features and config guide\n- `@ciphertrust-bot risk` show deterministic risk assessment\n- `@ciphertrust-bot label` auto-detect labels\n- `@ciphertrust-bot label bug` add one label manually\n- `@ciphertrust-bot needs-repro`\n- `@ciphertrust-bot duplicate #123`\n- `@ciphertrust-bot summarize`\n- `@ciphertrust-bot groq-check`\n'''
FEATURES='''CipherTrust Terraform Bot features:\n\n1. Auto-label issues from title/body\n2. Auto-label PRs from title/body/changed files\n3. Missing test detector for provider/internal code changes\n4. Missing docs/examples detector for user-facing changes\n5. Terraform provider-specific labels: auth, provider-config, resource, data-source, key-management, regression\n6. Issue quality triage: needs-info and needs-repro\n7. Maintainer commands through `@ciphertrust-bot ...`\n8. Duplicate issue detection with keyword search, error/resource signals, and optional Groq reasoning\n9. Helpful next-step PR comments\n10. First-time contributor PR comments\n11. Stale PR and issue cleanup\n12. Reviewer assignment by folder ownership\n13. Safe auto-merge, disabled by default\n14. Groq-backed summaries and checks\n\nFull feature and configuration guide:\n'''+FEATURES_URL

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

def risk_result(issue):
    files=[]
    if 'pull_request' in issue:
        try:
            files=gh.pr_files(issue['number'])
        except Exception as e:
            log('failed fetching PR files for risk command: '+type(e).__name__+': '+str(e)[:300])
    return triage.risk_markdown(issue,files)

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
    if cmd in ('features','docs','guide'):
        return comment(n,FEATURES)
    if cmd=='risk':
        return comment(n,risk_result(issue))
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
