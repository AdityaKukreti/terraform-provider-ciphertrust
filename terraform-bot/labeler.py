import subprocess as s

RULES={
'bug':['bug','error','fail','crash','panic','broken'],
'documentation':['docs','doc','readme','example'],
'enhancement':['feature','enhance','improve','request'],
'authentication':['auth','token','login','credential'],
'provider-config':['provider','configure','config'],
'resource':['resource'],
'data-source':['data source','datasource']
}

def run(issue):
    text=(issue.get('title','')+' '+str(issue.get('body'))).lower()
    labels=[k for k,v in RULES.items() if any(w in text for w in v)]
    if labels:
        s.run(['gh','issue','edit',str(issue['number']),'--add-label',','.join(labels)],check=False)
