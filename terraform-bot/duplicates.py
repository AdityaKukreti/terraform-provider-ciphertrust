import json,subprocess as s
import llm
import github_api as gh
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
    c=[x for x in json.loads(r.stdout or '[]') if x['number']!=issue['number']]
    if not c:return
    llm_hits=llm.duplicate_reason(issue,c)
    msg=[]
    for h in llm_hits:
        if float(h.get('confidence',0))>=.7:
            msg.append('- #'+str(h.get('issue_number'))+' — '+h.get('reason',''))
    if not msg:
        for x in c:
            score=len(base&words(x['title']))/max(1,len(base|words(x['title'])))
            if score>=.35:msg.append('- #'+str(x['number'])+' '+x['title']+' '+x['url'])
    if msg:
        try:
            gh.add_comment(issue['number'],'Possible duplicate issues:\n'+'\n'.join(msg[:3]))
        except Exception as e:
            gh.log('duplicates','failed commenting on #'+str(issue['number'])+': '+type(e).__name__+': '+str(e)[:300])
