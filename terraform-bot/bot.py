import json,os,subprocess as s
e=json.load(open(os.environ['GITHUB_EVENT_PATH']))
i=e['issue'];t=(i['title']+' '+str(i.get('body'))).lower();L=[]
if 'bug' in t or 'error' in t:L+=['bug']
if 'docs' in t or 'readme' in t:L+=['documentation']
if L:s.run(['gh','issue','edit',str(i['number']),'--add-label',','.join(L)])
