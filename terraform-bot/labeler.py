import subprocess as s
import llm

RULES={
'bug':['bug','error','fail','crash','panic','broken'],
'documentation':['docs','doc','readme','example'],
'enhancement':['feature','enhance','improve','request'],
'question':['how','why','question','help']
}
CUSTOM_LABELS={
'needs-repro':('fbca04','Needs reproduction steps or environment details')
}

def ensure_label(label):
    if label not in CUSTOM_LABELS:return True
    color,desc=CUSTOM_LABELS[label]
    r=s.run(['gh','label','create',label,'--color',color,'--description',desc,'--force'],capture_output=True,text=True)
    return r.returncode==0

def add_labels(issue_number,labels):
    added=[];failed=[]
    for label in labels:
        if not ensure_label(label):
            failed.append(label);continue
        r=s.run(['gh','issue','edit',str(issue_number),'--add-label',label],capture_output=True,text=True)
        if r.returncode==0:added.append(label)
        else:failed.append(label+': '+(r.stderr or r.stdout)[-200:])
    return added,failed

def suggest(issue):
    text=(issue.get('title','')+' '+str(issue.get('body'))).lower()
    labels=[k for k,v in RULES.items() if any(w in text for w in v)]
    labels+=llm.classify(issue)
    return sorted(set(labels))

def run(issue):
    labels=suggest(issue)
    if labels:add_labels(issue['number'],labels)
