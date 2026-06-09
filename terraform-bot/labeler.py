import subprocess as s
import llm
import triage
import github_api as gh

RULES={
'bug':['bug','error','fail','failed','failure','crash','panic','broken','not working','unable','exception','auth','authentication','unauthorized','forbidden','credential','credentials','token','login'],
'documentation':['docs','doc','readme','example'],
'enhancement':['feature','enhance','improve','request'],
'question':['how','why','question','help']
}
CUSTOM_LABELS={
'needs-repro':('fbca04','Needs reproduction steps or environment details'),
'needs-info':('fbca04','Needs more issue details'),
'needs-tests':('fbca04','Needs tests or test confirmation'),
'needs-docs':('0075ca','Needs docs or examples update'),
'auth':('d73a4a','Authentication or authorization related'),
'provider-config':('c5def5','Provider configuration related'),
'ciphertrust-manager':('5319e7','CipherTrust Manager related'),
'key-management':('1d76db','Key management related'),
'resource':('bfd4f2','Terraform resource related'),
'data-source':('bfd4f2','Terraform data source related'),
'regression':('d73a4a','Regression report'),
'acceptance-test':('0e8a16','Acceptance test related'),
'security-review-required':('b60205','Security-sensitive change requiring review'),
'breaking-change':('b60205','Potential breaking change'),
'risk/high':('b60205','High-risk change'),
'risk/medium':('fbca04','Medium-risk change'),
'risk/low':('0e8a16','Low-risk change')
}

def log(msg):
    print('[terraform-bot][labeler] '+msg,flush=True)

def ensure_label(label):
    if label not in CUSTOM_LABELS:return True
    color,desc=CUSTOM_LABELS[label]
    r=s.run(['gh','label','create',label,'--color',color,'--description',desc,'--force'],capture_output=True,text=True)
    if r.returncode!=0:
        log('failed to ensure label '+label+': '+(r.stderr or r.stdout)[-500:])
    return r.returncode==0

def add_labels(issue_number,labels):
    added=[];failed=[]
    for label in sorted(set(labels)):
        if not ensure_label(label):
            failed.append(label);continue
        r=s.run(['gh','issue','edit',str(issue_number),'--add-label',label],capture_output=True,text=True)
        if r.returncode==0:
            added.append(label)
            log('added label '+label+' to #'+str(issue_number))
        else:
            reason=label+': '+(r.stderr or r.stdout)[-500:]
            failed.append(reason)
            log('failed label '+reason)
    return added,failed

def suggest(issue):
    text=(issue.get('title','')+' '+str(issue.get('body'))).lower()
    labels=[k for k,v in RULES.items() if any(w in text for w in v)]
    labels+=triage.provider_labels_from_text(issue)
    labels+=triage.risk_report(issue).get('labels',[])
    labels+=llm.classify(issue)
    labels=sorted(set(labels))
    log('suggested labels for #'+str(issue.get('number'))+': '+(', '.join(labels) if labels else 'none'))
    return labels

def run(issue):
    labels=suggest(issue)
    quality_labels,missing=triage.issue_quality(issue)
    labels=sorted(set(labels+quality_labels))
    if not labels:
        log('no labels to apply for #'+str(issue.get('number')))
        return [],[]
    added,failed=add_labels(issue['number'],labels)
    if missing:
        msg=triage.issue_quality_comment(missing)
        if msg:
            try: gh.add_comment(issue['number'],msg)
            except Exception as e: log('failed issue quality comment: '+type(e).__name__+': '+str(e)[:300])
    log('label result for #'+str(issue.get('number'))+': added='+((', '.join(added)) if added else 'none')+' failed='+(('; '.join(failed)) if failed else 'none'))
    return added,failed
