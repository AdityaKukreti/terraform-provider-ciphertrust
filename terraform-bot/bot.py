import json,os,requests as R
e=json.load(open(os.environ['GITHUB_EVENT_PATH']))
i=e.get('issue')or{}
if not i or 'pull_request' in i:quit()
s=(i.get('title','')+' '+(i.get('body')or'')).lower()
m={'bug':'bug error fail crash','documentation':'docs documentation readme','enhancement':'feature enhancement improve'}
l=[k for k,v in m.items()if any(w in s for w in v.split())]
if l:R.post