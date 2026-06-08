import json,subprocess as s
STOP=set('the a an and or to of for in on with when from into this that is are be by'.split())

def words(x):
    out=[]
    for w in x.lower().replace('-',' ').replace('_',' ').split():
        w=''.join(c for c in w if c.isalnum())
        if len(w)>2 and w not in STOP:out.append(w)
    return set(out)

def run(issue):
    base=words(issue.get('title',''))
    if len(base)<2:return
    q=' '.join(list(base)[:5])
    r=s.run(['gh','issue','list','--state','all','--search',q,'--json','number,title,url','--limit','10'],text=True,capture_output=True)
    if r.returncode:return
    msg=[]
    for x in json.loads(r.stdout or '[]'):
        if x['number']==issue['number']:continue
        other=words(x['title'])
        score=len(base&other)/max(1,len(base|other))
        if score>=.35:msg.append('- #'+str(x['number'])+' '+x['title']+' '+x['url'])
    if msg:
        s.run(['gh','issue','comment',str(issue['number']),'--body','Possible duplicate issues:\n'+'\n'.join(msg[:3])],check=False)
