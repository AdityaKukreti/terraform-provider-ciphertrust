import json,subprocess as s,re
import llm
import github_api as gh
STOP=set('the a an and or to of for in on with when from into this that is are be by have has had was were into using while during'.split())

RESOURCE_RE=re.compile(r'\b(?:resource|data source|datasource)\s+["`]?([a-zA-Z0-9_\-]+)')
ERROR_RE=re.compile(r'(?i)(error|exception|panic|failed|failure|unauthorized|forbidden|timeout|invalid|cannot|unable)[^\n]{0,160}')

def text(issue):
    return (str(issue.get('title',''))+' '+str(issue.get('body') or '')).lower()

def words(x):
    out=[]
    for w in x.lower().replace('-',' ').replace('_',' ').split():
        w=''.join(c for c in w if c.isalnum())
        if len(w)>2 and w not in STOP:out.append(w)
    return set(out)

def signals(issue):
    raw=str(issue.get('title',''))+'\n'+str(issue.get('body') or '')
    low=raw.lower()
    resources=set(m.group(1).lower() for m in RESOURCE_RE.finditer(raw))
    errors=set(m.group(0).lower().strip() for m in ERROR_RE.finditer(raw))
    auth=set(x for x in ['auth','authentication','token','credential','unauthorized','forbidden','login','api key'] if x in low)
    return {'resources':resources,'errors':errors,'auth':auth,'words':words(raw)}

def search_candidates(issue,base):
    queries=[]
    title=' '.join(list(words(issue.get('title','')))[:5])
    if title:queries.append(title)
    sig=signals(issue)
    if sig['resources']:queries.extend(list(sig['resources'])[:3])
    if sig['auth']:queries.append(' '.join(list(sig['auth'])[:3]))
    seen={issue['number']}; out=[]
    for q in queries[:4]:
        r=s.run(['gh','issue','list','--state','all','--search',q,'--json','number,title,url,body','--limit','15'],text=True,capture_output=True)
        if r.returncode:
            gh.log('duplicates','search failed for query '+q+': '+(r.stderr or r.stdout)[-200:])
            continue
        for item in json.loads(r.stdout or '[]'):
            if item['number'] in seen:continue
            seen.add(item['number']); out.append(item)
    return out

def score(issue,candidate):
    a=signals(issue); b=signals(candidate)
    total=0.0; reasons=[]
    word_score=len(a['words']&b['words'])/max(1,len(a['words']|b['words']))
    total+=word_score
    if a['resources'] and a['resources']&b['resources']:
        total+=0.45; reasons.append('same Terraform resource/data source: '+', '.join(sorted(a['resources']&b['resources'])))
    if a['auth'] and a['auth']&b['auth']:
        total+=0.25; reasons.append('same auth/token/credential signal')
    if a['errors'] and b['errors']:
        overlap=False
        for x in a['errors']:
            for y in b['errors']:
                if x[:40] in y or y[:40] in x or len(words(x)&words(y))>=3:
                    overlap=True
        if overlap:
            total+=0.35; reasons.append('similar error wording')
    if not reasons and word_score>=0.35:
        reasons.append('similar title/body keywords')
    return total,reasons

def run(issue):
    base=words(issue.get('title','')+' '+str(issue.get('body') or ''))
    if len(base)<2:return
    candidates=search_candidates(issue,base)
    if not candidates:return
    llm_hits=llm.duplicate_reason(issue,candidates)
    msg=[]; used=set()
    for h in llm_hits:
        if float(h.get('confidence',0))>=.7:
            n=h.get('issue_number')
            msg.append('- #'+str(n)+' — '+h.get('reason','possible duplicate'))
            used.add(int(n)) if str(n).isdigit() else None
    scored=[]
    for x in candidates:
        if x['number'] in used:continue
        sc,reasons=score(issue,x)
        if sc>=0.35:
            scored.append((sc,x,reasons))
    for sc,x,reasons in sorted(scored,key=lambda z:z[0],reverse=True)[:3-len(msg)]:
        reason='; '.join(reasons[:2]) if reasons else 'similar issue'
        msg.append('- #'+str(x['number'])+' '+x['title']+' — '+reason+' '+x['url'])
    if msg:
        try:
            gh.add_comment(issue['number'],'Possible duplicate issues:\n'+'\n'.join(msg[:3]))
        except Exception as e:
            gh.log('duplicates','failed commenting on #'+str(issue['number'])+': '+type(e).__name__+': '+str(e)[:300])
