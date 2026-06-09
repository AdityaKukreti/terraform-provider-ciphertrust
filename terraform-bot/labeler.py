import subprocess as s
import llm

RULES={
'bug':['bug','error','fail','failed','failure','crash','panic','broken','not working','unable','exception','auth','authentication','unauthorized','forbidden','credential','credentials','token','login'],
'documentation':['docs','doc','readme','example'],
'enhancement':['feature','enhance','improve','request'],
'question':['how','why','question','help']
}
CUSTOM_LABELS={
'needs-repro':('fbca04','Needs reproduction steps or environment details')
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
    for label in labels:
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
    labels+=llm.classify(issue)
    labels=sorted(set(labels))
    log('suggested labels for #'+str(issue.get('number'))+': '+(', '.join(labels) if labels else 'none'))
    return labels

def run(issue):
    labels=suggest(issue)
    if not labels:
        log('no labels to apply for #'+str(issue.get('number')))
        return [],[]
    added,failed=add_labels(issue['number'],labels)
    log('label result for #'+str(issue.get('number'))+': added='+((', '.join(added)) if added else 'none')+' failed='+(('; '.join(failed)) if failed else 'none'))
    return added,failed
