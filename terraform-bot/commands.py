import subprocess as s
import llm
import labeler
ALLOWED={'OWNER','MEMBER','COLLABORATOR'}
HELP='''Terraform bot commands:\n- `/bot help`\n- `/bot label` auto-detect labels\n- `/bot label bug` add one label manually\n- `/bot needs-repro`\n- `/bot duplicate #123`\n- `/bot summarize`\n- `/bot groq-check`\n'''

def comment(n,msg):s.run(['gh','issue','comment',str(n),'--body',msg],check=False)

def run(issue,c):
    body=c.get('body','').strip()
    if not body.startswith('/bot'):return
    n=issue['number'];p=body.split()
    if c.get('author_association') not in ALLOWED:
        return comment(n,'Only repo collaborators can run bot commands.')
    if len(p)<2 or p[1]=='help':return comment(n,HELP)
    if p[1]=='groq-check':return comment(n,llm.status())
    if p[1]=='summarize':
        msg=llm.summarize(issue) or ('LLM summary unavailable. '+llm.LAST_ERROR)
        return comment(n,msg)
    if p[1]=='label':
        if len(p)>2:
            label=' '.join(p[2:])
            r=s.run(['gh','issue','edit',str(n),'--add-label',label],capture_output=True,text=True)
            if r.returncode==0:return comment(n,'Added label: '+label)
            return comment(n,'Could not add label `'+label+'`. It may not exist in this repo. GitHub said: '+(r.stderr or r.stdout)[-500:])
        labels=labeler.suggest(issue)
        if not labels:return comment(n,'No matching labels detected for this issue.')
        r=s.run(['gh','issue','edit',str(n),'--add-label',','.join(labels)],capture_output=True,text=True)
        if r.returncode==0:return comment(n,'Added labels: '+', '.join(labels))
        return comment(n,'Detected labels: '+', '.join(labels)+' but could not apply them. GitHub said: '+(r.stderr or r.stdout)[-500:])
    if p[1]=='needs-repro':
        msg=llm.summarize(issue) or 'Please add reproduction steps, expected/actual behavior, and provider/Terraform versions.'
        s.run(['gh','issue','edit',str(n),'--add-label','needs-repro'],check=False);return comment(n,msg)
    if p[1]=='duplicate' and len(p)>2:
        s.run(['gh','issue','edit',str(n),'--add-label','duplicate'],check=False);return comment(n,'Possible duplicate of '+p[2])
