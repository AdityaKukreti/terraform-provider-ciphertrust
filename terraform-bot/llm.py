import json,os,urllib.request

ALLOWED={'bug','documentation','enhancement','question','duplicate','needs-repro'}
MODEL=os.getenv('GROQ_MODEL','llama-3.1-8b-instant')
URL='https://api.groq.com/openai/v1/chat/completions'

def classify(issue):
    key=os.getenv('GROQ_API_KEY')
    if not key:return []
    prompt='Classify this GitHub issue. Return JSON only: {"labels":[],"confidence":0.0}. Allowed labels: '+', '.join(sorted(ALLOWED))+'\nTitle: '+issue.get('title','')+'\nBody: '+str(issue.get('body',''))[:3000]
    data={'model':MODEL,'temperature':0,'messages':[{'role':'user','content':prompt}]}
    req=urllib.request.Request(URL,data=json.dumps(data).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
        res=json.loads(urllib.request.urlopen(req,timeout=20).read())
        txt=res['choices'][0]['message']['content'].strip()
        obj=json.loads(txt[txt.find('{'):txt.rfind('}')+1])
        if float(obj.get('confidence',0))<0.7:return []
        return [x for x in obj.get('labels',[]) if x in ALLOWED]
    except Exception:
        return []
