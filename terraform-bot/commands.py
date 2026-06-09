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
HELP='''## CipherTrust Bot Commands

| Command | Purpose |
| --- | --- |
| `@ciphertrust-bot help` | Show this help message |
| `@ciphertrust-bot features` | Show available bot features and config guide |
| `@ciphertrust-bot risk` | Show deterministic risk assessment |
| `@ciphertrust-bot label` | Auto-detect labels |
| `@ciphertrust-bot label bug` | Add one label manually |
| `@ciphertrust-bot check-labels` | Safely check missing/wrong bot-managed labels |
| `@ciphertrust-bot clean-labels` | Remove only inappropriate bot-managed labels |
| `@ciphertrust-bot triage` | Re-run labels and issue quality checks |
| `@ciphertrust-bot needs-repro` | Ask for reproduction details |
| `@ciphertrust-bot duplicate #123` | Mark as possible duplicate |
| `@ciphertrust-bot summarize` | Generate a maintainer summary |
| `@ciphertrust-bot groq-check` | Check Groq connectivity |

### Natural language examples

- `@ciphertrust-bot can you check the labels?`
- `@ciphertrust-bot clean up wrong labels`
- `@ciphertrust-bot what is the risk here?`
- `@ciphertrust-bot can you summarize this?`

_Handled by ciphertrust-bot._
'''
FEATURES='''## CipherTrust Terraform Bot Features

1. **Auto-label issues** from title/body
2. **Auto-label PRs** from title/body/changed files
3. **Missing test detector** for provider/internal code changes
4. **Missing docs/examples detector** for user-facing changes
5. **Terraform provider-specific labels**: `auth`, `provider-config`, `resource`, `data-source`, `key-management`, `regression`
6. **Issue quality triage**: `needs-info` and `needs-repro`
7. **Safe label checking**: adds missing bot-managed labels, reports questionable ones
8. **Conservative label cleanup**: removes only inappropriate bot-managed labels when explicitly requested
9. **Maintainer commands** through `@ciphertrust-bot ...`
10. **Duplicate issue detection** with keyword search, error/resource signals, and optional Groq reasoning
11. **Helpful next-step PR comments**
12. **First-time contributor PR comments**
13. **Stale PR and issue cleanup**
14. **Reviewer assignment** by folder ownership
15. **Safe auto-merge**, disabled by default
16. **Groq-backed summaries, checks, and safe natural-language intent routing**

Full feature and configuration guide: '''+FEATURES_URL+'''

_Handled by ciphertrust-bot._
'''

def log(msg):
    print('[terraform-bot][commands] '+msg,flush=True)

def md_label(label):
    return '`'+str(label)+'`'

def md_list(items):
    items=[str(x) for x in items if str(x)]
    if not items:return '- none'
    return '\n'.join('- '+x for x in items)

def md_label_list(labels):
    labels=sorted([str(x) for x in labels if str(x)])
    if not labels:return '- none'
    return '\n'.join('- '+md_label(x) for x in labels)

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
        if first in ('help','features','docs','guide','risk','label','labels','check-labels','check-label','clean-labels','clean-label','triage','needs-repro','summarize','summary','groq-check','duplicate'):
            return [first]+parts[1:],rest
        rlow=rest.lower()
        if any(x in rlow for x in ['clean label','clean up label','remove wrong label','remove inappropriate label']):
            return ['clean-labels'],rest
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
    parts=['## Label Update']
    parts.append('### Added')
    parts.append(md_label_list(added))
    if failed:
        parts.append('\n### Failed')
        parts.append(md_list(failed))
    parts.append('\n_Handled by ciphertrust-bot._')
    return comment(n,'\n'.join(parts))

def suggested_labels(issue):
    labels=labeler.suggest(issue)
    quality_labels,missing=triage.issue_quality(issue)
    return sorted(set(labels+quality_labels)),missing

def label_state(issue):
    current=set(current_label_names(issue))
    suggested,missing_info=suggested_labels(issue)
    suggested=set(suggested)
    managed=bot_managed_labels()
    missing=sorted([x for x in suggested if x not in current])
    questionable=sorted([x for x in current if x in managed and x not in suggested])
    return current,suggested,missing,questionable,missing_info

def check_labels_result(issue):
    current,suggested,missing,questionable,missing_info=label_state(issue)
    added,failed=labeler.add_labels(issue['number'],missing) if missing else ([],[])
    parts=['## Label Check Complete']
    parts.append('### Current labels')
    parts.append(md_label_list(current))
    parts.append('\n### Suggested bot-managed labels')
    parts.append(md_label_list(suggested))
    parts.append('\n### Added missing labels')
    parts.append(md_label_list(added))
    parts.append('\n### Possibly inappropriate bot-managed labels')
    parts.append(md_label_list(questionable))
    if missing_info:
        parts.append('\n### Missing issue details')
        parts.append(md_list(missing_info))
    if failed:
        parts.append('\n### Failures')
        parts.append(md_list(failed))
    parts.append('\n> No labels were removed. Manual/non-bot labels are preserved. Use `@ciphertrust-bot clean-labels` to remove only inappropriate bot-managed labels.')
    parts.append('\n_Handled by ciphertrust-bot._')
    return '\n'.join(parts)

def clean_labels_result(issue):
    current,suggested,missing,questionable,missing_info=label_state(issue)
    removed=[];failed=[]
    for label in questionable:
        try:
            gh.remove_label(issue['number'],label)
            removed.append(label)
        except Exception as e:
            failed.append(label+': '+type(e).__name__+': '+str(e)[:200])
    added,add_failed=labeler.add_labels(issue['number'],missing) if missing else ([],[])
    failed.extend(add_failed)
    preserved=sorted([x for x in current if x not in bot_managed_labels()])
    parts=['## Clean Labels Complete']
    parts.append('### Removed inappropriate bot-managed labels')
    parts.append(md_label_list(removed))
    parts.append('\n### Added missing bot-managed labels')
    parts.append(md_label_list(added))
    parts.append('\n### Preserved manual/custom labels')
    parts.append(md_label_list(preserved))
    if failed:
        parts.append('\n### Failures')
        parts.append(md_list(failed))
    parts.append('\n> Only bot-managed labels were eligible for removal.')
    parts.append('\n_Handled by ciphertrust-bot._')
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
    parts=['## Triage Complete']
    parts.append('### Added labels')
    parts.append(md_label_list(added))
    parts.append('\n### Suggested labels')
    parts.append(md_label_list(sorted(set(labels+quality_labels))))
    if missing:
        parts.append('\n### Missing issue details')
        parts.append(md_list(missing))
    if failed:
        parts.append('\n### Failures')
        parts.append(md_list(failed))
    parts.append('\n_Handled by ciphertrust-bot._')
    return '\n'.join(parts)

def run(issue,c):
    p,rest=parse_command(c.get('body',''),issue)
    if p is None:
        log('no command trigger matched for comment on #'+str(issue.get('number')))
        return
    n=issue['number']
    log('matched command on #'+str(n)+': '+' '.join(p))
    if c.get('author_association') not in ALLOWED:
        return comment(n,'> Only repo collaborators can run bot commands.')
    if len(p)<1 or p[0]=='help':return comment(n,HELP)
    cmd=p[0]
    if cmd in ('features','docs','guide'):
        return comment(n,FEATURES)
    if cmd=='risk':
        return comment(n,risk_result(issue))
    if cmd in ('check-labels','check-label'):
        return comment(n,check_labels_result(issue))
    if cmd in ('clean-labels','clean-label'):
        return comment(n,clean_labels_result(issue))
    if cmd in ('label','labels','triage'):
        if cmd=='label' and len(p)>1:return label_result(n,[' '.join(p[1:])])
        return comment(n,triage_result(issue))
    if cmd=='groq-check':return comment(n,'## Groq Check\n\n'+llm.status()+'\n\n_Handled by ciphertrust-bot._')
    if cmd in ('summarize','summary'):
        msg=llm.summarize(issue) or ('LLM summary unavailable. '+llm.LAST_ERROR)
        return comment(n,'## Summary\n\n'+msg+'\n\n_Handled by ciphertrust-bot._')
    if cmd=='needs-repro':
        msg=llm.summarize(issue) or 'Please add reproduction steps, expected/actual behavior, and provider/Terraform versions.'
        labeler.add_labels(n,['needs-repro']);return comment(n,'## Reproduction Details Needed\n\n'+msg+'\n\n_Handled by ciphertrust-bot._')
    if cmd=='duplicate' and len(p)>1:
        labeler.add_labels(n,['duplicate']);return comment(n,'## Possible Duplicate\n\nMarked as possible duplicate of '+md_label(p[1])+'.\n\n_Handled by ciphertrust-bot._')
    return comment(n,'> I did not understand that command. Try `@ciphertrust-bot help` or `@ciphertrust-bot features`.')
