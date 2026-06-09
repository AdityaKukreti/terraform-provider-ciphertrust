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
HELP='''Terraform bot commands:\n- `@ciphertrust-bot help`\n- `@ciphertrust-bot features` show available bot features and config guide\n- `@ciphertrust-bot risk` show deterministic risk assessment\n- `@ciphertrust-bot label` auto-detect labels\n- `@ciphertrust-bot label bug` add one label manually\n- `@ciphertrust-bot check-labels` safely check missing/wrong bot-managed labels\n- `@ciphertrust-bot triage` re-run labels and issue quality checks\n- `@ciphertrust-bot needs-repro`\n- `@ciphertrust-bot duplicate #123`\n- `@ciphertrust-bot summarize`\n- `@ciphertrust-bot groq-check`\n\nNatural language examples:\n- `@ciphertrust-bot can you check the labels?`\n- `@ciphertrust-bot what is the risk here?`\n- `@ciphertrust-bot can you summarize this?`\n'''
FEATURES='''CipherTrust Terraform Bot features:\n\n1. Auto-label issues from title/body\n2. Auto-label PRs from title/body/changed files\n3. Missing test detector for provider/internal code changes\n4. Missing docs/examples detector for user-facing changes\n5. Terraform provider-specific labels: auth, provider-config, resource, data-source, key-management, regression\n6. Issue quality triage: needs-info and needs-repro\n7. Safe label checking: adds missing bot-managed labels, reports questionable ones, never auto-removes\n8. Maintainer commands through `@ciphertrust-bot ...`\n9. Duplicate issue detection with keyword search, error/resource signals, and optional Groq reasoning\n10. Helpful next-step PR comments\n11. First-time contributor PR comments\n12. Stale PR and issue cleanup\n13. Reviewer assignment by folder ownership\n14. Safe auto-merge, disabled by default\n15. Groq-backed summaries, checks, and safe natural-language intent routing\n\nFull feature and configuration guide:\n'''+FEATURES_URL

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

def parse_command(body,issue):
    body=body.strip()
    low=body.lower()
    for t in TRIGGERS:
        if not low.startswith(t):
            continue
        rest=body[len(t):].strip()
        parts=rest.split()
        if not parts:
            return [],rest
        first=parts[0].lower().strip('.,?!')
        if first in ('help','features','docs','guide','risk','label','labels','check-labels','check-label','triage','needs-repro','summarize','summary','groq-check','duplicate'):
            return [first]+parts[1:],rest
        rlow=rest.lower()
        if any(x in rlow for x in ['check the label','check labels','what labels','which labels','label this','triage this','run triage']):
            return ['check-labels'],rest
        if any(x in rlow for x in ['risk','safe','dangerous','high risk','low risk']):
            return ['risk'],rest
        if any(x in rlow for x in ['summarize','summary','explain this','what is this about']):
            return ['summarize'],rest
        if any(x in rlow for x in ['features','what can you do','capabilities','docs','guide']):
            return ['features'],rest
        intent=llm.intent(rest,issue)
        name=intent.get('intent','unknown')
        if name!='unknown':
            args=intent.get('args',{}) or {}
            if name=='triage':
                return ['check-labels'],rest
            if name=='duplicate' and args.get('duplicate_of'):
                return ['duplicate',str(args.get('duplicate_of'))],rest
            return [name],rest
        return parts,rest
    return None,''

def current_label_names(issue):
    return sorted([x.get('name') for x in issue.get('labels',[]) if x.get('name')])

def bot_managed_labels():
    return set(labeler.CUSTOM_LABELS.keys())|set(labeler.RULES.keys())|set(llm.ALLOWED)

def label_result(n,labels):
    added,failed=labeler.add_labels(n,labels)
    parts=[]
    if added:parts.append('Added labels: '+', '.join(added))
    if failed:parts.append('Failed labels: '+', '.join(failed))
    return comment(n,'\n'.join(parts) if parts else 'No labels changed.')

def suggested_labels(issue):
    labels=labeler.suggest(issue)
    quality_labels,missing=triage.issue_quality(issue)
    return sorted(set(labels+quality_labels)),missing

def check_labels_result(issue):
    current=set(current_label_names(issue))
    suggested,missing_info=suggested_labels(issue)
    suggested=set(suggested)
    managed=bot_managed_labels()
    missing=sorted([x for x in suggested if x not in current])
    questionable=sorted([x for x in current if x in managed and x not in suggested])
    added,failed=labeler.add_labels(issue['number'],missing) if missing else ([],[])
    parts=['Label check complete.']
    parts.append('Current labels: '+(', '.join(sorted(current)) if current else 'none'))
    parts.append('Suggested bot-managed labels: '+(', '.join(sorted(suggested)) if suggested else 'none'))
    if added:parts.append('Added missing labels: '+', '.join(added))
    if questionable:
        parts.append('Possibly inappropriate bot-managed labels, not removed: '+', '.join(questionable))
    else:
        parts.append('No questionable bot-managed labels found.')
    if missing_info:
        parts.append('Missing issue details: '+', '.join(missing_info))
    if failed:parts.append('Failed labels: '+', '.join(failed))
    parts.append('\nI did not remove any labels. Manual/non-bot labels are preserved.')
    return '\n'.join(parts)

def risk_result(issue):
    files=[]
    if 'pull_request' in issue:
        try:
            files=gh.pr_files(issue['number'])
        except Exception as e:
            log('failed fetching PR files for risk command: '+type(e).__name__+': '+str(e)[:300])
    return triage.risk_markdown(issue,files)

def triage_result(issue):
    added,failed=labeler.run(issue)
    labels=labeler.suggest(issue)
    quality_labels,missing=triage.issue_quality(issue)
    parts=['Triage complete.']
    if added:parts.append('Added labels: '+', '.join(added))
    if labels or quality_labels:parts.append('Suggested labels: '+', '.join(sorted(set(labels+quality_labels))))
    if missing:parts.append('Missing issue details: '+', '.join(missing))
    if failed:parts.append('Failed labels: '+', '.join(failed))
    if len(parts)==1:parts.append('No label changes detected.')
    return '\n'.join(parts)

def run(issue,c):
    p,rest=parse_command(c.get('body',''),issue)
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
    if cmd in ('check-labels','check-label'):
        return comment(n,check_labels_result(issue))
    if cmd in ('label','labels','triage'):
        if cmd=='label' and len(p)>1:return label_result(n,[' '.join(p[1:])])
        return comment(n,triage_result(issue))
    if cmd=='groq-check':return comment(n,llm.status())
    if cmd in ('summarize','summary'):
        msg=llm.summarize(issue) or ('LLM summary unavailable. '+llm.LAST_ERROR)
        return comment(n,msg)
    if cmd=='needs-repro':
        msg=llm.summarize(issue) or 'Please add reproduction steps, expected/actual behavior, and provider/Terraform versions.'
        labeler.add_labels(n,['needs-repro']);return comment(n,msg)
    if cmd=='duplicate' and len(p)>1:
        labeler.add_labels(n,['duplicate']);return comment(n,'Possible duplicate of '+p[1])
    return comment(n,'I did not understand that command. Try `@ciphertrust-bot help` or `@ciphertrust-bot features`.')
