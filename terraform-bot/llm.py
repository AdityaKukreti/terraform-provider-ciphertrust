import json,os,urllib.error,urllib.request
ALLOWED={'bug','documentation','enhancement','question','duplicate','needs-repro'}
MODEL=os.getenv('GROQ_MODEL','llama-3.1-8b-instant')
URL='https://api.groq.com/openai/v1/chat/completions'
LAST_ERROR=''

def ask(prompt):
    global LAST_ERROR
    key=os.getenv('GROQ_API_KEY')
    if not key:
        LAST_ERROR='missing_key';return ''
    data={'model':MODEL,'temperature':0,'messages':[{'role':'user','content':prompt}]}
    req=urllib.request.Request(URL,data=json.dumps(data).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
        r=json.loads(urllib.request.urlopen(req,timeout=20).read())
        LAST_ERROR='ok';return r['choices'][0]['message']['content'].strip()
    except urllib.error.HTTPError as e:
        LAST_ERROR='http_'+str(e.code);return ''
    except Exception as e:
        LAST_ERROR=type(e).__name__;return ''

def status():
    txt=ask('Reply with OK only.')
    return 'Groq status: '+LAST_ERROR+(' using '+MODEL if txt else '')

def classify(issue):
    p='Classify this GitHub issue. Return JSON only: {"labels":[],"confidence":0.0}. Allowed labels: '+', '.join(sorted(ALLOWED))+'\nTitle: '+issue.get('title','')+'\nBody: '+str(issue.get('body',''))[:3000]
    try:
        txt=ask(p);obj=json.loads(txt[txt.find('{'):txt.rfind('}')+1])
        if float(obj.get('confidence',0))<0.7:return []
        return [x for x in obj.get('labels',[]) if x in ALLOWED]
    except Exception:return []

def summarize(issue):
    p='Summarize this Terraform provider GitHub issue for maintainers. Include Summary, Likely area, Missing info.\nTitle: '+issue.get('title','')+'\nBody: '+str(issue.get('body',''))[:5000]
    return ask(p)[:3000]

def duplicate_reason(issue,cands):
    p='Find true duplicate issues. Return JSON only: {"duplicates":[{"issue_number":0,"confidence":0.0,"reason":""}]}. New: '+issue.get('title','')+'\nCandidates: '+json.dumps(cands)[:5000]
    try:
        txt=ask(p);obj=json.loads(txt[txt.find('{'):txt.rfind('}')+1])
        return obj.get('duplicates',[])
    except Exception:return []
