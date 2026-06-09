import json,os
from groq import Groq
ALLOWED={'bug','documentation','enhancement','question','duplicate','needs-repro'}
INTENTS={'help','features','risk','triage','summarize','needs-repro','duplicate','unknown'}
MODEL=os.getenv('GROQ_MODEL','llama-3.1-8b-instant')
LAST_ERROR=''

def ask(prompt):
    global LAST_ERROR
    if not os.getenv('GROQ_API_KEY'):
        LAST_ERROR='missing_key';return ''
    try:
        c=Groq().chat.completions.create(model=MODEL,messages=[{'role':'user','content':prompt}],temperature=0,max_completion_tokens=1024,top_p=1,stream=False)
        LAST_ERROR='ok';return c.choices[0].message.content.strip()
    except Exception as e:
        LAST_ERROR=type(e).__name__+': '+str(e)[:180];return ''

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

def intent(command_text,issue):
    p='''You are a safe GitHub maintainer-bot intent classifier.
Return JSON only: {"intent":"unknown","confidence":0.0,"args":{}}.
Allowed intents: help, features, risk, triage, summarize, needs-repro, duplicate, unknown.
Rules:
- Use triage for requests to check labels, apply labels, inspect labels, classify, or triage.
- Use risk for requests asking whether it is safe, risky, high risk, or what the risk is.
- Use summarize for summary/explain/what is this about.
- Use features for capabilities/docs/what can you do.
- Use needs-repro when the user asks to request reproduction details.
- Use duplicate only when the user asks to mark/check duplicate; include issue number in args.duplicate_of if explicitly present like #123.
- Never output destructive intents like close, merge, delete, approve, or edit workflow.
- If unsure, use unknown.

Command text: '''+command_text[:1000]+'''\nIssue title: '''+issue.get('title','')[:500]+'''\nIssue body: '''+str(issue.get('body') or '')[:1500]
    try:
        txt=ask(p)
        obj=json.loads(txt[txt.find('{'):txt.rfind('}')+1])
        name=str(obj.get('intent','unknown'))
        conf=float(obj.get('confidence',0))
        if name not in INTENTS or conf<0.75:
            return {'intent':'unknown','confidence':conf,'args':{}}
        args=obj.get('args',{}) if isinstance(obj.get('args',{}),dict) else {}
        return {'intent':name,'confidence':conf,'args':args}
    except Exception as e:
        return {'intent':'unknown','confidence':0.0,'args':{}}
