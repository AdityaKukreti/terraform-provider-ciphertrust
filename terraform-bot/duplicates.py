import re
import github_api as gh
import commenter

STOP=set('''the a an and or to of for in on with when from into this that is are be by have has had was were using while during can cannot could should would will not no yes issue terraform ciphertrust provider manager thales please help unable cannot getting'''.split())

TF_BLOCK_RE=re.compile(r'(?i)\b(?:resource|data)\s+"([a-z0-9_\-]+)"')
TF_NAME_RE=re.compile(r'(?i)\b(ciphertrust_[a-z0-9_]+|cckm_[a-z0-9_]+|cte_[a-z0-9_]+)\b')
ENV_RE=re.compile(r'\b(?:CIPHERTRUST|CTE|CCKM|CM)_[A-Z0-9_]+\b')
HTTP_RE=re.compile(r'\b(?:40[013489]|409|42[29]|50[0234])\b')
ERROR_LINE_RE=re.compile(r'(?im)^.*(?:error|exception|panic|failed|failure|unauthorized|forbidden|timeout|invalid|cannot|unable|denied|nil pointer|segmentation|crash).*$')
AREA_TERMS={
    'auth':['auth','authentication','login','token','credential','unauthorized','forbidden','password','certificate','tls','ssl'],
    'aws':['aws','kms','xks','cloudhsm','custom key store'],
    'azure':['azure','akv','key vault'],
    'gcp':['gcp','google'],
    'oci':['oci','oracle','vault','compartment'],
    'cte':['cte','guardpoint','client group','policy','ldt'],
    'connection':['connection','scp','proxy','ldap'],
    'cm':['domain','cluster','license','ntp','syslog','prometheus','scheduler'],
    'key':['key','keys','rotation','encrypt','decrypt','material'],
}


def _text(issue):
    return str(issue.get('title') or '')+'\n'+str(issue.get('body') or '')


def _title(issue):
    return str(issue.get('title') or '')


def _labels(issue):
    raw=issue.get('labels') or []
    out=[]
    for l in raw:
        if isinstance(l,dict) and l.get('name'):
            out.append(l['name'])
        elif isinstance(l,str):
            out.append(l)
    return set(out)


def words(text):
    text=(text or '').lower().replace('_',' ').replace('-',' ')
    found=re.findall(r'[a-z0-9]{3,}',text)
    return set(w for w in found if w not in STOP and not w.isdigit())


def phrases(text):
    out=[]
    for line in ERROR_LINE_RE.findall(text or '')[:5]:
        clean=' '.join(line.strip().split())
        if len(clean)>20:
            out.append(clean[:180].lower())
    return set(out)


def signals(issue):
    raw=_text(issue)
    low=raw.lower()
    area=set()
    for name,terms in AREA_TERMS.items():
        if any(t in low for t in terms):
            area.add(name)
    resources=set(x.lower() for x in TF_BLOCK_RE.findall(raw)) | set(x.lower() for x in TF_NAME_RE.findall(raw))
    env=set(x.upper() for x in ENV_RE.findall(raw))
    http=set(HTTP_RE.findall(raw))
    errs=phrases(raw)
    return {
        'title_words':words(_title(issue)),
        'body_words':words(raw),
        'resources':resources,
        'env':env,
        'http':http,
        'errors':errs,
        'areas':area,
        'labels':_labels(issue),
    }


def jaccard(a,b):
    if not a or not b:
        return 0.0
    return len(a&b)/max(1,len(a|b))


def overlap(a,b):
    return sorted(a&b)


def error_overlap(a,b):
    hits=[]
    for x in a:
        xw=words(x)
        for y in b:
            yw=words(y)
            if not xw or not yw:
                continue
            if x[:60] in y or y[:60] in x or len(xw&yw)>=3:
                hits.append(x[:90])
                break
    return hits[:2]


def search_terms(issue):
    sig=signals(issue)
    terms=[]
    if sig['resources']:
        terms.extend(sorted(sig['resources'])[:5])
    if sig['env']:
        terms.extend(sorted(sig['env'])[:3])
    if sig['http']:
        terms.extend(sorted(sig['http'])[:3])
    for e in sorted(sig['errors'],key=len,reverse=True)[:2]:
        ew=[w for w in words(e) if len(w)>3]
        if ew:
            terms.append(' '.join(ew[:5]))
    tw=[w for w in sig['title_words'] if len(w)>3]
    if tw:
        terms.append(' '.join(sorted(tw)[:6]))
    if sig['areas']:
        terms.append(' '.join(sorted(sig['areas'])[:4]))
    dedup=[]
    for t in terms:
        t=' '.join(str(t).split())
        if t and t not in dedup:
            dedup.append(t)
    return dedup[:8]


def search_candidates(issue):
    seen={issue.get('number')}
    out=[]
    for q in search_terms(issue):
        for item in gh.search_issues(q,limit=25):
            if item.get('pull_request'):
                continue
            n=item.get('number')
            if not n or n in seen:
                continue
            seen.add(n)
            out.append(item)
    return out[:60]


def score(issue,candidate):
    a=signals(issue); b=signals(candidate)
    total=0.0; reasons=[]
    title_sim=jaccard(a['title_words'],b['title_words'])
    body_sim=jaccard(a['body_words'],b['body_words'])
    if title_sim>=0.22:
        total+=min(0.30,title_sim*0.75); reasons.append('similar title keywords')
    if body_sim>=0.16:
        total+=min(0.18,body_sim*0.45); reasons.append('similar body keywords')
    res=overlap(a['resources'],b['resources'])
    if res:
        total+=0.34; reasons.append('same Terraform resource/data source: '+', '.join(res[:3]))
    env=overlap(a['env'],b['env'])
    if env:
        total+=0.22; reasons.append('same environment variable: '+', '.join(env[:2]))
    http=overlap(a['http'],b['http'])
    if http:
        total+=0.14; reasons.append('same HTTP/status code: '+', '.join(http[:2]))
    err=error_overlap(a['errors'],b['errors'])
    if err:
        total+=0.28; reasons.append('similar error wording')
    areas=overlap(a['areas'],b['areas'])
    if areas:
        total+=min(0.18,0.06*len(areas)); reasons.append('same area: '+', '.join(areas[:3]))
    labs=[l for l in overlap(a['labels'],b['labels']) if l not in {'needs-info','stale'}]
    if labs:
        total+=min(0.08,0.03*len(labs)); reasons.append('shared labels: '+', '.join(sorted(labs)[:3]))
    if res and err:
        total+=0.12
    if res and areas:
        total+=0.08
    return min(total,1.0),reasons


def candidate_url(c):
    return c.get('html_url') or c.get('url') or ''


def run(issue):
    if len(words(_text(issue)))<2:
        return
    candidates=search_candidates(issue)
    scored=[]
    for c in candidates:
        sc,reasons=score(issue,c)
        if sc>=0.65:
            scored.append((sc,c,reasons))
    scored=sorted(scored,key=lambda x:x[0],reverse=True)[:5]
    if not scored:
        gh.log('duplicates','no strong duplicate candidates for #'+str(issue.get('number')))
        return
    lines=['## Possible duplicate issues','']
    lines.append('I found similar existing issues. No issue was closed automatically.')
    lines.append('')
    lines.append('| Candidate | Why |')
    lines.append('| --- | --- |')
    for sc,c,reasons in scored:
        why='; '.join(reasons[:3]) if reasons else 'similar title/body signals'
        url=candidate_url(c)
        ref='[#'+str(c.get('number'))+']('+url+')' if url else '#'+str(c.get('number'))
        title=str(c.get('title') or '').replace('|','-')[:90]
        lines.append('| '+ref+' '+title+' | '+why.replace('|','-')+' |')
    lines.append('')
    lines.append('_Handled by ciphertrust-bot._')
    try:
        commenter.upsert(issue['number'],'duplicates','\n'.join(lines))
    except Exception as e:
        gh.log('duplicates','failed commenting on #'+str(issue['number'])+': '+type(e).__name__+': '+str(e)[:300])
