import json,os,subprocess as s
e=json.load(open(os.environ['GITHUB_EVENT_PATH']));i=e.get('issue')or{}
t=(i.get('title','')+' '+str(i.get('body'))).lower()
L=[]
if any(x in t for x in'bug error fail crash'.split()):L+=['bug']
if any(x in t for x in'feature enhance improve'.split()):L+=['enhancement']
if any(x in t for x in'docs doc readme'.split()):L+=['documentation']
if L:s.run(['gh','issue','edit',str(i['number']),'--add