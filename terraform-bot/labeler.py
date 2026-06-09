import subprocess as s
import llm

RULES={
'bug':['bug','error','fail','crash','panic','broken'],
'documentation':['docs','doc','readme','example'],
'enhancement':['feature','enhance','improve','request'],
'question':['how','why','question','help']
}

def run(issue):
    text=(issue.get('title','')+' '+str(issue.get('body'))).lower()
    labels=[k for k,v in RULES.items() if any(w in text for w in v)]
    labels+=llm.classify(issue)
    labels=sorted(set(labels))
    if labels:
        s.run(['gh','issue','edit',str(issue['number']),'--add-label',','.join(labels)],check=False)
